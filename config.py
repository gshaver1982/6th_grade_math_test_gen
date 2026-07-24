from dataclasses import dataclass
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

PAGE_SIZE = letter
PAGE_WIDTH, PAGE_HEIGHT = PAGE_SIZE

MARGIN_LEFT = 0.5 * inch
MARGIN_RIGHT = 0.5 * inch
MARGIN_TOP = 0.5 * inch
MARGIN_BOTTOM = 0.5 * inch

TITLE_FONT = "Helvetica-Bold"
BODY_FONT = "Helvetica"
BODY_FONT_BOLD = "Helvetica-Bold"
SMALL_FONT = "Helvetica"

QUESTIONS_PER_PAGE = 5
TITLE_BLOCK_HEIGHT = 0.1 * inch
WORK_BOX_HEIGHT = 1.35 * inch
SHOW_WORKBOX_BORDER = False
SHOW_WORKBOX_LINES = False

FONT_NAME = "Helvetica"
FONT_SIZE = 11

PAGE_MARGIN = 0.5 * inch
DEFAULT_QUESTION_COUNT = 25


@dataclass(frozen=True)
class WorksheetConfig:
    num_questions: int = DEFAULT_QUESTION_COUNT
    seed: int | None = None
    difficulty: str = "medium"