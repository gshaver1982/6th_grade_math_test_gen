# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 18:08:24 2026

@author: Garrett
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile

from flask import Flask, render_template_string, request, send_file

from generators import build_question_set
from pdf_writer import write_answer_key_pdf, write_worksheet_pdf

app = Flask(__name__)

PAGE = """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Math Test Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 40px auto;
            padding: 0 16px;
            line-height: 1.5;
        }
        .card {
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        label {
            display: block;
            margin-top: 16px;
            font-weight: 600;
        }
        input {
            width: 100%;
            padding: 10px;
            margin-top: 6px;
            box-sizing: border-box;
        }
        button {
            margin-top: 20px;
            padding: 12px 18px;
            border: 0;
            border-radius: 8px;
            background: #1f6feb;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background: #1558b0;
        }
        .hint {
            color: #666;
            font-size: 14px;
            margin-top: 6px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Math Test Generator</h1>
        <form method="post" action="/generate">
            <label for="num_questions">Number of questions</label>
            <input id="num_questions" name="num_questions" type="number" min="1" value="25">

            <label for="seed">Seed (optional)</label>
            <input id="seed" name="seed" type="number" placeholder="Leave blank for random">

            <label for="base_name">Base filename</label>
            <input id="base_name" name="base_name" type="text" value="math_practice_test">

            <div class="hint">The download will contain both the worksheet and the answer key.</div>

            <button type="submit">Generate PDF</button>
        </form>
    </div>
</body>
</html>
"""


@app.get("/")
def home():
    return render_template_string(PAGE)


@app.post("/generate")
def generate():
    num_questions = int(request.form.get("num_questions", "25"))
    seed_text = request.form.get("seed", "").strip()
    seed = int(seed_text) if seed_text else None
    base_name = request.form.get("base_name", "math_practice_test").strip() or "math_practice_test"

    questions = build_question_set(num_questions=num_questions, seed=seed)

    with TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        worksheet_path = tmpdir_path / f"{base_name}.pdf"
        answer_key_path = tmpdir_path / f"{base_name}_answer_key.pdf"

        write_worksheet_pdf(questions, worksheet_path)
        write_answer_key_pdf(questions, answer_key_path)

        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w", compression=ZIP_DEFLATED) as zf:
            zf.write(worksheet_path, arcname=worksheet_path.name)
            zf.write(answer_key_path, arcname=answer_key_path.name)

        zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name=f"{base_name}.zip",
        mimetype="application/zip",
    )


if __name__ == "__main__":
    app.run(debug=True)