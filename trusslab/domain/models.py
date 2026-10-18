"""Typed domain objects for objective-led lessons and mastery checks."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

BlockKind = Literal["paragraph", "bullets", "steps", "formula", "callout", "table"]
CalloutTone = Literal["info", "success", "warning", "danger", "highlight"]


@dataclass(frozen=True, slots=True)
class ContentBlock:
    """One reusable piece of lesson content."""

    kind: BlockKind
    heading: str = ""
    text: str = ""
    items: tuple[str, ...] = ()
    formula: str = ""
    tone: CalloutTone = "info"
    table_headers: tuple[str, ...] = ()
    table_rows: tuple[tuple[str, ...], ...] = ()

    def __post_init__(self) -> None:
        if self.kind == "formula" and not self.formula.strip():
            raise ValueError("Formula content blocks must contain a formula.")
        if self.kind in {"bullets", "steps"} and not self.items:
            raise ValueError(f"{self.kind} content blocks must contain at least one item.")
        if self.kind == "table":
            if not self.table_headers or not self.table_rows:
                raise ValueError("Table content blocks need headers and at least one row.")
            if any(len(row) != len(self.table_headers) for row in self.table_rows):
                raise ValueError("Every table row must have the same number of cells as its header.")


@dataclass(frozen=True, slots=True)
class QuizOption:
    id: str
    text: str

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.text.strip():
            raise ValueError("Quiz options need a non-empty id and display text.")


@dataclass(frozen=True, slots=True)
class QuizQuestion:
    id: str
    prompt: str
    options: tuple[QuizOption, ...]
    correct_option_id: str
    explanation: str
    hint: str

    def __post_init__(self) -> None:
        ids = [option.id for option in self.options]
        if not self.id.strip() or not self.prompt.strip():
            raise ValueError("Questions need an id and prompt.")
        if len(ids) < 2 or len(ids) != len(set(ids)):
            raise ValueError(f"Question {self.id!r} must have unique options.")
        if self.correct_option_id not in ids:
            raise ValueError(f"Question {self.id!r} points to an unknown correct option.")
        if not self.explanation.strip() or not self.hint.strip():
            raise ValueError("Every question needs feedback and a hint.")


@dataclass(frozen=True, slots=True)
class LessonModule:
    id: str
    title: str
    subtitle: str
    purpose: str
    level: str
    minutes: int
    objectives: tuple[str, ...]
    sections: tuple[ContentBlock, ...]
    quiz: tuple[QuizQuestion, ...]
    diagram_id: str
    experiment_id: str | None = None
    free_body_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not all((self.id, self.title, self.subtitle, self.purpose, self.level, self.diagram_id)):
            raise ValueError("A lesson module is missing required metadata.")
        if self.minutes <= 0:
            raise ValueError("Estimated lesson time must be positive.")
        if not self.objectives:
            raise ValueError(f"Module {self.id!r} needs at least one learning objective.")
        question_ids = [question.id for question in self.quiz]
        if len(self.quiz) != 3:
            raise ValueError(f"Module {self.id!r} must have exactly three mastery questions.")
        if len(question_ids) != len(set(question_ids)):
            raise ValueError(f"Module {self.id!r} has duplicate question ids.")

    @property
    def objective_count(self) -> int:
        return len(self.objectives)
