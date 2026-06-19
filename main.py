import streamlit as st
import pandas as pd
import hashlib
import plotly.express as px
import plotly.graph_objects as go
import string
import math
import time
import json
import base64 as b64lib
from fpdf import FPDF
from cipher import (
    CaesarCipher, VigenereCipher, AtbashCipher, ROT13Cipher,
    XORCipher, RailFenceCipher, HashTools, Base64Tools, CipherCompare,
    calculate_entropy, get_character_frequencies
)
from storage import StorageManager

# ─────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="⚡ AEGIS SOVEREIGN SUITE PRO v4.0",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="⚡"
)

storage = StorageManager()

# ─────────────────────────────────────────────────────────
#  GLOBAL CSS — NEON CYBER GLASSMORPHIC TERMINAL
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

/* ── ROOT RESET ─────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background:
        radial-gradient(ellipse at 10% 20%, rgba(0,245,212,0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(139,92,246,0.06) 0%, transparent 50%),
        linear-gradient(160deg, #020818 0%, #040d22 40%, #010410 100%) !important;
    color: #c9d1d9 !important;
    font-family: 'Share Tech Mono', monospace !important;
    min-height: 100vh;
}

/* ── SIDEBAR ─────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020818 0%, #010410 100%) !important;
    border-right: 1px solid rgba(0,245,212,0.2) !important;
    box-shadow: 4px 0 30px rgba(0,245,212,0.05) !important;
}
section[data-testid="stSidebar"] * { color: #e6edf3 !important; }

/* ── HEADINGS ─────────────────────────────────────── */
h1, h2, h3, h4 {
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 2px !important;
}
h1 { color: #00f5d4 !important; text-shadow: 0 0 20px rgba(0,245,212,0.5), 0 0 40px rgba(0,245,212,0.2) !important; font-size: 1.6rem !important; }
h2 { color: #00b4d8 !important; text-shadow: 0 0 15px rgba(0,180,216,0.4) !important; font-size: 1.25rem !important; }
h3 { color: #8b5cf6 !important; text-shadow: 0 0 10px rgba(139,92,246,0.4) !important; font-size: 1.05rem !important; }

/* ── CARDS / PANELS ───────────────────────────────── */
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
    background: rgba(6, 18, 40, 0.7) !important;
    border: 1px solid rgba(0,180,216,0.18) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.5), inset 0 1px 0 rgba(0,245,212,0.06) !important;
    margin-bottom: 16px !important;
}

/* ── METRICS ──────────────────────────────────────── */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(0,245,212,0.06) 0%, rgba(0,180,216,0.03) 100%) !important;
    border: 1px solid rgba(0,245,212,0.25) !important;
    border-radius: 10px !important;
    padding: 16px !important;
    position: relative;
    overflow: hidden;
}
div[data-testid="metric-container"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,245,212,0.6), transparent);
}
div[data-testid="stMetricValue"] {
    color: #00f5d4 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    text-shadow: 0 0 12px rgba(0,245,212,0.5) !important;
}
div[data-testid="stMetricLabel"] label { color: #8f9aa5 !important; letter-spacing: 1.5px !important; text-transform: uppercase !important; font-size: 0.65rem !important; }
div[data-testid="stMetricDelta"] { font-family: monospace !important; }

/* ── INPUTS ───────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput input {
    background: rgba(2, 12, 27, 0.9) !important;
    color: #00f5d4 !important;
    border: 1px solid rgba(0,180,216,0.3) !important;
    border-radius: 8px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.9rem !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #00f5d4 !important;
    box-shadow: 0 0 0 2px rgba(0,245,212,0.15), 0 0 20px rgba(0,245,212,0.1) !important;
    outline: none !important;
}

/* ── SELECTBOX ────────────────────────────────────── */
div[data-baseweb="select"] > div {
    background: rgba(2, 12, 27, 0.9) !important;
    border: 1px solid rgba(0,180,216,0.3) !important;
    border-radius: 8px !important;
    color: #00f5d4 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* ── BUTTONS ──────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, rgba(0,180,216,0.12) 0%, rgba(0,245,212,0.08) 100%) !important;
    border: 1px solid rgba(0,180,216,0.4) !important;
    color: #00f5d4 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.82rem !important;
    border-radius: 8px !important;
    letter-spacing: 1px !important;
    transition: all 0.25s ease !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,245,212,0.2) 0%, rgba(0,180,216,0.15) 100%) !important;
    border-color: #00f5d4 !important;
    box-shadow: 0 0 20px rgba(0,245,212,0.3), 0 0 40px rgba(0,245,212,0.1) !important;
    transform: translateY(-1px) !important;
    color: #ffffff !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(0,245,212,0.2) 0%, rgba(0,180,216,0.15) 100%) !important;
    border-color: #00f5d4 !important;
    box-shadow: 0 0 15px rgba(0,245,212,0.2) !important;
}

