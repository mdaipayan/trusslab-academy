"""Reusable Streamlit presenters for lesson content, objectives and quizzes."""
from __future__ import annotations

from html import escape
from typing import Any
import pandas as pd
import streamlit as st

from trusslab.domain.models import ContentBlock, LessonModule
from trusslab.domain.glossary import GLOSSARY
from trusslab.services.learning import LearningService, ProgressService
from trusslab.ui.theme import CSS


def inject_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)




def render_glossary() -> None:
    """Render the standalone reference page for engineering symbols and abbreviations."""
    st.markdown('<div class="module-kicker">REFERENCE PAGE</div>', unsafe_allow_html=True)
    st.title("Abbreviations & symbols")
    st.markdown(
        "A quick reference for the notation used throughout TrussLab Academy. "
        "This page is separate from the lessons so it can grow as new app features are added."
    )
    st.info(
        "**Member force:** use **F** for axial member force. "
        "**N** is the unit newton, not the member-force symbol. "
        "With the sign convention used here, positive force means tension and negative force means compression."
    )
    for heading, rows in GLOSSARY:
        st.markdown(f"### {heading}")
        st.dataframe(
            pd.DataFrame(rows, columns=("Symbol / abbreviation", "Meaning", "How to read it in this app")),
            width="stretch",
            hide_index=True,
        )


def render_objectives(module: LessonModule, progress: ProgressService) -> None:
    mastered = progress.is_mastered(module.id)
    status = "✓ Objective achieved" if mastered else "○ In progress"
    rows = []
    for index, objective in enumerate(module.objectives, start=1):
        icon = "✓" if mastered else str(index)
        rows.append(f'<div class="objective-line"><span class="objective-index">{icon}</span>{escape(objective)}</div>')
    st.markdown(
        '<div class="objective-card"><div class="objective-heading">Your learning objective · ' + escape(status) + '</div>'
        + "".join(rows) + '</div>',
        unsafe_allow_html=True,
    )


def _render_callout_text(text: str) -> str:
    """Escape lesson text and preserve simple **bold** emphasis in HTML callouts."""
    import re

    parts: list[str] = []
    cursor = 0
    for match in re.finditer(r"\*\*(.+?)\*\*", text):
        parts.append(escape(text[cursor:match.start()]))
        parts.append(f"<strong>{escape(match.group(1))}</strong>")
        cursor = match.end()
    parts.append(escape(text[cursor:]))
    return "".join(parts).replace("\\n", "<br>")


def _render_block(block: ContentBlock) -> None:
    if block.heading:
        st.markdown(f'<div class="content-heading">{escape(block.heading)}</div>', unsafe_allow_html=True)
    if block.kind == "paragraph":
        st.markdown(block.text)
    elif block.kind in {"bullets", "steps"}:
        if block.kind == "steps":
            lines = [f"{index}. {item}" for index, item in enumerate(block.items, start=1)]
        else:
            lines = [f"- {item}" for item in block.items]
        st.markdown("\n".join(lines))
    elif block.kind == "formula":
        if block.text:
            st.markdown(block.text)
        st.latex(block.formula)
    elif block.kind == "callout":
        tone = block.tone if block.tone in {"info", "success", "warning", "danger", "highlight"} else "info"
        heading = f'<div class="callout-title">{escape(block.heading)}</div>' if block.heading else ""
        st.markdown(f'<div class="callout callout-{tone}">{heading}{_render_callout_text(block.text)}</div>', unsafe_allow_html=True)
    elif block.kind == "table":
        df = pd.DataFrame(block.table_rows, columns=block.table_headers)
        st.dataframe(df, width="stretch", hide_index=True)


def render_lesson_blocks(module: LessonModule) -> None:
    for block in module.sections:
        _render_block(block)


def render_quiz(module: LessonModule, learning: LearningService, progress: ProgressService) -> None:
    """Render the module-end mastery quiz and its option-specific feedback."""
    st.markdown("### Check your understanding")
    st.markdown(
        '<div class="muted">Three short questions, directly aligned with the objectives above. '
        'Answer all three correctly to mark this objective as achieved. You can retry after reviewing the feedback.</div>',
        unsafe_allow_html=True,
    )
    attempt_count = progress.attempt_count(module.id)
    best_score = progress.best_score(module.id)
    if attempt_count:
        st.caption(f"Attempts this session: {attempt_count} · Best score: {best_score}/{len(module.quiz)}")
    else:
        st.caption("No attempts yet in this session.")

    if progress.is_mastered(module.id):
        result = progress.result(module.id)
        st.markdown(
            '<div class="objective-achieved"><strong>✓ Objective achieved.</strong> '
            'You have mastered this module. Revisit the lesson any time to refresh your understanding.</div>',
            unsafe_allow_html=True,
        )
        _render_result(module, result)
        return

    attempt = int(st.session_state.get(f"quiz_attempt_{module.id}", 0))
    pending_warning = None
    with st.form(key=f"quiz_form_{module.id}_{attempt}", clear_on_submit=False, border=False):
        for index, question in enumerate(module.quiz, start=1):
            st.markdown(
                f'<div class="quiz-question"><div class="quiz-number">Question {index} of {len(module.quiz)}</div>'
                f'<div class="quiz-prompt">{escape(question.prompt)}</div></div>',
                unsafe_allow_html=True,
            )
            option_map = {option.id: option.text for option in question.options}
            st.radio(
                f"Choose an answer for question {index}",
                options=list(option_map),
                index=None,
                format_func=lambda option_id, labels=option_map: labels[option_id],
                key=f"answer_{module.id}_{attempt}_{question.id}",
                label_visibility="collapsed",
            )
        submitted = st.form_submit_button("Check answers", type="primary", width="stretch")
    if submitted:
        answers: dict[str, str | None] = {
            question.id: st.session_state.get(f"answer_{module.id}_{attempt}_{question.id}")
            for question in module.quiz
        }
        if any(answer is None for answer in answers.values()):
            pending_warning = "Please answer all three questions before checking your result."
        else:
            evaluation = learning.evaluate(module, answers)
            progress.record(module.id, evaluation)
            st.rerun()
    if pending_warning:
        st.warning(pending_warning)

    result = progress.result(module.id)
    if result:
        _render_result(module, result)
        if not result["passed"]:
            if st.button("Try the quiz again", key=f"retry_{module.id}_{attempt}", width="stretch"):
                progress.clear_latest_result(module.id)
                st.session_state[f"quiz_attempt_{module.id}"] = attempt + 1
                st.rerun()


def _render_result(module: LessonModule, result: dict[str, Any] | None) -> None:
    if not result:
        return
    score, total = result["score"], result["total"]
    if result["passed"]:
        st.success(f"Objective achieved — {score}/{total} correct. Excellent work!")
    else:
        st.warning(f"You scored {score}/{total}. Review the explanations below, then try again.")
    feedback_by_id = {item["question_id"]: item for item in result["feedback"]}
    for index, question in enumerate(module.quiz, start=1):
        item = feedback_by_id[question.id]
        selected = item["selected_text"]
        correct = item["correct_text"]
        if item["is_correct"]:
            st.markdown(
                f'<div class="feedback-correct"><strong>Q{index} · Correct</strong><br>'
                f'Your answer: {escape(selected)}<br>{escape(item["explanation"])}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="feedback-wrong"><strong>Q{index} · Review</strong><br>'
                f'Your answer: {escape(selected)}<br>Answer to learn: {escape(correct)}<br>'
                f'{escape(item["explanation"])}</div>',
                unsafe_allow_html=True,
            )
