"""Design system: approachable typography, calm surfaces and semantic highlights."""

CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root {
  --ink: #152535; --muted: #647789; --teal: #0d9488; --teal-soft: #e2f5f2;
  --amber: #f3c969; --amber-soft: #fff5d8; --line: #e3e9ed;
  --surface: #ffffff; --canvas: #f6f8fa; --danger: #b42332; --danger-soft: #fff0f0;
  --success: #16794b; --success-soft: #e8f7ee; --blue: #245fbd; --blue-soft: #edf4ff;
}
html, body, [data-testid="stAppViewContainer"] {
  background: var(--canvas); color: var(--ink);
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
}
[data-testid="stAppViewContainer"] * { font-family: 'DM Sans', 'Segoe UI', sans-serif; }
h1, h2, h3, h4, .hero-title, .module-title, .brand-title {
  font-family: 'Manrope', 'Segoe UI', sans-serif !important;
  letter-spacing: -0.035em;
}
.main .block-container { max-width: 1360px; padding: 1.6rem 2.2rem 3.2rem; }
[data-testid="stSidebar"] { background: #152535; border-right: 1px solid #243c4d; }
[data-testid="stSidebar"] * { color: #edf5f7; }
[data-testid="stSidebar"] hr { border-color: #344958; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { font-size: .88rem; line-height: 1.3; }
[data-testid="stSidebar"] [data-testid="stRadio"] > label { color: #9eb4c0; font-size: .75rem; font-weight: 800; text-transform: uppercase; letter-spacing: .09em; }
[data-testid="stSidebar"] [data-testid="stProgressBar"] > div { background: #314756; }
[data-testid="stSidebar"] [data-testid="stProgressBar"] div div { background: #48c7b6; }
.stButton > button, [data-testid="stFormSubmitButton"] button {
  border-radius: 12px; min-height: 2.75rem; font-weight: 750;
  border: 1px solid var(--line); transition: border-color .15s, transform .15s;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] button:hover { border-color: var(--teal); transform: translateY(-1px); }
.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] button[kind="primary"] {
  background: var(--teal); border-color: var(--teal); color: #fff;
}
.stButton > button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] button[kind="primary"]:hover { background: #08796f; border-color: #08796f; }
[data-testid="stMetric"] { background: var(--surface); border: 1px solid var(--line); border-radius: 15px; padding: .8rem 1rem; }
[data-testid="stMetricLabel"] { color: var(--muted); font-size: .8rem; }
[data-testid="stMetricValue"] { font-family: 'Manrope', 'Segoe UI', sans-serif !important; color: var(--ink); }
hr { border-color: var(--line); }
.hero-panel {
  background: linear-gradient(120deg, #132b3b 0%, #1b4653 62%, #0d766f 100%);
  color: white; border-radius: 24px; padding: 1.45rem 1.65rem 1.55rem;
  margin: .2rem 0 1.3rem; box-shadow: 0 12px 28px rgba(24,57,72,.12);
}
.hero-eyebrow { font-size: .74rem; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; color: #a5e7de; margin-bottom: .45rem; }
.hero-title { color:#fff; font-size: clamp(1.75rem, 3vw, 2.45rem); font-weight: 800; line-height: 1.13; margin: 0 0 .55rem; }
.hero-copy { color: #e4f3f4; font-size: 1rem; line-height: 1.7; max-width: 780px; margin: 0; }
.module-kicker { color: var(--teal); text-transform: uppercase; letter-spacing: .12em; font-size: .72rem; font-weight: 800; margin-bottom: .38rem; }
.module-title { font-size: clamp(1.65rem, 2.8vw, 2.25rem); line-height: 1.18; color: var(--ink); margin: 0 0 .45rem; font-weight: 800; }
.module-subtitle { color: var(--muted); font-size: 1rem; line-height: 1.55; margin-bottom: .9rem; }
.pill { display:inline-block; border-radius: 999px; padding:.28rem .62rem; font-size:.72rem; font-weight:800; letter-spacing:.04em; background:var(--teal-soft); color:#086b63; }
.objective-card, .lesson-card, .quiz-card, .progress-card {
  background: var(--surface); border: 1px solid var(--line); border-radius: 17px;
  padding: 1rem 1.15rem; box-shadow: 0 4px 14px rgba(20,45,58,.035); margin-bottom: .8rem;
}
.objective-card { border-left: 5px solid var(--teal); }
.objective-heading { color: var(--muted); font-size: .72rem; letter-spacing:.11em; text-transform:uppercase; font-weight:800; margin-bottom:.5rem; }
.objective-line { color:var(--ink); font-size:.96rem; line-height:1.55; margin:.35rem 0; }
.objective-index { display:inline-flex; align-items:center; justify-content:center; border-radius:8px; width:1.45rem; height:1.45rem; margin-right:.5rem; background:var(--teal-soft); color:#086b63; font-weight:800; font-size:.78rem; }
.content-heading { color:var(--ink); font-size:1.08rem; font-weight:800; margin:.5rem 0 .55rem; }
.content-body { color:#314758; font-size:1rem; line-height:1.78; }
.callout { border-radius: 12px; padding: .85rem 1rem; margin:.65rem 0 1rem; border:1px solid transparent; font-size:.94rem; line-height:1.68; }
.callout-title { font-weight:800; margin-bottom:.24rem; }
.callout-info { background:var(--blue-soft); color:#204a86; border-color:#d4e4ff; }
.callout-success { background:var(--success-soft); color:#145e3d; border-color:#c7ebd5; }
.callout-warning { background:var(--amber-soft); color:#744900; border-color:#f6e4a9; }
.callout-danger { background:var(--danger-soft); color:#8d1f2a; border-color:#f6cfd3; }
.callout-highlight { background:#fff5c2; color:#5f4700; border-color:#f1d66c; border-left:4px solid #d6a71f; }
.objective-achieved { background:var(--success-soft); border:1px solid #c7ebd5; border-radius:14px; padding:.95rem 1rem; color:#145e3d; line-height:1.6; }
.quiz-question { border:1px solid var(--line); border-radius:15px; padding:.8rem 1rem .4rem; margin:.55rem 0 .8rem; background:#fff; }
.quiz-number { color:var(--teal); font-weight:900; font-size:.73rem; letter-spacing:.1em; text-transform:uppercase; margin-bottom:.2rem; }
.quiz-prompt { color:var(--ink); font-size:1rem; font-weight:750; line-height:1.5; margin-bottom:.35rem; }
.feedback-correct { background:var(--success-soft); border-left:4px solid #22a06b; color:#145e3d; border-radius:8px; padding:.65rem .8rem; margin:.45rem 0; line-height:1.55; }
.feedback-wrong { background:var(--danger-soft); border-left:4px solid #d94b56; color:#8d1f2a; border-radius:8px; padding:.65rem .8rem; margin:.45rem 0; line-height:1.55; }
.muted { color:var(--muted); font-size:.84rem; line-height:1.6; }
.st-key-learn, [data-testid="stPlotlyChart"] { max-width:100%; }
[data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
@media (max-width: 850px) {
  .main .block-container { padding:1rem .85rem 2rem; }
  .hero-panel { padding:1.15rem 1rem; border-radius:18px; }
  .objective-card, .lesson-card, .quiz-card { padding:.85rem; }
  [data-testid="stHorizontalBlock"] { flex-wrap:wrap; gap:.75rem !important; }
  [data-testid="stHorizontalBlock"] > [data-testid="column"] { flex:1 1 100% !important; min-width:100% !important; max-width:100% !important; }
  .stButton > button { width:100%; }
}
@media (prefers-reduced-motion: reduce) { * { transition:none !important; } }

/* Keyboard accessibility and compact-screen polish */
:focus-visible { outline: 3px solid #f0b429 !important; outline-offset: 3px !important; border-radius: 5px; }
.stProgress > div > div { border-radius: 999px; }
[data-testid="stCaptionContainer"] { line-height: 1.55; }
[data-testid="stRadio"] [role="radiogroup"] { gap: .42rem; }
[data-testid="stRadio"] [role="radio"] { align-items: flex-start; line-height: 1.45; }
[data-testid="stDataFrame"] { background: #fff; }
[data-testid="stPlotlyChart"] { border-radius: 14px; overflow: hidden; }
.stAlert { border-radius: 12px; }
.pill--success { background: var(--success-soft); color: #145e3d; }
.pill--neutral { background: #e9eef2; color: #40586a; }
@media (max-width: 520px) { .hero-title { font-size: 1.65rem; } .module-title { font-size: 1.55rem; overflow-wrap: anywhere; } [data-testid="stMetric"] { padding: .65rem .7rem; } [data-testid="stMetricValue"] { font-size: 1.25rem; } .quiz-question { padding: .75rem .8rem .35rem; } }

/* Emphasise key terms without adding more paragraphs */
.main [data-testid="stMarkdownContainer"] strong { color: #08796f; font-weight: 800; }
.content-heading { padding-left: .55rem; border-left: 3px solid var(--teal); }
[data-testid="stTabs"] button { font-weight: 750; }
.fbd-legend { display: flex; flex-wrap: wrap; gap: .5rem; margin: .25rem 0 .65rem; color: var(--muted); font-size: .82rem; }
.fbd-chip { display: inline-block; border-radius: 999px; padding: .22rem .55rem; background: #fff; border: 1px solid var(--line); font-weight: 700; }
.fbd-chip--load { color: #a86400; border-color: #f3c969; }
.fbd-chip--reaction { color: #245fbd; border-color: #bcd2f5; }
.fbd-chip--tension { color: #16794b; border-color: #b8e5ce; }
.fbd-chip--compression { color: #b42332; border-color: #f1b8be; }

/* Compact, grouped learning-path sidebar */
[data-testid="stSidebarContent"] { padding: .55rem .62rem .65rem !important; }
[data-testid="stSidebar"] .academy-brand { padding: .05rem 0 .1rem !important; }
[data-testid="stSidebar"] .academy-eyebrow { color:#75d8cc; font-size:.64rem; font-weight:900; letter-spacing:.14em; text-transform:uppercase; line-height:1.25; }
[data-testid="stSidebar"] .academy-brand-title { margin-top:.08rem; color:#fff; font-family:'Manrope','Segoe UI',sans-serif !important; font-size:1.28rem; font-weight:900; letter-spacing:-.045em; white-space:nowrap; line-height:1.2; }
[data-testid="stSidebar"] .academy-brand-title span { color:#75d8cc; }
[data-testid="stSidebar"] .academy-brand-copy { color:#afc4cf; font-size:.72rem; line-height:1.28; margin-top:.12rem; max-width:230px; }
[data-testid="stSidebar"] .sidebar-section-kicker { display:block; color:#9eb4c0; font-size:.64rem; font-weight:850; letter-spacing:.12em; line-height:1.3; margin:.04rem 0 .1rem !important; }
[data-testid="stSidebar"] .sidebar-progress-row { display:flex; align-items:baseline; gap:.35rem; margin:0 0 .08rem !important; line-height:1.2; }
[data-testid="stSidebar"] .sidebar-progress-count { color:#fff; font-size:1.42rem; font-weight:900; line-height:1.1; }
[data-testid="stSidebar"] .sidebar-progress-total { color:#d0dde3; font-size:.8rem; font-weight:650; }
[data-testid="stSidebar"] .sidebar-progress-percent { margin-left:auto; color:#75d8cc; font-size:.8rem; font-weight:850; }
[data-testid="stSidebar"] [data-testid="stProgressBar"] { margin:.08rem 0 .06rem !important; }
[data-testid="stSidebar"] hr { border-color:#344958; margin:.34rem 0 !important; }
[data-testid="stSidebar"] .sidebar-nav-title { display:block; color:#ffffff; font-size:.75rem; font-weight:900; letter-spacing:.09em; line-height:1.35; padding:.12rem 0 .2rem; margin:.12rem 0 .14rem !important; }
[data-testid="stSidebar"] .sidebar-nav-group { display:flex; justify-content:space-between; align-items:center; min-height:.85rem; padding:.18rem .1rem .08rem !important; margin:.20rem 0 .12rem !important; color:#9bb4c1; font-size:.60rem; font-weight:900; letter-spacing:.11em; line-height:1.25; }
[data-testid="stSidebar"] .sidebar-nav-group-count { color:#7896a5; letter-spacing:0; font-size:.63rem; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap:.42rem !important; }

/* Stable Streamlit button test IDs are used instead of the old kind= CSS
   attribute. The latter stopped matching current Streamlit button markup. */
[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"] {
  display:flex !important;
  align-items:center !important;
  justify-content:flex-start !important;
  text-align:left !important;
  min-height:1.82rem !important;
  height:auto !important;
  padding:.18rem .48rem !important;
  border-radius:8px !important;
  border:1px solid #355064 !important;
  background:#1b3040 !important;
  background-color:#1b3040 !important;
  color:#e5eef2 !important;
  font-size:.77rem !important;
  font-weight:650 !important;
  line-height:1.18 !important;
  white-space:normal !important;
  box-shadow:none !important;
  margin:0 !important;
  transform:none !important;
}
[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"] p,
[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"] span {
  color:#e5eef2 !important;
  font-size:.77rem !important;
  line-height:1.18 !important;
  margin:0 !important;
}
[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]:hover {
  background:#28485a !important;
  background-color:#28485a !important;
  border-color:#71a0b0 !important;
  color:#ffffff !important;
}
[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]:hover p,
[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]:hover span {
  color:#ffffff !important;
}
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {
  display:flex !important;
  align-items:center !important;
  justify-content:flex-start !important;
  text-align:left !important;
  min-height:1.82rem !important;
  height:auto !important;
  padding:.18rem .48rem !important;
  border-radius:8px !important;
  border:1px solid #56d0c4 !important;
  background:#0d9488 !important;
  background-color:#0d9488 !important;
  color:#ffffff !important;
  font-size:.77rem !important;
  font-weight:850 !important;
  line-height:1.18 !important;
  white-space:normal !important;
  box-shadow:0 2px 7px rgba(0,0,0,.12) !important;
  margin:0 !important;
  transform:none !important;
}
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] p,
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] span {
  color:#ffffff !important;
  font-size:.77rem !important;
  line-height:1.18 !important;
  margin:0 !important;
}
[data-testid="stSidebar"] button[data-testid^="stBaseButton-"]:focus-visible {
  outline:3px solid #f0b429 !important;
  outline-offset:2px !important;
}
@media (max-width: 850px) {
  [data-testid="stSidebar"] .academy-brand-title { font-size:1.24rem !important; }
  [data-testid="stSidebar"] button[data-testid^="stBaseButton-"] { min-height:2rem !important; }
}

</style>
"""
