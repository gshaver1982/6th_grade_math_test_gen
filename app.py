from __future__ import annotations

import secrets
from pathlib import Path
from tempfile import TemporaryDirectory

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
        .buttons {
            margin-top: 20px;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }
        button {
            padding: 12px 18px;
            border: 0;
            border-radius: 8px;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }
        .worksheet-btn {
            background: #1f6feb;
        }
        .worksheet-btn:hover {
            background: #1558b0;
        }
        .key-btn {
            background: #28a745;
        }
        .key-btn:hover {
            background: #1e7e34;
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
        <form method="post">
            <input type="hidden" name="fallback_seed" value="{{ fallback_seed }}">

            <label for="num_questions">Number of questions</label>
            <input id="num_questions" name="num_questions" type="number" min="1" value="25">

            <label for="seed">Seed (optional)</label>
            <input id="seed" name="seed" type="number" placeholder="Leave blank for random">

            <label for="base_name">Base filename</label>
            <input id="base_name" name="base_name" type="text" value="math_practice_test">

            <div class="hint">
                If seed is blank, both downloads use the same hidden seed so the worksheet and answer key match.
            </div>

            <div class="buttons">
                <button class="worksheet-btn" type="submit" formaction="/worksheet">
                    Download Worksheet
                </button>
                <button class="key-btn" type="submit" formaction="/answer-key">
                    Download Answer Key
                </button>
            </div>
        </form>
    </div>
</body>
</html>
"""


def _resolve_seed() -> int:
    seed_text = request.form.get("seed", "").strip()
    if seed_text:
        return int(seed_text)

    fallback_seed = request.form.get("fallback_seed", "").strip()
    if fallback_seed:
        return int(fallback_seed)

    return secrets.randbelow(1_000_000_000)


def _resolve_num_questions() -> int:
    return int(request.form.get("num_questions", "25"))


def _resolve_base_name() -> str:
    return request.form.get("base_name", "math_practice_test").strip() or "math_practice_test"


@app.get("/")
def home():
    fallback_seed = secrets.randbelow(1_000_000_000)
    return render_template_string(PAGE, fallback_seed=fallback_seed)


@app.post("/worksheet")
def worksheet():
    num_questions = _resolve_num_questions()
    seed = _resolve_seed()
    base_name = _resolve_base_name()

    questions = build_question_set(num_questions=num_questions, seed=seed)

    with TemporaryDirectory() as tmpdir:
        worksheet_path = Path(tmpdir) / f"{base_name}.pdf"
        write_worksheet_pdf(questions, worksheet_path)

        return send_file(
            worksheet_path,
            as_attachment=True,
            download_name=f"{base_name}.pdf",
            mimetype="application/pdf",
        )


@app.post("/answer-key")
def answer_key():
    num_questions = _resolve_num_questions()
    seed = _resolve_seed()
    base_name = _resolve_base_name()

    questions = build_question_set(num_questions=num_questions, seed=seed)

    with TemporaryDirectory() as tmpdir:
        answer_key_path = Path(tmpdir) / f"{base_name}_answer_key.pdf"
        write_answer_key_pdf(questions, answer_key_path)

        return send_file(
            answer_key_path,
            as_attachment=True,
            download_name=f"{base_name}_answer_key.pdf",
            mimetype="application/pdf",
        )


if __name__ == "__main__":
    app.run(debug=True)