/* ── TABS ─────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(2,8,24,0.6) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(0,180,216,0.15) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #8f9aa5 !important;
    border-radius: 7px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.5px !important;
    padding: 8px 16px !important;
    border: none !important;
    transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,180,216,0.25), rgba(0,245,212,0.15)) !important;
    color: #00f5d4 !important;
    box-shadow: 0 0 12px rgba(0,245,212,0.2) !important;
}

/* ── SLIDERS ──────────────────────────────────────── */
.stSlider > div > div > div > div { background: #00f5d4 !important; }
.stSlider > div > div { background: rgba(0,180,216,0.2) !important; }

/* ── DATAFRAME ────────────────────────────────────── */
.stDataFrame { border: 1px solid rgba(0,180,216,0.2) !important; border-radius: 8px !important; }

/* ── EXPANDER ─────────────────────────────────────── */
details > summary {
    background: rgba(0,180,216,0.08) !important;
    border: 1px solid rgba(0,180,216,0.2) !important;
    border-radius: 8px !important;
    color: #00b4d8 !important;
    font-family: 'Share Tech Mono', monospace !important;
    padding: 10px 16px !important;
}

/* ── PROGRESS ─────────────────────────────────────── */
.stProgress > div > div > div { background: linear-gradient(90deg, #00b4d8, #00f5d4) !important; border-radius: 4px; }
.stProgress > div > div { background: rgba(0,180,216,0.1) !important; border-radius: 4px; }

/* ── ALERTS ───────────────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: 8px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.82rem !important;
}

/* ── SCROLLBAR ────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #020818; }
::-webkit-scrollbar-thumb { background: rgba(0,180,216,0.4); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #00f5d4; }

/* ── CUSTOM CLASSES ───────────────────────────────── */
.aegis-badge {
    display: inline-block;
    padding: 3px 10px;
    background: rgba(0,245,212,0.1);
    border: 1px solid rgba(0,245,212,0.3);
    border-radius: 20px;
    color: #00f5d4;
    font-size: 0.7rem;
    letter-spacing: 1px;
    font-family: 'Share Tech Mono', monospace;
}
.cipher-output {
    background: rgba(0,245,212,0.04);
    border: 1px solid rgba(0,245,212,0.2);
    border-left: 3px solid #00f5d4;
    border-radius: 8px;
    padding: 16px;
    font-family: 'Share Tech Mono', monospace;
    color: #00f5d4;
    font-size: 0.9rem;
    word-break: break-all;
    line-height: 1.6;
    margin: 10px 0;
}
.stat-row {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 10px 0;
}
.stat-chip {
    padding: 6px 14px;
    background: rgba(0,180,216,0.08);
    border: 1px solid rgba(0,180,216,0.25);
    border-radius: 20px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #8f9aa5;
}
.stat-chip span { color: #00f5d4; }
.section-header {
    padding: 10px 0;
    border-bottom: 1px solid rgba(0,180,216,0.15);
    margin-bottom: 16px;
}
.pulse {
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────────────────
defaults = {
    "authenticated": False,
    "username": "",
    "cached_steps": [],
    "brute_force_attempts": 0,
    "cooldown_until": 0.0,
    "live_input": "",
    "live_shift": 4,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────

def password_strength(pw: str) -> tuple[int, str, str]:
    score = 0
    if len(pw) >= 8:  score += 1
    if len(pw) >= 12: score += 1
    if any(c.isupper() for c in pw): score += 1
    if any(c.islower() for c in pw): score += 1
    if any(c.isdigit() for c in pw): score += 1
    if any(c in string.punctuation for c in pw): score += 1
    if len(pw) >= 16: score += 1
    labels = {0:"CRITICAL",1:"WEAK",2:"WEAK",3:"FAIR",4:"FAIR",5:"STRONG",6:"STRONG",7:"ELITE"}
    colors = {0:"#ff4d4d",1:"#ff6b35",2:"#ff9a3c",3:"#ffd166",4:"#a8d8a8",5:"#06d6a0",6:"#00f5d4",7:"#00f5d4"}
    return score, labels.get(score,"FAIR"), colors.get(score,"#ffd166")


def _pdf_safe(text: str) -> str:
    """Strip/replace characters outside latin-1 (0x00–0xFF) so fpdf's
    built-in Helvetica/Courier fonts never raise FPDFUnicodeEncodingException.
    Common Unicode punctuation is mapped to plain-ASCII equivalents first."""
    replacements = {
        "\u2014": "--",   # em dash  —
        "\u2013": "-",    # en dash  –
        "\u2018": "'",    # left single quote
        "\u2019": "'",    # right single quote
        "\u201c": '"',    # left double quote
        "\u201d": '"',    # right double quote
        "\u2026": "...",  # ellipsis
        "\u00b7": "-",    # middle dot
        "\u2022": "*",    # bullet
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    # Drop anything still outside latin-1
    return text.encode("latin-1", errors="replace").decode("latin-1")


def make_pdf(username, cipher_name, input_text, output_text, extra_info=""):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 180, 216)
    pdf.cell(0, 10, _pdf_safe("AEGIS SOVEREIGN SUITE PRO -- OPERATION RECEIPT"), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_draw_color(0, 180, 216)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    from datetime import datetime
    pdf.cell(0, 6, _pdf_safe(f"Operator: {username}   |   Cipher: {cipher_name}   |   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    if extra_info:
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 6, _pdf_safe(extra_info), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, "INPUT:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 5, _pdf_safe(input_text[:800]))
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, "OUTPUT:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(0, 100, 80)
    pdf.multi_cell(0, 5, _pdf_safe(output_text[:800]))
    return bytes(pdf.output())


def render_entropy_bar(val: float, max_val: float = 8.0):
    pct = min(val / max_val, 1.0)
    if pct < 0.4:   color, label = "#ff6b35", "LOW ENTROPY"
    elif pct < 0.65: color, label = "#ffd166", "MEDIUM ENTROPY"
    else:            color, label = "#00f5d4", "HIGH ENTROPY"
    st.markdown(f"""
    <div style="margin:8px 0;">
      <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
        <span style="font-size:0.75rem;color:#8f9aa5;font-family:'Share Tech Mono',monospace;">SHANNON ENTROPY</span>
        <span style="font-size:0.75rem;font-family:'Share Tech Mono',monospace;color:{color};">{val} / {max_val} — {label}</span>
      </div>
      <div style="background:rgba(0,180,216,0.1);border-radius:4px;height:6px;overflow:hidden;">
        <div style="width:{pct*100:.1f}%;height:100%;background:linear-gradient(90deg,{color},{color}aa);border-radius:4px;transition:width 0.5s ease;"></div>
      </div>
    </div>""", unsafe_allow_html=True)


def render_output_panel(label: str, text: str):
    st.markdown(f'<div class="cipher-output"><span style="color:#8f9aa5;font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;">{label}</span><br><br>{text}</div>', unsafe_allow_html=True)


def render_text_stats(text: str):
    unique = len(set(text))
    alpha  = sum(1 for c in text if c.isalpha())
    digits = sum(1 for c in text if c.isdigit())
    spaces = text.count(" ")
    syms   = len(text) - alpha - digits - spaces
    st.markdown(f"""
    <div class="stat-row">
      <div class="stat-chip">Total Chars: <span>{len(text)}</span></div>
      <div class="stat-chip">Unique: <span>{unique}</span></div>
      <div class="stat-chip">Alpha: <span>{alpha}</span></div>
      <div class="stat-chip">Digits: <span>{digits}</span></div>
      <div class="stat-chip">Spaces: <span>{spaces}</span></div>
      <div class="stat-chip">Symbols: <span>{syms}</span></div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
#  AUTH SCREEN
# ─────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("""
        <div style="text-align:center;padding:30px 0 20px;">
          <div style="font-family:'Orbitron',monospace;font-size:2rem;font-weight:900;
               background:linear-gradient(135deg,#00f5d4,#00b4d8,#8b5cf6);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               text-shadow:none;letter-spacing:4px;">⚡ AEGIS</div>
          <div style="font-family:'Orbitron',monospace;font-size:0.7rem;color:#8f9aa5;
               letter-spacing:6px;margin-top:4px;">SOVEREIGN SUITE PRO v4.0</div>
          <div style="margin-top:12px;font-size:0.75rem;color:#3d5166;font-family:'Share Tech Mono',monospace;">
               FULL-ASCII CRYPTOGRAPHIC COMMAND PLATFORM</div>
        </div>""", unsafe_allow_html=True)

        tab_log, tab_reg = st.tabs(["🔒  AUTHENTICATE", "📋  PROVISION"])

        with tab_log:
            u_in = st.text_input("Operator ID", key="lin_u", placeholder="username")
            p_in = st.text_input("Passkey", type="password", key="lin_p", placeholder="••••••••")

            if p_in:
                sc, lb, col = password_strength(p_in)
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                  <div style="height:3px;border-radius:2px;background:linear-gradient(90deg,{col},{col}66);width:{min(sc/7*100,100):.0f}%;transition:width 0.3s;"></div>
                  <div style="font-size:0.65rem;color:{col};letter-spacing:2px;margin-top:3px;font-family:'Share Tech Mono',monospace;">PASSKEY STRENGTH: {lb}</div>
                </div>""", unsafe_allow_html=True)

            if st.button("⚡  AUTHENTICATE MAINFRAME", type="primary", use_container_width=True):
                users = storage.load_users()
                hp    = hashlib.sha256(p_in.encode()).hexdigest()
                if u_in in users and users[u_in]["password"] == hp:
                    st.session_state.authenticated = True
                    st.session_state.username = u_in
                    st.rerun()
                else:
                    st.error("❌  ACCESS DENIED — Invalid credential signature.")

        with tab_reg:
            r_u = st.text_input("New Operator ID", key="reg_u", placeholder="choose username")
            r_p = st.text_input("Passkey", type="password", key="reg_p", placeholder="choose password")
            if r_p:
                sc, lb, col = password_strength(r_p)
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                  <div style="height:3px;border-radius:2px;background:linear-gradient(90deg,{col},{col}66);width:{min(sc/7*100,100):.0f}%;transition:width 0.3s;"></div>
                  <div style="font-size:0.65rem;color:{col};letter-spacing:2px;margin-top:3px;font-family:'Share Tech Mono',monospace;">STRENGTH: {lb}</div>
                </div>""", unsafe_allow_html=True)
            if st.button("📋  PROVISION OPERATOR", use_container_width=True):
                if r_u and r_p:
                    users = storage.load_users()
                    if r_u in users:
                        st.error("Identity conflict: username already provisioned.")
                    else:
                        users[r_u] = {"password": hashlib.sha256(r_p.encode()).hexdigest()}
                        storage.save_users(users)
                        st.success("✅  Operator provisioned. Switch to AUTHENTICATE.")
                else:
                    st.warning("Fill both fields to provision.")

# ─────────────────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────────────────
else:
    # ── SIDEBAR ──────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:12px 14px;background:linear-gradient(135deg,rgba(0,245,212,0.08),rgba(0,180,216,0.05));
             border:1px solid rgba(0,245,212,0.2);border-radius:10px;margin-bottom:16px;">
          <div style="font-size:0.6rem;color:#8f9aa5;letter-spacing:2px;text-transform:uppercase;">Authenticated Operator</div>
          <div style="font-family:'Orbitron',monospace;color:#00f5d4;font-size:0.95rem;font-weight:700;margin-top:4px;">
            ⚡ {st.session_state.username.upper()}</div>
          <div style="font-size:0.6rem;color:#3d5166;margin-top:4px;letter-spacing:1px;">CLEARANCE LEVEL: SOVEREIGN</div>
        </div>""", unsafe_allow_html=True)

        menu = st.radio("", [
            "📊  TELEMETRY",
            "⚙️  CIPHER LAB",
            "🔐  ADVANCED CIPHERS",
            "💥  CRACK SANDBOX",
            "🔑  HASH & ENCODE",
            "📚  BLUEPRINTS"
        ], label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)

        # Quick stats in sidebar
        hist   = storage.load_history()
        u_hist = [e for e in hist if e.get("username") == st.session_state.username]
        st.markdown(f"""
        <div style="padding:10px 14px;background:rgba(0,0,0,0.3);border:1px solid rgba(0,180,216,0.1);border-radius:8px;margin-bottom:12px;">
          <div style="font-size:0.6rem;color:#8f9aa5;letter-spacing:2px;margin-bottom:8px;">SESSION STATS</div>
          <div style="display:flex;justify-content:space-between;font-size:0.72rem;font-family:'Share Tech Mono',monospace;margin-bottom:4px;">
            <span style="color:#8f9aa5;">Operations</span><span style="color:#00f5d4;">{len(u_hist)}</span>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:0.72rem;font-family:'Share Tech Mono',monospace;">
            <span style="color:#8f9aa5;">Encryptions</span>
            <span style="color:#00f5d4;">{sum(1 for e in u_hist if 'Enc' in e.get('operation',''))}</span>
          </div>
        </div>""", unsafe_allow_html=True)

        if st.button("🔴  TERMINATE SESSION", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    # ════════════════════════════════════════════════════
    #  VIEW 1 — TELEMETRY
    # ════════════════════════════════════════════════════
    if "TELEMETRY" in menu:
        st.markdown("<h1>📊 OPERATIONS TELEMETRY CENTER</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#8f9aa5;font-size:0.8rem;letter-spacing:1px;'>REAL-TIME CRYPTOGRAPHIC ACTIVITY MONITORING & ANALYTICS MATRIX</p>", unsafe_allow_html=True)

        hist   = storage.load_history()
        u_hist = [e for e in hist if e.get("username") == st.session_state.username]

        e_c = sum(1 for e in u_hist if "Enc" in e.get("operation",""))
        d_c = sum(1 for e in u_hist if "Dec" in e.get("operation",""))
        c_c = sum(1 for e in u_hist if "Crack" in e.get("operation","") or "Brute" in e.get("operation",""))
        tot = len(u_hist)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("⚡ ENCRYPTIONS", e_c,  delta=f"+{e_c}" if e_c else None)
        col2.metric("🔓 DECRYPTIONS", d_c,  delta=f"+{d_c}" if d_c else None)
        col3.metric("💥 CRACKS RUN",  c_c,  delta=f"+{c_c}" if c_c else None)
        col4.metric("📦 TOTAL OPS",   tot,  delta=f"+{tot}" if tot else None)

        if u_hist:
            df = pd.DataFrame(u_hist)

            st.markdown("---")
            col_chart, col_pie = st.columns([3, 2])

            with col_chart:
                st.markdown("### 📈 Payload Volume Timeline")
                fig = px.area(df, x="timestamp", y="length", color="operation",
                              title="",
                              labels={"length":"Char Count","timestamp":"Timestamp"},
                              color_discrete_sequence=["#00f5d4","#00b4d8","#8b5cf6","#e76f51","#ffd166","#06d6a0"])
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_family="'Share Tech Mono',monospace",
                    font_color="#8f9aa5",
                    showlegend=True,
                    legend=dict(bgcolor="rgba(0,0,0,0.3)", bordercolor="rgba(0,180,216,0.2)", borderwidth=1)
                )
                fig.update_xaxes(showgrid=False, showline=True, linecolor="rgba(0,180,216,0.2)")
                fig.update_yaxes(showgrid=True, gridcolor="rgba(0,180,216,0.08)")
                st.plotly_chart(fig, use_container_width=True)

            with col_pie:
                st.markdown("### 🥧 Operation Mix")
                op_counts = df["operation"].value_counts().reset_index()
                op_counts.columns = ["Operation","Count"]
                fig2 = px.pie(op_counts, names="Operation", values="Count",
                              color_discrete_sequence=["#00f5d4","#00b4d8","#8b5cf6","#e76f51","#ffd166","#06d6a0","#ff6b35"])
                fig2.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", font_family="monospace", showlegend=True)
                fig2.update_traces(textposition="inside", textinfo="percent+label", hole=0.4)
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown("### 📜 Operation Audit Ledger")
            st.dataframe(
                df[["timestamp","operation","length","shift"]][::-1].rename(columns={
                    "timestamp":"Timestamp","operation":"Operation",
                    "length":"Chars","shift":"Key/Shift"
                }),
                use_container_width=True, hide_index=True
            )

            # Export
            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                st.download_button(
                    "💾  Export Audit Log (JSON)",
                    data=json.dumps(u_hist, indent=2),
                    file_name="aegis_audit_log.json",
                    mime="application/json"
                )
            with col_dl2:
                st.download_button(
                    "📄  Export Audit Log (CSV)",
                    data=df.to_csv(index=False),
                    file_name="aegis_audit_log.csv",
                    mime="text/csv"
                )
        else:
            st.info("🔍  No operations recorded yet. Run cipher operations to populate telemetry.")

    # ════════════════════════════════════════════════════
    #  VIEW 2 — CIPHER LAB (Caesar + Vigenère)
    # ════════════════════════════════════════════════════
    elif "CIPHER LAB" in menu:
        st.markdown("<h1>⚙️ CRYPTOGRAPHIC MUTATION SUITE LAB</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#8f9aa5;font-size:0.75rem;letter-spacing:1px;'>FULL-ASCII ENCRYPTION ENGINE — HANDLES LETTERS · DIGITS · SYMBOLS · SPACES · PUNCTUATION</p>", unsafe_allow_html=True)

        # ── ASCII COVERAGE BADGE ──────────────────────────
        st.markdown("""
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px;">
          <span class="aegis-badge">✓ UPPERCASE</span>
          <span class="aegis-badge">✓ LOWERCASE</span>
          <span class="aegis-badge">✓ DIGITS 0-9</span>
          <span class="aegis-badge">✓ SPACES</span>
          <span class="aegis-badge">✓ !@#$%^&*()</span>
          <span class="aegis-badge">✓ PUNCTUATION</span>
          <span class="aegis-badge">✓ FULL ASCII 32-126</span>
        </div>""", unsafe_allow_html=True)

        cipher_mode = st.selectbox("SELECT CIPHER ENGINE", [
            "Caesar Shift (Modulo-95 Full ASCII)",
            "Vigenère Polyalphabetic (Full ASCII)"
        ])

        # ── INPUT ─────────────────────────────────────────
        input_data = ""
        tab_txt, tab_file, tab_live = st.tabs(["📥  TEXT INPUT", "📂  FILE UPLOAD", "⚡  LIVE PREVIEW"])

        with tab_txt:
            input_data = st.text_area(
                "INPUT PAYLOAD",
                height=130,
                placeholder="Enter text, numbers, symbols, spaces — anything goes!\nExample: Hello World! 123 #@$%",
                key="main_input"
            )

        with tab_file:
            up_file = st.file_uploader("Upload .txt / .docx / .pdf", type=["txt","docx","pdf"])
            if up_file:
                ext = up_file.name.split(".")[-1].lower()
                if ext == "txt":
                    input_data = up_file.read().decode("utf-8", errors="replace")
                    st.success(f"✅  Loaded {len(input_data)} characters from {up_file.name}")
                elif ext == "docx":
                    try:
                        import docx2txt
                        input_data = docx2txt.process(up_file)
                        st.success(f"✅  Extracted {len(input_data)} characters from Word document.")
                    except ImportError:
                        st.error("Run: pip install docx2txt")
                elif ext == "pdf":
                    try:
                        from pypdf import PdfReader
                        reader = PdfReader(up_file)
                        input_data = "\n".join(p.extract_text() or "" for p in reader.pages)
                        st.success(f"✅  Extracted {len(input_data)} characters from PDF.")
                    except ImportError:
                        st.error("Run: pip install pypdf")

        with tab_live:
            st.markdown("<p style='color:#8f9aa5;font-size:0.8rem;'>Type below — see encryption update in real-time as you type.</p>", unsafe_allow_html=True)
            live_text  = st.text_input("LIVE INPUT", placeholder="Type anything...", key="live_rt")
            live_shift = st.slider("LIVE SHIFT", 1, 94, 13, key="live_shift_rt")
            if live_text:
                live_enc, _ = CaesarCipher.encrypt(live_text, live_shift)
                st.markdown(f'<div class="cipher-output">🔒 <strong>ENCRYPTED:</strong> {live_enc}</div>', unsafe_allow_html=True)
                live_dec, _ = CaesarCipher.decrypt(live_enc, live_shift)
                st.markdown(f'<div class="cipher-output" style="border-left-color:#8b5cf6;">🔓 <strong>ROUND-TRIP:</strong> {live_dec}</div>', unsafe_allow_html=True)

        # ── INPUT ANALYSIS ────────────────────────────────
        if input_data:
            ent = calculate_entropy(input_data)
            render_entropy_bar(ent)
            render_text_stats(input_data)

        st.markdown("---")
        res_out = ""

        # ── CAESAR ────────────────────────────────────────
        if "Caesar" in cipher_mode:
            # Initialize the slider's state value BEFORE the widget is created.
            # Streamlit forbids writing to st.session_state[key] once a widget
            # with that key has been instantiated on the page — so the random
            # button only ever sets a separate "pending" key, and we apply it
            # to "caesar_shift" right before the slider renders (safe, since
            # the widget for this key hasn't been instantiated yet this run).
            if "caesar_shift" not in st.session_state:
                st.session_state["caesar_shift"] = 13
            if "_pending_caesar_shift" in st.session_state:
                st.session_state["caesar_shift"] = st.session_state.pop("_pending_caesar_shift")

            col_sl, col_rnd = st.columns([4, 1])
            with col_sl:
                shift = st.slider("SHIFT KEY (1–94)", 1, 94, key="caesar_shift")
            with col_rnd:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🎲 RANDOM", use_container_width=True):
                    import random
                    st.session_state["_pending_caesar_shift"] = random.randint(1, 94)
                    st.rerun()

            # Alphabet map — full printable
            with st.expander("🗺️  Full ASCII Substitution Map (Printable chars 32–126)"):
                from cipher import PRINTABLE_CHARS
                orig   = PRINTABLE_CHARS
                shifted = PRINTABLE_CHARS[shift:] + PRINTABLE_CHARS[:shift]
                chunk = 32
                for i in range(0, len(orig), chunk):
                    row_orig = orig[i:i+chunk]
                    row_shft = shifted[i:i+chunk]
                    st.markdown(
                        f"<div style='font-family:monospace;font-size:0.7rem;line-height:1.8;color:#8f9aa5;'>"
                        f"<span style='color:#8f9aa5;'>IN : </span>"
                        f"<span style='color:#3d5166;'>{' '.join(repr(c)[1:-1] for c in row_orig)}</span><br>"
                        f"<span style='color:#8f9aa5;'>OUT: </span>"
                        f"<span style='color:#00f5d4;'>{' '.join(repr(c)[1:-1] for c in row_shft)}</span>"
                        f"</div>", unsafe_allow_html=True
                    )

            col_enc, col_dec = st.columns(2)
            if col_enc.button("🔒  ENCRYPT", type="primary", use_container_width=True, key="c_enc"):
                if input_data.strip():
                    res_out, steps = CaesarCipher.encrypt(input_data, shift)
                    st.session_state.cached_steps = steps
                    storage.add_history_entry(st.session_state.username, "Caesar Enc", len(input_data), shift)
                else:
                    st.warning("Input is empty.")

            if col_dec.button("🔓  DECRYPT", use_container_width=True, key="c_dec"):
                if input_data.strip():
                    res_out, steps = CaesarCipher.decrypt(input_data, shift)
                    st.session_state.cached_steps = steps
                    storage.add_history_entry(st.session_state.username, "Caesar Dec", len(input_data), shift)
                else:
                    st.warning("Input is empty.")

        # ── VIGENÈRE ──────────────────────────────────────
        elif "Vigenère" in cipher_mode or "Vigen" in cipher_mode:
            raw_key = st.text_input("PASSPHRASE KEY", value="AEGIS", placeholder="Any text — letters, numbers, symbols OK").strip()
            if raw_key:
                v_key = VigenereCipher.derive_crypto_key(raw_key, 32)
                st.markdown(f"""
                <div style="background:rgba(0,0,0,0.3);border:1px solid rgba(139,92,246,0.25);border-radius:8px;padding:10px 14px;margin:8px 0;">
                  <div style="font-size:0.65rem;color:#8f9aa5;letter-spacing:2px;margin-bottom:4px;">DERIVED CRYPTO KEY (SHA-256 KDF)</div>
                  <div style="font-family:'Share Tech Mono',monospace;color:#8b5cf6;font-size:0.8rem;word-break:break-all;">{v_key}</div>
                </div>""", unsafe_allow_html=True)

                col_enc, col_dec = st.columns(2)
                if col_enc.button("🔒  ENCRYPT", type="primary", use_container_width=True, key="v_enc"):
                    if input_data.strip():
                        res_out = VigenereCipher.encrypt(input_data, v_key)
                        st.session_state.cached_steps = []
                        storage.add_history_entry(st.session_state.username, "Vigenere Enc", len(input_data), 0)
                    else:
                        st.warning("Input is empty.")

                if col_dec.button("🔓  DECRYPT", use_container_width=True, key="v_dec"):
                    if input_data.strip():
                        res_out = VigenereCipher.decrypt(input_data, v_key)
                        st.session_state.cached_steps = []
                        storage.add_history_entry(st.session_state.username, "Vigenere Dec", len(input_data), 0)
                    else:
                        st.warning("Input is empty.")

        # ── OUTPUT ────────────────────────────────────────
        if res_out:
            st.markdown("### 📤 OUTPUT")
            render_output_panel("ENCRYPTED / DECRYPTED RESULT", res_out)
            render_entropy_bar(calculate_entropy(res_out))
            render_text_stats(res_out)

            col_dl1, col_dl2, col_dl3 = st.columns(3)
            with col_dl1:
                st.download_button("💾  Download .txt", data=res_out, file_name="aegis_output.txt", mime="text/plain")
            with col_dl2:
                st.download_button("📋  Download .json",
                    data=json.dumps({"input":input_data,"output":res_out,"cipher":cipher_mode}, indent=2),
                    file_name="aegis_output.json", mime="application/json")
            with col_dl3:
                pdf_bytes = make_pdf(st.session_state.username, cipher_mode, input_data, res_out)
                st.download_button("📄  Download PDF", data=pdf_bytes, file_name="aegis_receipt.pdf", mime="application/pdf")

            if st.session_state.cached_steps:
                with st.expander("🧮  Character-by-Character Substitution Table"):
                    df_steps = pd.DataFrame(st.session_state.cached_steps)
                    st.dataframe(df_steps, use_container_width=True, hide_index=True)

    # ════════════════════════════════════════════════════
    #  VIEW 3 — ADVANCED CIPHERS
    # ════════════════════════════════════════════════════
    elif "ADVANCED" in menu:
        st.markdown("<h1>🔐 ADVANCED CIPHER ARSENAL</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#8f9aa5;font-size:0.75rem;letter-spacing:1px;'>ATBASH · ROT13 · XOR · RAIL FENCE · CIPHER COMPARE ENGINE</p>", unsafe_allow_html=True)

        adv_input = st.text_area("INPUT PAYLOAD", height=120,
            placeholder="All character types supported: letters, digits, spaces, symbols, punctuation…",
            key="adv_input")

        if adv_input:
            ent = calculate_entropy(adv_input)
            render_entropy_bar(ent)
            render_text_stats(adv_input)

        st.markdown("---")
        tab_atb, tab_rot, tab_xor, tab_rail, tab_cmp = st.tabs([
            "🪞 ATBASH", "♻️ ROT13", "⊕ XOR", "🚆 RAIL FENCE", "⚡ COMPARE ALL"
        ])

        # ── ATBASH ────────────────────────────────────────
        with tab_atb:
            st.markdown("### 🪞 Atbash Mirror Cipher (Full ASCII)")
            st.markdown("<p style='color:#8f9aa5;font-size:0.8rem;'>Mirrors ASCII values: char at position N → char at position (94-N). Symmetric — same operation encrypts and decrypts. Handles ALL printable characters.</p>", unsafe_allow_html=True)
            if st.button("🪞  APPLY ATBASH (Encrypt = Decrypt)", type="primary", use_container_width=True):
                if adv_input.strip():
                    result = AtbashCipher.process(adv_input)
                    render_output_panel("ATBASH OUTPUT", result)
                    storage.add_history_entry(st.session_state.username, "Atbash", len(adv_input), 0)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button("💾  Download", data=result, file_name="atbash_output.txt", mime="text/plain")
                    rt = AtbashCipher.process(result)
                    st.markdown(f"<div style='font-size:0.75rem;color:#8f9aa5;font-family:monospace;margin-top:8px;'>✓ Round-trip check: {'PASS — identical to input' if rt==adv_input else 'MISMATCH'}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Enter input above.")

        # ── ROT13 ─────────────────────────────────────────
        with tab_rot:
            st.markdown("### ♻️ ROT13 Cipher (Letters Only)")
            st.markdown("<p style='color:#8f9aa5;font-size:0.8rem;'>Rotates letters by 13. Non-letter chars (digits, spaces, symbols) pass through unchanged. Symmetric.</p>", unsafe_allow_html=True)
            if st.button("♻️  APPLY ROT13", type="primary", use_container_width=True):
                if adv_input.strip():
                    result = ROT13Cipher.process(adv_input)
                    render_output_panel("ROT13 OUTPUT", result)
                    storage.add_history_entry(st.session_state.username, "ROT13", len(adv_input), 13)
                    st.download_button("💾  Download", data=result, file_name="rot13_output.txt", mime="text/plain")
                else:
                    st.warning("Enter input above.")

        # ── XOR ───────────────────────────────────────────
        with tab_xor:
            st.markdown("### ⊕ XOR Stream Cipher")
            st.markdown("<p style='color:#8f9aa5;font-size:0.8rem;'>Applies XOR with a repeating key. Symmetric — same key decrypts. Works on all printable chars.</p>", unsafe_allow_html=True)
            xor_key = st.text_input("XOR KEY", value="AEGIS2025", placeholder="Any string key")
            col1, col2 = st.columns(2)
            if col1.button("⊕  XOR ENCRYPT", type="primary", use_container_width=True):
                if adv_input.strip() and xor_key:
                    result = XORCipher.process(adv_input, xor_key)
                    render_output_panel("XOR ENCRYPTED OUTPUT", result)
                    storage.add_history_entry(st.session_state.username, "XOR Enc", len(adv_input), 0)
                    st.download_button("💾  Download", data=result, file_name="xor_encrypted.txt", mime="text/plain")
                else:
                    st.warning("Provide both input and key.")
            if col2.button("⊕  XOR DECRYPT", use_container_width=True):
                if adv_input.strip() and xor_key:
                    result = XORCipher.process(adv_input, xor_key)
                    render_output_panel("XOR DECRYPTED OUTPUT", result)
                    storage.add_history_entry(st.session_state.username, "XOR Dec", len(adv_input), 0)
                    st.download_button("💾  Download", data=result, file_name="xor_decrypted.txt", mime="text/plain")

        # ── RAIL FENCE ────────────────────────────────────
        with tab_rail:
            st.markdown("### 🚆 Rail Fence Transposition Cipher")
            st.markdown("<p style='color:#8f9aa5;font-size:0.8rem;'>Rearranges characters in a zigzag pattern across N rails. Preserves all characters including spaces and symbols.</p>", unsafe_allow_html=True)
            rails = st.slider("NUMBER OF RAILS", 2, 10, 3, key="rf_rails")

            # Visual zigzag demo
            if adv_input:
                demo = adv_input[:20]
                fence_visual = [[] for _ in range(rails)]
                rail, direction = 0, 1
                positions = []
                for i, ch in enumerate(demo):
                    fence_visual[rail].append((i, ch))
                    positions.append(rail)
                    if rail == 0: direction = 1
                    elif rail == rails-1: direction = -1
                    rail += direction

                vis_lines = []
                for r in range(rails):
                    row = [" "] * len(demo)
                    for idx, ch in fence_visual[r]:
                        row[idx] = ch
                    vis_lines.append(f"Rail {r+1}: {''.join(row)}")

                st.markdown(f"<div style='background:rgba(0,0,0,0.3);border:1px solid rgba(0,180,216,0.15);border-radius:8px;padding:12px;font-family:monospace;font-size:0.75rem;color:#8b5cf6;'>{'<br>'.join(vis_lines)}</div>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            if col1.button("🚆  ENCRYPT (Rail Fence)", type="primary", use_container_width=True):
                if adv_input.strip():
                    result = RailFenceCipher.encrypt(adv_input, rails)
                    render_output_panel("RAIL FENCE ENCRYPTED", result)
                    storage.add_history_entry(st.session_state.username, "RailFence Enc", len(adv_input), rails)
                    st.download_button("💾  Download", data=result, file_name="railfence_enc.txt", mime="text/plain")
                else:
                    st.warning("Enter input above.")

            if col2.button("🚆  DECRYPT (Rail Fence)", use_container_width=True):
                if adv_input.strip():
                    result = RailFenceCipher.decrypt(adv_input, rails)
                    render_output_panel("RAIL FENCE DECRYPTED", result)
                    storage.add_history_entry(st.session_state.username, "RailFence Dec", len(adv_input), rails)
                    st.download_button("💾  Download", data=result, file_name="railfence_dec.txt", mime="text/plain")

        # ── COMPARE ALL ───────────────────────────────────
        with tab_cmp:
            st.markdown("### ⚡ Cipher Comparison Engine")
            st.markdown("<p style='color:#8f9aa5;font-size:0.8rem;'>Encrypt your input with ALL ciphers simultaneously — see side-by-side results.</p>", unsafe_allow_html=True)

            cmp_shift = st.slider("Caesar shift for compare", 1, 94, 13, key="cmp_shift")
            cmp_vkey  = st.text_input("Vigenère passphrase for compare", value="AEGIS", key="cmp_vkey")

            if st.button("⚡  COMPARE ALL CIPHERS", type="primary", use_container_width=True):
                if adv_input.strip():
                    results = CipherCompare.compare_all(adv_input, cmp_shift, cmp_vkey)
                    for r in results:
                        ent_val = calculate_entropy(r["Output"])
                        st.markdown(f"""
                        <div style="background:rgba(0,0,0,0.3);border:1px solid rgba(0,180,216,0.15);border-radius:10px;
                             padding:14px;margin-bottom:10px;">
                          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                            <span style="font-family:'Orbitron',monospace;color:#00b4d8;font-size:0.85rem;font-weight:700;">{r['Cipher']}</span>
                            <span class="aegis-badge">Key: {r['Key']}</span>
                            <span class="aegis-badge">Entropy: {ent_val}</span>
                          </div>
                          <div style="font-family:'Share Tech Mono',monospace;color:#00f5d4;font-size:0.8rem;word-break:break-all;">
                            {r['Output'][:120]}{'…' if len(r['Output'])>120 else ''}
                          </div>
                        </div>""", unsafe_allow_html=True)

                    df_cmp = pd.DataFrame(results)
                    st.download_button(
                        "💾  Download Comparison (JSON)",
                        data=json.dumps(results, indent=2),
                        file_name="cipher_comparison.json",
                        mime="application/json"
                    )
                else:
                    st.warning("Enter input above.")

    # ════════════════════════════════════════════════════
    #  VIEW 4 — CRACK SANDBOX
    # ════════════════════════════════════════════════════
    elif "CRACK" in menu:
        st.markdown("<h1>💥 PERMUTATION BRUTE FORCE CRACK SANDBOX</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#8f9aa5;font-size:0.75rem;letter-spacing:1px;'>EXHAUSTIVE KEY-SPACE SEARCH · CHI-SQUARED FITNESS SCORING · ENGLISH LANGUAGE HEURISTICS</p>", unsafe_allow_html=True)

        intercepted = st.text_area("INTERCEPTED CIPHERTEXT", height=120,
            placeholder="Paste ciphertext here — Caesar-encrypted text with unknown shift key…")

        current_time = time.time()
        if current_time < st.session_state.cooldown_until:
            remaining = int(st.session_state.cooldown_until - current_time)
            st.error(f"🛑  WAF LOCKOUT: Rate limit active. Resumes in {remaining}s.")
        else:
            if st.button("💥  LAUNCH BRUTE FORCE SWEEP (All 94 Shift Keys)", type="primary", use_container_width=True):
                st.session_state.brute_force_attempts += 1
                if st.session_state.brute_force_attempts >= 4:
                    st.session_state.cooldown_until = time.time() + 30
                    st.session_state.brute_force_attempts = 0
                    st.error("🚨  RATE LIMIT: WAF lockout activated (30s cooldown).")
                    st.rerun()

                if intercepted.strip():
                    with st.spinner("🔍  Scanning all 94 key offsets…"):
                        possibilities = CaesarCipher.brute_force_crack(intercepted)
                    storage.add_history_entry(st.session_state.username, "Brute Force Crack", len(intercepted), 0)

                    st.success(f"✅  Sweep complete — top {len(possibilities)} candidates ranked by fitness score.")

                    col_res, col_chart = st.columns([3, 2])

                    with col_res:
                        st.markdown("### 🏆 Top Candidates (Chi-Squared Ranked)")
                        df_poss = pd.DataFrame(possibilities)
                        # Highlight top row
                        st.dataframe(df_poss, use_container_width=True, hide_index=True)

                        best = possibilities[0]
                        st.markdown(f"""
                        <div style="margin-top:12px;padding:14px;background:rgba(0,245,212,0.06);
                             border:1px solid rgba(0,245,212,0.3);border-radius:10px;">
                          <div style="font-size:0.65rem;color:#8f9aa5;letter-spacing:2px;margin-bottom:6px;">BEST CANDIDATE</div>
                          <div style="font-family:'Orbitron',monospace;color:#00f5d4;font-size:1.1rem;font-weight:700;">
                            SHIFT KEY: {best['Shift Key']}</div>
                          <div style="font-family:'Share Tech Mono',monospace;color:#c9d1d9;font-size:0.82rem;margin-top:8px;">
                            {best['Decrypted Preview']}</div>
                        </div>""", unsafe_allow_html=True)

                    with col_chart:
                        st.markdown("### 📊 Fitness Score Landscape")
                        fig = go.Figure()
                        shifts  = [r["Shift Key"] for r in possibilities]
                        scores  = [r["Fitness Score"] for r in possibilities]
                        fig.add_trace(go.Scatter(
                            x=shifts, y=scores,
                            mode="markers+lines",
                            marker=dict(color="#00f5d4", size=8, symbol="circle"),
                            line=dict(color="rgba(0,245,212,0.3)", width=1),
                            name="Fitness"
                        ))
                        fig.add_trace(go.Scatter(
                            x=[possibilities[0]["Shift Key"]], y=[possibilities[0]["Fitness Score"]],
                            mode="markers",
                            marker=dict(color="#ffd166", size=14, symbol="star"),
                            name="Best Match"
                        ))
                        fig.update_layout(
                            template="plotly_dark",
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            font_family="monospace",
                            xaxis_title="Shift Key",
                            yaxis_title="Chi-Squared Score (lower=better)",
                            showlegend=True
                        )
                        st.plotly_chart(fig, use_container_width=True)

                        st.markdown("### 📈 Char Frequency Analysis")
                        freq_data = get_character_frequencies(intercepted)
                        if freq_data:
                            df_freq = pd.DataFrame(
                                sorted(freq_data.items(), key=lambda x: -x[1])[:20],
                                columns=["Char","Count"]
                            )
                            fig2 = px.bar(df_freq, x="Char", y="Count",
                                          color="Count",
                                          color_continuous_scale=["#0A192F","#00b4d8","#00f5d4"])
                            fig2.update_layout(
                                template="plotly_dark",
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                font_family="monospace",
                                showlegend=False
                            )
                            st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.warning("Paste ciphertext to crack.")

    # ════════════════════════════════════════════════════
    #  VIEW 5 — HASH & ENCODE
    # ════════════════════════════════════════════════════
    elif "HASH" in menu:
        st.markdown("<h1>🔑 HASH GENERATOR & BASE64 ENCODER</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#8f9aa5;font-size:0.75rem;letter-spacing:1px;'>MD5 · SHA-1 · SHA-256 · SHA-512 · BASE64 ENCODE/DECODE</p>", unsafe_allow_html=True)

        tab_hash, tab_b64, tab_pw = st.tabs(["#  HASH GENERATOR", "📦  BASE64", "🔐  PASSWORD ANALYZER"])

        with tab_hash:
            hash_input = st.text_area("INPUT FOR HASHING", height=100,
                placeholder="Enter any text — letters, digits, symbols, spaces all hashed correctly…")
            if st.button("⚡  GENERATE ALL HASHES", type="primary", use_container_width=True):
                if hash_input:
                    hashes = HashTools.compute(hash_input)
                    storage.add_history_entry(st.session_state.username, "Hash Generate", len(hash_input), 0)
                    for algo, val in hashes.items():
                        color = {"MD5":"#ff6b35","SHA-1":"#ffd166","SHA-256":"#00f5d4","SHA-512":"#8b5cf6"}[algo]
                        st.markdown(f"""
                        <div style="background:rgba(0,0,0,0.3);border:1px solid rgba(0,180,216,0.15);border-radius:8px;
                             padding:12px 16px;margin-bottom:10px;">
                          <div style="font-size:0.65rem;letter-spacing:2px;color:#8f9aa5;margin-bottom:6px;">{algo}</div>
                          <div style="font-family:'Share Tech Mono',monospace;color:{color};font-size:0.8rem;word-break:break-all;">{val}</div>
                        </div>""", unsafe_allow_html=True)
                    st.download_button("💾  Download Hashes (JSON)",
                        data=json.dumps({"input": hash_input, "hashes": hashes}, indent=2),
                        file_name="hashes.json", mime="application/json")
                else:
                    st.warning("Enter text to hash.")

        with tab_b64:
            b64_input = st.text_area("INPUT", height=100,
                placeholder="Supports ALL characters — letters, numbers, symbols, spaces, unicode…")
            col1, col2 = st.columns(2)
            if col1.button("📦  BASE64 ENCODE", type="primary", use_container_width=True):
                if b64_input:
                    result = Base64Tools.encode(b64_input)
                    render_output_panel("BASE64 ENCODED", result)
                    storage.add_history_entry(st.session_state.username, "Base64 Enc", len(b64_input), 0)
                    st.download_button("💾  Download", data=result, file_name="base64_encoded.txt", mime="text/plain")
                else:
                    st.warning("Enter text.")
            if col2.button("📦  BASE64 DECODE", use_container_width=True):
                if b64_input:
                    result = Base64Tools.decode(b64_input)
                    render_output_panel("BASE64 DECODED", result)
                    storage.add_history_entry(st.session_state.username, "Base64 Dec", len(b64_input), 0)
                    st.download_button("💾  Download", data=result, file_name="base64_decoded.txt", mime="text/plain")
                else:
                    st.warning("Enter text.")

        with tab_pw:
            st.markdown("### 🔐 Password Strength Analyzer")
            pw_test = st.text_input("ENTER PASSWORD TO ANALYZE", type="password",
                placeholder="Test any password — checks length, complexity, character diversity…")
            if pw_test:
                sc, lb, col = password_strength(pw_test)
                st.markdown(f"""
                <div style="padding:20px;background:rgba(0,0,0,0.4);border:1px solid rgba(0,180,216,0.2);border-radius:12px;margin-top:8px;">
                  <div style="text-align:center;font-family:'Orbitron',monospace;font-size:1.5rem;font-weight:900;color:{col};text-shadow:0 0 20px {col}66;margin-bottom:16px;">{lb}</div>
                  <div style="background:rgba(0,180,216,0.1);border-radius:6px;height:10px;margin-bottom:16px;">
                    <div style="width:{min(sc/7*100,100):.0f}%;height:100%;background:linear-gradient(90deg,{col},{col}88);border-radius:6px;transition:width 0.5s;"></div>
                  </div>
                """, unsafe_allow_html=True)

                checks = [
                    ("Length ≥ 8",    len(pw_test) >= 8),
                    ("Length ≥ 12",   len(pw_test) >= 12),
                    ("Length ≥ 16",   len(pw_test) >= 16),
                    ("Uppercase",     any(c.isupper() for c in pw_test)),
                    ("Lowercase",     any(c.islower() for c in pw_test)),
                    ("Digits",        any(c.isdigit() for c in pw_test)),
                    ("Symbols",       any(c in string.punctuation for c in pw_test)),
                ]
                for label, passed in checks:
                    icon  = "✅" if passed else "❌"
                    color = "#00f5d4" if passed else "#ff4d4d"
                    st.markdown(f"<div style='font-family:monospace;font-size:0.8rem;color:{color};padding:2px 0;'>{icon} {label}</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)
                ent = calculate_entropy(pw_test)
                render_entropy_bar(ent)

    # ════════════════════════════════════════════════════
    #  VIEW 6 — BLUEPRINTS
    # ════════════════════════════════════════════════════
    elif "BLUEPRINTS" in menu:
        st.markdown("<h1>📚 MATHEMATICAL INTELLIGENCE BLUEPRINTS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#8f9aa5;font-size:0.75rem;letter-spacing:1px;'>CRYPTOGRAPHIC PRIMITIVES REFERENCE · ALGORITHM DOCUMENTATION · MATHEMATICAL FOUNDATIONS</p>", unsafe_allow_html=True)

        tab_c, tab_v, tab_ent, tab_adv = st.tabs([
            "🔒 CAESAR", "🔑 VIGENÈRE", "🧠 ENTROPY", "⚡ ADVANCED"
        ])

        with tab_c:
            st.markdown("### Caesar Cipher — Modulo-95 Full ASCII")
            st.markdown("<p style='color:#8f9aa5;'>Unlike traditional Caesar (letters only, mod-26), this implementation works across the <strong style='color:#00f5d4;'>full printable ASCII range (chars 32–126)</strong> — encrypting spaces, digits, symbols, and punctuation too.</p>", unsafe_allow_html=True)
            st.code("""# Full ASCII Caesar — handles ALL printable characters
# ASCII 32 = space, ASCII 126 = ~
# Shift range: 1 to 94

def encrypt_char(char, shift):
    if 32 <= ord(char) <= 126:
        return chr(((ord(char) - 32 + shift) % 95) + 32)
    return char  # non-printable: pass through unchanged

# Example:
# 'A' (65) + shift 4 → (65-32+4) % 95 + 32 = 37 + 32 = 69 = 'E'
# '!' (33) + shift 4 → (33-32+4) % 95 + 32 = 5  + 32 = 37 = '%'
# ' ' (32) + shift 4 → (32-32+4) % 95 + 32 = 4  + 32 = 36 = '$'
# '9' (57) + shift 4 → (57-32+4) % 95 + 32 = 29 + 32 = 61 = '='
""", language="python")

        with tab_v:
            st.markdown("### Vigenère Cipher — SHA-256 KDF + Full ASCII")
            st.code("""# 1. Derive cryptographic key from passphrase
import hashlib

def derive_key(passphrase, length):
    hashed = hashlib.sha256(passphrase.encode()).hexdigest()
    PRINTABLE = [chr(i) for i in range(32, 127)]  # 95 chars
    key = ''.join(PRINTABLE[(int(c, 16) * 6) % 95] for c in hashed)
    while len(key) < length:
        hashed = hashlib.sha256((hashed + passphrase).encode()).hexdigest()
        key += ''.join(PRINTABLE[(int(c, 16) * 6) % 95] for c in hashed)
    return key[:length]

# 2. Encrypt with full-ASCII polyalphabetic shift
def encrypt(text, key):
    result, ki = [], 0
    for ch in text:
        if 32 <= ord(ch) <= 126:
            k_shift = ord(key[ki % len(key)]) - 32
            enc = chr(((ord(ch) - 32 + k_shift) % 95) + 32)
            result.append(enc)
            ki += 1
        else:
            result.append(ch)
    return ''.join(result)
""", language="python")

        with tab_ent:
            st.markdown("### Shannon Entropy Analysis")
            st.markdown("<p style='color:#8f9aa5;'>Entropy measures the unpredictability/randomness of a text. Higher entropy = more random = harder to crack without the key.</p>", unsafe_allow_html=True)
            st.code("""import math
from collections import Counter

def shannon_entropy(text):
    total = len(text)
    freq = Counter(text)
    entropy = 0.0
    for count in freq.values():
        p = count / total
        entropy -= p * math.log2(p)
    return round(entropy, 4)

# Interpretation:
# 0.0 - 2.0  →  Very low entropy (repetitive/predictable)
# 2.0 - 4.5  →  Moderate entropy (natural language text)
# 4.5 - 6.5  →  High entropy (compressed or encrypted data)
# 6.5 - 8.0  →  Very high entropy (random/truly encrypted)
""", language="python")

        with tab_adv:
            st.markdown("### Atbash, XOR, Rail Fence")
            st.code("""# ATBASH — Full ASCII mirror
def atbash(char):
    if 32 <= ord(char) <= 126:
        return chr(126 - (ord(char) - 32))  # mirror within range
    return char

# XOR — symmetric stream cipher
def xor_cipher(text, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

# RAIL FENCE — transposition cipher
def rail_fence_encrypt(text, rails):
    fence = [[] for _ in range(rails)]
    rail, direction = 0, 1
    for ch in text:
        fence[rail].append(ch)
        if rail == 0: direction = 1
        elif rail == rails - 1: direction = -1
        rail += direction
    return ''.join(''.join(r) for r in fence)
""", language="python")

            st.markdown("### Chi-Squared Fitness Scoring (Brute Force)")
            st.code("""# English character frequency table
ENGLISH_FREQ = {'E': 12.70, 'T': 9.06, 'A': 8.17, ...}

def english_score(text):
    letters = [c.upper() for c in text if c.isalpha()]
    total = len(letters)
    observed = Counter(letters)
    score = 0.0
    for ch, expected_pct in ENGLISH_FREQ.items():
        expected = (expected_pct / 100) * total
        obs = observed.get(ch, 0)
        score += (obs - expected) ** 2 / expected  # chi-squared
    # Bonus for common English words
    words = re.findall(r'[a-zA-Z]+', text.lower())
    hits = sum(1 for w in words if w in COMMON_WORDS)
    score -= hits * 3  # reward matches
    return score  # lower = more English-like
""", language="python")