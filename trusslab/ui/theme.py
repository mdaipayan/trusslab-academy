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
</style>
"""
