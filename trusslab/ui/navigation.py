"""Compact labels and groups for the student learning-path sidebar."""

from __future__ import annotations

from typing import Final


NAV_LABELS: Final[dict[str, str]] = {
    "foundations": "Foundations",
    "truss-types": "Truss layouts",
    "determinacy": "Determinacy",
    "joints": "Method of joints",
    "sections": "Method of sections",
    "determinate-example": "Worked 3–4–5 truss",
    "truss-compatibility": "Truss compatibility",
    "indeterminate-triangle": "Redundant reaction",
    "force-method": "Force method",
    "optimization": "Optimization",
}

# Grouping mirrors the learning sequence without repeating long lesson titles.
NAV_GROUPS: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    ("START HERE", ("foundations", "truss-types", "determinacy")),
    ("SOLVE TRUSSES", ("joints", "sections", "determinate-example")),
    ("COMPATIBILITY", ("truss-compatibility", "indeterminate-triangle", "force-method")),
    ("DESIGN", ("optimization",)),
)

# Standalone reference pages are separate from the lesson sequence. Add future
# destinations (for example, an "App scope" page) here when their content is ready.
SIDEBAR_PAGES: Final[tuple[tuple[str, str], ...]] = (
    ("glossary", "Abbreviations & symbols"),
)


def navigation_groups(module_ids: tuple[str, ...]) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Return valid groups in course order, including any ungrouped future modules."""
    known = set(module_ids)
    groups = tuple(
        (title, tuple(module_id for module_id in ids if module_id in known))
        for title, ids in NAV_GROUPS
    )
    grouped = {module_id for _, ids in groups for module_id in ids}
    ungrouped = tuple(module_id for module_id in module_ids if module_id not in grouped)
    if ungrouped:
        return groups + (("MORE", ungrouped),)
    return groups


def navigation_label(module_id: str, mastered: bool = False) -> str:
    """Return a concise sidebar label without a lesson number."""
    label = NAV_LABELS.get(module_id, module_id.replace("-", " ").title())
    return f"✓  {label}" if mastered else label
