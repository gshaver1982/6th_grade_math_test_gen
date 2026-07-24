# Math Test Generator

Generates a 25-question math practice worksheet and answer key as PDFs.

## Usage

```bash
python main.py --num-questions 25 --seed 7 --output-dir out --base-name practice_test
```

Outputs:
- `practice_test.pdf`
- `practice_test_answer_key.pdf`

## Notes

- Layout is fixed at 5 questions per page.
- Each question includes an answer line and a small work box.
- Questions are balanced across several 6th-grade math topics.
