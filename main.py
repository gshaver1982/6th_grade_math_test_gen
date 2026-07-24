from __future__ import annotations

import argparse
from pathlib import Path

from generators import build_question_set
from pdf_writer import write_answer_key_pdf, write_worksheet_pdf


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a 6th-grade math practice test PDF and answer key.")
    parser.add_argument("--num-questions", type=int, default=25, help="Number of questions to generate.")
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed for reproducible worksheets.")
    parser.add_argument("--difficulty", type=str, default="medium", choices=["easy", "medium", "hard"], help="Difficulty level.")
    parser.add_argument("--output-dir", type=str, default=".", help="Directory for generated PDFs.")
    parser.add_argument("--base-name", type=str, default="math_practice_test", help="Base filename for outputs.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    questions = build_question_set(num_questions=args.num_questions, seed=args.seed, difficulty=args.difficulty)

    worksheet_path = output_dir / f"{args.base_name}.pdf"
    key_path = output_dir / f"{args.base_name}_answer_key.pdf"

    write_worksheet_pdf(questions, worksheet_path)
    write_answer_key_pdf(questions, key_path)

    print(worksheet_path)
    print(key_path)


if __name__ == "__main__":
    main()
