"""TrussLab Academy — objective-led structural engineering lessons."""
from __future__ import annotations

import streamlit as st

from trusslab.domain.catalog import get_modules
from trusslab.domain.models import LessonModule
from trusslab.services.learning import LearningService, ProgressService
from trusslab.ui.components import inject_theme, render_glossary, render_lesson_blocks, render_objectives, render_quiz
from trusslab.ui.diagrams import DiagramFactory
from trusslab.ui.experiments import ExperimentRenderer

st.set_page_config(page_title="TrussLab Academy", page_icon="🔺", layout="wide", initial_sidebar_state="expanded")

MODULES = get_modules()
LEARNING = LearningService()
PROGRESS = ProgressService(st.session_state)


def _navigate(module_id: str) -> None:
    st.session_state["module_nav_radio"] = module_id


def _render_sidebar() -> str:
    st.sidebar.markdown(
        '<div style="padding:.45rem 0 .3rem"><div style="font-size:.68rem;letter-spacing:.16em;font-weight:900;color:#75d8cc;text-transform:uppercase">CIVIL ENGINEERING · LEARN</div>'
        '<div style="font-family:Manrope,Segoe UI,sans-serif;font-size:1.62rem;font-weight:900;letter-spacing:-.05em;color:#fff">TrussLab <span style="color:#75d8cc">Academy</span></div>'
        '<div style="color:#afc4cf;font-size:.82rem;line-height:1.5;margin-top:.3rem">Understand the behaviour. Then solve the structure.</div></div>',
        unsafe_allow_html=True,
    )
    st.sidebar.divider()
    completed = PROGRESS.mastered_count()
    percent = PROGRESS.completion_percent(len(MODULES))
    st.sidebar.markdown("<div style='font-size:.72rem;letter-spacing:.1em;font-weight:800;color:#9eb4c0;text-transform:uppercase'>Your progress</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<div style='font-size:1.75rem;font-weight:850;color:#fff;margin:.12rem 0'>{completed}<span style='font-size:.95rem;color:#9eb4c0'> / {len(MODULES)} modules</span></div>", unsafe_allow_html=True)
    st.sidebar.progress(percent / 100)
    st.sidebar.caption(f"{percent}% mastery achieved · Best score saved per module")
    st.sidebar.divider()

    module_by_id = {module.id: module for module in MODULES}
    def format_module(module_id: str) -> str:
        module = module_by_id[module_id]
        status = "✓" if PROGRESS.is_mastered(module_id) else "○"
        return f"{status}  {module.title}"

    selected_id = st.sidebar.radio(
        "YOUR LEARNING PATH", options=[module.id for module in MODULES], index=0,
        key="module_nav_radio", format_func=format_module,
    )
    st.sidebar.divider()
    st.sidebar.markdown("<div style='color:#9eb4c0;font-size:.78rem;line-height:1.7'>Every module ends with a 3-question mastery quiz. Get 3/3 to mark its objective as achieved. Progress is session-based in this starter.</div>", unsafe_allow_html=True)
    return selected_id


def _render_header() -> None:
    total = len(MODULES)
    complete = PROGRESS.mastered_count()
    st.markdown(
        '<div class="hero-panel"><div class="hero-eyebrow">A guided structural learning path</div>'
        '<div class="hero-title">Learn the behaviour, not just the formula.</div>'
        '<p class="hero-copy">Short lessons. Clear diagrams. Small experiments. A quiz at the end of every module so you know when the objective is achieved.</p></div>',
        unsafe_allow_html=True,
    )
    a, b, c = st.columns(3)
    a.metric("Modules mastered", f"{complete} / {total}")
    b.metric("Total study time", f"~{sum(module.minutes for module in MODULES)} min")
    c.metric("Quizzes per module", "3 questions", "All 3 correct = mastery")


def _render_module(module: LessonModule, index: int) -> None:
    done = PROGRESS.is_mastered(module.id)
    result = PROGRESS.result(module.id)
    score = PROGRESS.best_score(module.id)
    status = "MASTERED" if done else "IN PROGRESS"
    st.markdown(f'<div class="module-kicker">MODULE {index + 1:02d} / {len(MODULES):02d} · {module.level}</div>', unsafe_allow_html=True)
    st.markdown(f'<h1 class="module-title">{module.title}</h1>', unsafe_allow_html=True)
    st.markdown(f'<div class="module-subtitle">{module.subtitle}</div>', unsafe_allow_html=True)
    chips = f'<span class="pill">{module.minutes} MIN</span>&nbsp;&nbsp;<span class="pill">{status}</span>'
    if score is not None:
        chips += f'&nbsp;&nbsp;<span class="pill">BEST {score}/{len(module.quiz)}</span>'
    st.markdown(chips, unsafe_allow_html=True)
    st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="content-body">{module.purpose}</div>', unsafe_allow_html=True)
    render_objectives(module, PROGRESS)

    left, right = st.columns([1.15, .95], gap="large")
    with left:
        st.markdown("### The lesson")
        render_lesson_blocks(module)
    with right:
        st.markdown("### See the structure")
        st.plotly_chart(
            DiagramFactory.build(module.diagram_id), use_container_width=True,
            config={"responsive": True, "displaylogo": False, "scrollZoom": False},
            key=f"diagram_{module.id}",
        )
        st.markdown('<div class="muted">Hover over a joint or member for labels and coordinates. Diagrams are teaching schematics, not scale drawings.</div>', unsafe_allow_html=True)

    if module.experiment_id:
        st.divider()
        ExperimentRenderer.render(module)

    st.divider()
    render_quiz(module, LEARNING, PROGRESS)

    st.divider()
    previous_id = MODULES[index - 1].id if index > 0 else None
    next_id = MODULES[index + 1].id if index < len(MODULES) - 1 else None
    prev_col, progress_col, next_col = st.columns([1, 1.4, 1])
    with prev_col:
        if previous_id:
            st.button("← Previous module", key=f"prev_{module.id}", use_container_width=True,
                       on_click=_navigate, args=(previous_id,))
        else:
            st.button("← Course start", key="prev_start", disabled=True, use_container_width=True)
    with progress_col:
        st.markdown(f'<div class="muted" style="text-align:center;padding:.7rem 0">Module {index+1} of {len(MODULES)} · {PROGRESS.mastered_count()} objectives achieved</div>', unsafe_allow_html=True)
    with next_col:
        if next_id:
            st.button("Next module →", key=f"next_{module.id}", use_container_width=True,
                       on_click=_navigate, args=(next_id,))
        else:
            st.button("End of learning path", key="next_end", disabled=True, use_container_width=True)


def main() -> None:
    inject_theme()
    selected_id = _render_sidebar()
    _render_header()
    index = next(i for i, module in enumerate(MODULES) if module.id == selected_id)
    _render_module(MODULES[index], index)
    render_glossary()
    st.markdown("<div class='muted' style='text-align:center;margin-top:1rem'>TrussLab Academy · Educational use only · Structural design certification is outside this app's scope.</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
