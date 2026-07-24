from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas

from config import BODY_FONT, BODY_FONT_BOLD, MARGIN_BOTTOM, MARGIN_LEFT, MARGIN_RIGHT, MARGIN_TOP, PAGE_HEIGHT, PAGE_WIDTH, QUESTIONS_PER_PAGE, SMALL_FONT, TITLE_BLOCK_HEIGHT, WORK_BOX_HEIGHT
from generators import Question


TITLE_STYLE = ParagraphStyle(
    "title",
    fontName=BODY_FONT_BOLD,
    fontSize=16,
    leading=18,
    spaceAfter=0,
)

META_STYLE = ParagraphStyle(
    "meta",
    fontName=BODY_FONT,
    fontSize=10,
    leading=12,
)

QUESTION_STYLE = ParagraphStyle(
    "question",
    fontName=BODY_FONT,
    fontSize=11,
    leading=13,
)

ANSWER_STYLE = ParagraphStyle(
    "answer",
    fontName=BODY_FONT_BOLD,
    fontSize=11,
    leading=13,
)


def _draw_header(c: canvas.Canvas, title: str, subtitle: str, page_num: int, total_pages: int) -> float:
    top = PAGE_HEIGHT - MARGIN_TOP
    c.setFont(BODY_FONT_BOLD, 16)
    c.drawString(MARGIN_LEFT, top, title)

    c.setFont(BODY_FONT, 10)
    c.drawString(MARGIN_LEFT, top - 16, subtitle)

    '''c.setFont(BODY_FONT, 10)
    c.drawString(MARGIN_LEFT, top - 30, "Name: ________________________________")
    c.drawString(PAGE_WIDTH - MARGIN_RIGHT - 170, top - 30, "Date: __________________")
'''
    c.setFont(BODY_FONT, 9)
    c.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, top, f"Page {page_num} of {total_pages}")

    return top - TITLE_BLOCK_HEIGHT


def _wrap_paragraph(text: str, style: ParagraphStyle, width: float) -> Paragraph:
    return Paragraph(text.replace("\n", "<br/>"), style)


def _draw_work_box(c: canvas.Canvas, x: float, y_bottom: float, width: float, height: float) -> None:
    c.setStrokeColor(colors.lightgrey)
    c.rect(x, y_bottom, width, height, stroke=1, fill=0)
    # faint ruled lines
    '''line_gap = 12
    current = y_bottom + line_gap
    while current < y_bottom + height - 4:
        c.line(x + 4, current, x + width - 4, current)
        current += line_gap
    c.setStrokeColor(colors.black)'''


def _draw_question_block(c: canvas.Canvas, num: int, question: Question, x: float, top_y: float, width: float, block_height: float) -> float:
    question_text = f"{num}. {question.prompt}"
    question_para = _wrap_paragraph(question_text, QUESTION_STYLE, width)
    q_w, q_h = question_para.wrap(width, block_height)
    question_para.drawOn(c, x, top_y - q_h)

    answer_y = top_y - q_h - 14
    c.setFont(BODY_FONT_BOLD, 11)
    c.drawString(x, answer_y, "Answer:")
    #c.line(x + 52, answer_y - 2, x + width - 6, answer_y - 2)

    box_top = answer_y - 12
    box_height = WORK_BOX_HEIGHT
    _draw_work_box(c, x, box_top - box_height, width, box_height)

    return box_top - box_height


def write_worksheet_pdf(questions: Sequence[Question], output_path: str | Path, title: str = "Math Practice Test") -> Path:
    output_path = Path(output_path)
    c = canvas.Canvas(str(output_path), pagesize=letter)
    c.setTitle(title)

    total_pages = (len(questions) + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE
    content_top = PAGE_HEIGHT - MARGIN_TOP
    usable_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    block_height = (PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM - TITLE_BLOCK_HEIGHT - 16) / QUESTIONS_PER_PAGE

    for page_index in range(total_pages):
        page_questions = questions[page_index * QUESTIONS_PER_PAGE:(page_index + 1) * QUESTIONS_PER_PAGE]
        top_y = _draw_header(c, title, "", page_index + 1, total_pages)
        y = top_y

        for idx, question in enumerate(page_questions, start=page_index * QUESTIONS_PER_PAGE + 1):
            y = _draw_question_block(c, idx, question, MARGIN_LEFT, y, usable_width, block_height)
            y -= 10

        c.showPage()

    c.save()
    return output_path


def write_answer_key_pdf(questions: Sequence[Question], output_path: str | Path, title: str = "Math Practice Test - Answer Key") -> Path:
    output_path = Path(output_path)
    c = canvas.Canvas(str(output_path), pagesize=letter)
    c.setTitle(title)

    total_pages = (len(questions) + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE
    usable_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    block_height = (PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM - TITLE_BLOCK_HEIGHT - 16) / QUESTIONS_PER_PAGE

    for page_index in range(total_pages):
        page_questions = questions[page_index * QUESTIONS_PER_PAGE:(page_index + 1) * QUESTIONS_PER_PAGE]
        _draw_header(c, title, "Answers and short solution notes.", page_index + 1, total_pages)
        top_y = PAGE_HEIGHT - MARGIN_TOP - TITLE_BLOCK_HEIGHT
        y = top_y

        for idx, question in enumerate(page_questions, start=page_index * QUESTIONS_PER_PAGE + 1):
            q_text = f"{idx}. {question.prompt}"
            q_para = _wrap_paragraph(q_text, QUESTION_STYLE, usable_width)
            q_w, q_h = q_para.wrap(usable_width, block_height)
            q_para.drawOn(c, MARGIN_LEFT, y - q_h)
            c.setFont(BODY_FONT_BOLD, 11)
            c.drawString(MARGIN_LEFT, y - q_h - 14, f"Answer: {question.answer}")
            c.setFont(SMALL_FONT, 9)
            c.drawString(MARGIN_LEFT, y - q_h - 27, question.work)
            y -= block_height + 10

        c.showPage()

    c.save()
    return output_path
