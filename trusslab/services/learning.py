"""Quiz evaluation and progress bookkeeping, independent of the UI."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, MutableMapping

from trusslab.domain.models import LessonModule


@dataclass(frozen=True, slots=True)
class QuestionFeedback:
    question_id: str
    selected_option_id: str | None
    correct_option_id: str
    is_correct: bool
    explanation: str
    selected_text: str
    correct_text: str


@dataclass(frozen=True, slots=True)
class QuizEvaluation:
    module_id: str
    score: int
    total: int
    passed: bool
    feedback: tuple[QuestionFeedback, ...]

    @property
    def percentage(self) -> int:
        return round(100 * self.score / self.total) if self.total else 0


class LearningService:
    """Evaluate a module quiz. Objective achievement requires all questions correct."""

    @staticmethod
    def evaluate(module: LessonModule, answers: dict[str, str | None]) -> QuizEvaluation:
        feedback: list[QuestionFeedback] = []
        for question in module.quiz:
            selected = answers.get(question.id)
            options = {option.id: option.text for option in question.options}
            correct = selected == question.correct_option_id
            feedback.append(QuestionFeedback(
                question_id=question.id,
                selected_option_id=selected,
                correct_option_id=question.correct_option_id,
                is_correct=correct,
                explanation=question.explanation,
                selected_text=options.get(selected, "Not answered"),
                correct_text=options[question.correct_option_id],
            ))
        score = sum(item.is_correct for item in feedback)
        total = len(feedback)
        return QuizEvaluation(module.id, score, total, total > 0 and score == total, tuple(feedback))


class ProgressService:
    """Store a student's session-scoped learning progress behind one small API."""

    STATE_KEY = "trusslab_progress_v1"

    def __init__(self, session_state: MutableMapping[str, Any]) -> None:
        self._state = session_state
        if self.STATE_KEY not in self._state:
            self._state[self.STATE_KEY] = {
                "mastered": [],
                "best_scores": {},
                "attempts": {},
                "results": {},
            }

    @property
    def data(self) -> dict[str, Any]:
        return self._state[self.STATE_KEY]

    def is_mastered(self, module_id: str) -> bool:
        return module_id in self.data["mastered"]

    def mastered_count(self) -> int:
        return len(self.data["mastered"])

    def completion_percent(self, module_count: int) -> int:
        return round(100 * self.mastered_count() / module_count) if module_count else 0

    def best_score(self, module_id: str) -> int | None:
        return self.data["best_scores"].get(module_id)

    def attempt_count(self, module_id: str) -> int:
        return int(self.data["attempts"].get(module_id, 0))

    def result(self, module_id: str) -> dict[str, Any] | None:
        return self.data["results"].get(module_id)

    def record(self, module_id: str, evaluation: QuizEvaluation) -> None:
        data = self.data
        data["attempts"][module_id] = int(data["attempts"].get(module_id, 0)) + 1
        previous = data["best_scores"].get(module_id, -1)
        data["best_scores"][module_id] = max(previous, evaluation.score)
        data["results"][module_id] = {
            "score": evaluation.score,
            "total": evaluation.total,
            "passed": evaluation.passed,
            "percentage": evaluation.percentage,
            "feedback": [
                {
                    "question_id": item.question_id,
                    "selected_option_id": item.selected_option_id,
                    "correct_option_id": item.correct_option_id,
                    "is_correct": item.is_correct,
                    "explanation": item.explanation,
                    "selected_text": item.selected_text,
                    "correct_text": item.correct_text,
                }
                for item in evaluation.feedback
            ],
        }
        if evaluation.passed and module_id not in data["mastered"]:
            data["mastered"].append(module_id)

    def clear_latest_result(self, module_id: str) -> None:
        self.data["results"].pop(module_id, None)
