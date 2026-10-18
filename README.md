# TrussLab Academy

A fresh, modular Streamlit learning app for civil-engineering students. Every module has explicit learning objectives, a focused lesson, an interactive illustration or experiment where useful, and a three-question mastery quiz at the end.

## Product principles

- **One objective-led module at a time.** Students can see what they are expected to learn before reading.
- **Small assessment at the end.** Three single-answer questions test that module's objectives. A module is marked mastered at 3/3; students can review feedback and retry.
- **Glass-box engineering.** Equations are paired with plain-language meanings, symbol definitions, sign conventions and worked numerical steps. Member axial force is denoted by **F** consistently; **N** is reserved for the unit newton. The in-app **Symbols & abbreviations** reference defines the notation, engineering terms and units. 
- **Plain language first.** Short paragraphs, meaningful bullets, highlighted cautions and equation cards keep the page approachable.
- **Object-oriented and testable.** Content models, lesson catalog, quiz evaluation, progress handling, visualizations and UI rendering are separated.

## Run locally

Python 3.10 or later is recommended.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Run the standard-library tests:

```bash
python -m unittest discover -s tests -v
```

## Fresh GitHub repository

This folder is a clean repository starter and does not change the previous `truss_learning_app` project. To publish it, create a new empty repository on GitHub named `trusslab-academy` (do not initialize it with a README), then run from this folder:

```bash
git init -b main
git add .
git commit -m "Initial TrussLab Academy learning platform"
git remote add origin https://github.com/<your-username>/trusslab-academy.git
git push -u origin main
```

The current connected GitHub tools can edit existing repositories but do not expose a create-repository operation, so the remote repository creation step must be done from GitHub's **New repository** page. The complete starter source and tests are included here.

## Architecture

```text
app.py                      Streamlit composition root and session wiring
trusslab/domain/models.py   Typed lesson, content-block, and quiz models
trusslab/domain/catalog.py  The authored learning path and module content
trusslab/domain/glossary.py Student-facing engineering symbols, abbreviations and units
SYMBOLS_AND_ABBREVIATIONS.md  Human-readable glossary reference
trusslab/services/learning.py
                            Pure quiz evaluation and session progress service
trusslab/services/engineering.py
                            Small, testable calculations grounded in the notes
trusslab/ui/theme.py        Design tokens and responsive CSS
trusslab/ui/diagrams.py     Reusable Plotly structural diagrams
trusslab/ui/components.py   Reusable lesson and quiz presenters
trusslab/ui/experiments.py  Interactive what-if sandboxes
 tests/                     Tests for lessons, quizzes, calculations and diagrams
```

## Symbols and abbreviations

The app includes a **Symbols & abbreviations used in this app** expander below each module. The same 47-entry reference is available in [SYMBOLS_AND_ABBREVIATIONS.md](SYMBOLS_AND_ABBREVIATIONS.md). The app uses **F** for signed axial member force (such as `F_AB`) and **N** only for the force unit newton.

## Learning path

1. Truss foundations
2. Read common truss layouts
3. Determinacy and stability
4. Method of joints
5. Method of sections
6. Worked determinate 3–4–5 truss
7. Truss compatibility: redundant support reaction
8. Indeterminate triangle: redundant reaction
9. Internal redundancy: force method
10. Truss optimization as a glass-box process

## Progress and persistence

The starter uses Streamlit session state. Progress is available while the student's app session remains active; it is not yet tied to a user account or external database. The `ProgressService` boundary is intentionally isolated so authentication and durable storage can be added later without mixing them into lesson content.

## Engineering scope and source audit

The learning content follows the three provided study-note PDFs, with explanatory additions for equilibrium and compatibility. The ideal-truss lessons state that applied point loads act at joints. Module 7 uses an actual pin-jointed 3–4–5 triangular truss with a 10 kN downward joint load and one redundant horizontal support reaction at C. Students release the redundant, solve the determinate primary truss, use a unit-load system, and enforce zero horizontal displacement at C to recover the reaction. The lesson does not use a frame, rigid loading plate or between-joint load. The rectangular-truss force-method note reports a denominator of 13,400/(EA), but its displayed terms add to 12,280/(EA). The app flags the arithmetic discrepancy and asks for the internal-redundant compatibility convention to be checked rather than presenting the reported redundant force as a verified result. This is an educational tool, not an engineering design/code-compliance package; buckling, connection, fabrication, load-combination and code checks are outside this starter's scope.
