"""TrussLab Academy — objective-led structural engineering lessons."""
from __future__ import annotations

from html import escape

import streamlit as st

from trusslab.domain.catalog import get_modules
from trusslab.domain.models import LessonModule
from trusslab.services.learning import LearningService, ProgressService
from trusslab.ui.components import inject_theme, render_glossary, render_lesson_blocks, render_objectives, render_quiz
from trusslab.ui.diagrams import DiagramFactory
from trusslab.ui.experiments import ExperimentRenderer
from trusslab.ui.navigation import navigation_groups, navigation_label

st.set_page_config(page_title="TrussLab Academy", page_icon="🔺", layout="wide", initial_sidebar_state="expanded")

MODULES = get_modules()
LEARNING = LearningService()
PROGRESS = ProgressService(st.session_state)

FREE_BODY_TITLES = {
    "joint_c_fbd": "Isolate joint C",
    "section_cut_fbd": "Isolate the cut section",
    "whole_truss_fbd": "Whole-truss equilibrium",
    "released_truss_fbd": "Released primary truss",
    "unit_load_fbd": "Unit-load case",
    "loaded_truss_fbd": "Loaded truss",
    "joint_c_loaded_fbd": "Loaded joint C",
    "released_rectangular_fbd": "Remove redundant BD",
}


def _navigate(module_id: str) -> None:
    """Select a lesson from the sidebar or Previous/Next controls."""
    st.session_state["active_module_id"] = module_id


def _render_sidebar() -> str:
    st.sidebar.markdown(
        '<div class="academy-brand">'
        '<div class="academy-eyebrow">CIVIL ENGINEERING · LEARN</div>'
        '<div class="academy-brand-title">TrussLab <span>Academy</span></div>'
        '<div class="academy-brand-copy">Learn trusses · Solve step by step</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.sidebar.divider()

    completed = PROGRESS.mastered_count()
    percent = PROGRESS.completion_percent(len(MODULES))
    st.sidebar.markdown(
        '<div class="sidebar-section-kicker">YOUR PROGRESS</div>'
        f'<div class="sidebar-progress-row"><span class="sidebar-progress-count">{completed}</span>'
        f'<span class="sidebar-progress-total">of {len(MODULES)} mastered</span>'
        f'<span class="sidebar-progress-percent">{percent}%</span></div>',
        unsafe_allow_html=True,
    )
    st.sidebar.progress(percent / 100)
    st.sidebar.divider()

    module_by_id = {module.id: module for module in MODULES}
    module_ids = tuple(module.id for module in MODULES)
    selected_id = st.session_state.get("active_module_id", MODULES[0].id)
    if selected_id not in module_by_id:
        selected_id = MODULES[0].id
    st.session_state["active_module_id"] = selected_id

    st.sidebar.markdown('<div class="sidebar-nav-title">YOUR LEARNING PATH</div>', unsafe_allow_html=True)
    for group_title, group_ids in navigation_groups(module_ids):
        if not group_ids:
            continue
        group_done = sum(PROGRESS.is_mastered(module_id) for module_id in group_ids)
        st.sidebar.markdown(
            '<div class="sidebar-nav-group">'
            f'<span>{escape(group_title)}</span>'
            f'<span class="sidebar-nav-group-count">{group_done}/{len(group_ids)}</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        for module_id in group_ids:
            module = module_by_id[module_id]
            index = module_ids.index(module_id) + 1
            mastered = PROGRESS.is_mastered(module_id)
            label = navigation_label(module_id, mastered)
            st.sidebar.button(
                label,
                key=f"nav_{module_id}",
                type="primary" if module_id == selected_id else "secondary",
                use_container_width=True,
                on_click=_navigate,
                args=(module_id,),
                help=f"Module {index} of {len(MODULES)} · {module.title}",
            )

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



def _render_free_body_diagrams(module: LessonModule) -> None:
    """Show extra FBDs as a separate visual teaching aid."""
    if not module.free_body_ids:
        return

    st.divider()
    st.markdown("### Free-body diagrams")
    st.markdown(
        "A free-body diagram (FBD) shows **only the part you are analysing** and every force acting on it."
    )
    st.markdown(
        '<div class="fbd-legend">'
        '<span class="fbd-chip fbd-chip--load">Amber · applied loads</span>'
        '<span class="fbd-chip fbd-chip--reaction">Blue · support reactions</span>'
        '<span class="fbd-chip fbd-chip--tension">Green · assumed tension</span>'
        '<span class="fbd-chip fbd-chip--compression">Red · compression / cut marker</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    if len(module.free_body_ids) == 1:
        fbd_id = module.free_body_ids[0]
        st.plotly_chart(
            DiagramFactory.build_free_body(fbd_id),
            use_container_width=True,
            config={"responsive": True, "displaylogo": False, "scrollZoom": False},
            key=f"fbd_{module.id}_{fbd_id}",
        )
        return

    tabs = st.tabs([FREE_BODY_TITLES.get(fbd_id, fbd_id.replace("_", " ").title()) for fbd_id in module.free_body_ids])
    for tab, fbd_id in zip(tabs, module.free_body_ids):
        with tab:
            st.plotly_chart(
                DiagramFactory.build_free_body(fbd_id),
                use_container_width=True,
                config={"responsive": True, "displaylogo": False, "scrollZoom": False},
                key=f"fbd_{module.id}_{fbd_id}",
            )


def _render_module(module: LessonModule, index: int) -> None:
    done = PROGRESS.is_mastered(module.id)
    score = PROGRESS.best_score(module.id)
    status = "MASTERED" if done else "IN PROGRESS"
    status_class = "pill--success" if done else "pill--neutral"
    st.markdown(f'<div class="module-kicker">MODULE {index + 1:02d} / {len(MODULES):02d} · {module.level}</div>', unsafe_allow_html=True)
    st.markdown(f'<h1 class="module-title">{module.title}</h1>', unsafe_allow_html=True)
    st.markdown(f'<div class="module-subtitle">{escape(module.subtitle)}</div>', unsafe_allow_html=True)
    chips = f'<span class="pill">{module.minutes} MIN</span>&nbsp;&nbsp;<span class="pill {status_class}">{status}</span>'
    if score is not None:
        chips += f'&nbsp;&nbsp;<span class="pill">BEST {score}/{len(module.quiz)}</span>'
    st.markdown(chips, unsafe_allow_html=True)
    st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="content-body">{escape(module.purpose)}</div>', unsafe_allow_html=True)
    st.progress((index + 1) / len(MODULES), text=f"Learning path · module {index + 1} of {len(MODULES)}")
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

    _render_free_body_diagrams(module)

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
