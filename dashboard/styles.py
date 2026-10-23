import re
import streamlit as st

def render_html(html_content: str):
    """
    Renders application-controlled HTML safely and cleanly.
    1. Removes all HTML comments.
    2. Strips leading and trailing whitespace from each line (guaranteeing 0 leading spaces).
    3. Drops blank lines to prevent CommonMark from creating indented code blocks.
    4. Prefers native st.html() when supported (Streamlit >= 1.34) to bypass Markdown parsing completely.
    5. Falls back to st.markdown(..., unsafe_allow_html=True) with guaranteed zero-indent HTML lines.
    """
    if not html_content:
        return
    raw = str(html_content)
    # Remove all HTML comments
    no_comments = re.sub(r'<!--.*?-->', '', raw, flags=re.DOTALL)
    # Strip leading/trailing whitespace from each line and discard blank lines
    lines = [line.strip() for line in no_comments.splitlines() if line.strip()]
    if not lines:
        return
    sanitized = "\n".join(lines)

    if hasattr(st, "html"):
        try:
            st.html(sanitized)
            return
        except Exception:
            pass

    st.markdown(sanitized, unsafe_allow_html=True)

def get_theme_css(theme: str = "creamy") -> str:
    """
    Generates unified, high-contrast, professional CSS rules.
    Default and primary visual identity: Warm Creamy / Ivory Scientific Aesthetic.
    """
    # Professional Creamy Palette Tokens
    bg_app = "#F7F4EC"            # Warm Creamy Canvas
    bg_card = "#FFFDF8"           # Luminous Warm Card Background
    bg_card_hover = "#FBF7EE"     # Subtle Card Hover
    bg_surface = "#F0EBDD"        # Secondary Surface / Sidebar
    border_color = "#E7E0D3"      # Delicate Warm Border
    border_subtle = "#EFE9DD"     # Soft Internal Line
    text_primary = "#292D32"      # High-contrast Charcoal
    text_secondary = "#70736F"    # Balanced Warm Grey
    text_muted = "#949692"        # Subdued Grey
    primary_accent = "#647C70"    # Sophisticated Sage Green
    secondary_accent = "#A58B65"  # Warm Bronze / Sand
    highlight_tint = "#EAEFE8"    # Subtle Sage Highlight
    badge_bg = "#EAEFE8"          # Soft Sage Tint
    badge_border = "#D4DFD2"      # Sage Border
    badge_text = "#486254"        # Deep Sage Text
    success_bg = "#EAEFE8"
    success_border = "#C8D7C4"
    success_text = "#3F6350"
    sidebar_bg = "#F3EFE3"
    sidebar_text = "#292D32"
    sidebar_sub = "#70736F"
    sidebar_active_bg = "#EAEFE8"
    sidebar_active_border = "#647C70"
    table_header_bg = "#F0EBDD"
    code_bg = "#EFE9DC"

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ==============================================================================
   0. HIDE DEFAULT STREAMLIT UPPER HEADER, TOOLBAR & COLLAPSE BUTTON
   ============================================================================== */
header,
header[data-testid="stHeader"],
[data-testid="stHeader"],
.stApp > header,
[data-testid="stDecoration"],
[data-testid="stToolbar"],
[data-testid="stStatusWidget"],
#MainMenu,
.stDeployButton,
footer,
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {{
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
    overflow: hidden !important;
    border: none !important;
}}

/* ==============================================================================
   1. GLOBAL BOX-SIZING & ROOT CONTAINER (MINIMIZE TOP WHITESPACE)
   ============================================================================== */
*, *::before, *::after {{
    box-sizing: border-box !important;
}}

html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    color: {text_primary} !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

.stApp {{
    background-color: {bg_app} !important;
    overflow-x: hidden !important;
}}

/* Main container constraints — Minimal top padding to remove excessive whitespace */
.main .block-container {{
    max-width: 1400px !important;
    padding-top: 0.75rem !important;
    padding-bottom: 3.5rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}}

/* Remove default empty element margins */
.main .block-container > div:first-child {{
    margin-top: 0 !important;
    padding-top: 0 !important;
}}

/* ==============================================================================
   2. UNIFIED TYPOGRAPHY HIERARCHY
   ============================================================================== */
h1 {{
    font-family: 'Inter', sans-serif !important;
    font-size: 1.85rem !important; /* ~30px */
    font-weight: 700 !important;
    line-height: 1.25 !important;
    letter-spacing: -0.025em !important;
    color: {text_primary} !important;
    margin-top: 0 !important;
    margin-bottom: 0.35rem !important;
}}

h2 {{
    font-family: 'Inter', sans-serif !important;
    font-size: 1.35rem !important; /* ~21px */
    font-weight: 600 !important;
    line-height: 1.3 !important;
    letter-spacing: -0.015em !important;
    color: {text_primary} !important;
    margin-top: 0 !important;
    margin-bottom: 0.3rem !important;
}}

h3 {{
    font-family: 'Inter', sans-serif !important;
    font-size: 1.05rem !important; /* ~17px */
    font-weight: 600 !important;
    line-height: 1.35 !important;
    color: {text_primary} !important;
    margin-top: 0 !important;
    margin-bottom: 0.25rem !important;
}}

h4, h5, h6 {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important; /* ~15px */
    font-weight: 600 !important;
    color: {text_primary} !important;
    margin: 0 !important;
}}

p, label, input, button, select, textarea {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: {text_secondary};
    font-size: 0.92rem;
    line-height: 1.6;
}}

/* ==============================================================================
   3. SIDEBAR STYLING
   ============================================================================== */
section[data-testid="stSidebar"] {{
    background-color: {sidebar_bg} !important;
    border-right: 1px solid {border_color} !important;
    padding-top: 1.2rem !important;
    width: 285px !important;
    min-width: 250px !important;
}}

section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {{
    display: none !important;
    visibility: hidden !important;
}}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {{
    color: {sidebar_text} !important;
}}

/* Sidebar radio button navigation */
section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {{
    gap: 4px !important;
}}

section[data-testid="stSidebar"] div[data-testid="stRadio"] label {{
    padding: 7px 12px !important;
    border-radius: 6px !important;
    transition: all 0.15s ease !important;
    border: 1px solid transparent !important;
    margin: 0 !important;
    cursor: pointer !important;
}}

section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
    background-color: {sidebar_active_bg} !important;
}}

section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] {{
    background-color: {sidebar_active_bg} !important;
    border: 1px solid {sidebar_active_border} !important;
    font-weight: 600 !important;
}}

section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] span {{
    color: {primary_accent} !important;
    font-weight: 600 !important;
}}

/* ==============================================================================
   4. CARD & CONTAINER SYSTEM
   ============================================================================== */
.ph-card {{
    background-color: {bg_card} !important;
    border: 1px solid {border_color} !important;
    border-radius: 8px !important;
    padding: 18px 22px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 1px 3px rgba(41, 45, 50, 0.03) !important;
    transition: border-color 0.15s ease !important;
    min-width: 0 !important;
    width: 100% !important;
    overflow: hidden !important;
}}

.ph-card:hover {{
    border-color: {secondary_accent}88 !important;
}}

.ph-card-accent {{
    border-left: 3px solid {primary_accent} !important;
}}

/* ==============================================================================
   5. EQUAL-SIZED COMPACT KPI CARDS (BALANCED TYPOGRAPHY)
   ============================================================================== */
.metric-container {{
    background-color: {bg_card} !important;
    border: 1px solid {border_color} !important;
    border-radius: 8px !important;
    padding: 14px 16px !important;
    text-align: left !important;
    min-width: 0 !important;
    width: 100% !important;
    height: 100% !important;
    min-height: 105px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    box-shadow: 0 1px 2px rgba(41, 45, 50, 0.02) !important;
    transition: all 0.15s ease !important;
}}

.metric-container:hover {{
    border-color: {primary_accent}88 !important;
}}

.metric-label {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: {text_secondary} !important;
    margin-bottom: 2px !important;
    line-height: 1.3 !important;
    word-break: normal !important;
    white-space: normal !important;
}}

.metric-value {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.65rem !important; /* ~26px — Compact and professional */
    font-weight: 700 !important;
    color: {text_primary} !important;
    line-height: 1.2 !important;
    margin: 3px 0 !important;
}}

.metric-caption {{
    font-size: 0.74rem !important;
    color: {text_secondary} !important;
    line-height: 1.35 !important;
    margin-top: 1px !important;
}}

/* ==============================================================================
   6. BADGES & STATUS INDICATORS
   ============================================================================== */
.badge-status {{
    display: inline-flex !important;
    align-items: center !important;
    gap: 5px !important;
    padding: 3px 8px !important;
    border-radius: 4px !important;
    font-size: 0.73rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    font-family: 'Inter', sans-serif !important;
    white-space: nowrap !important;
}}

.badge-passed {{
    background-color: {success_bg} !important;
    border: 1px solid {success_border} !important;
    color: {success_text} !important;
}}

.badge-telemetry {{
    background-color: {badge_bg} !important;
    border: 1px solid {badge_border} !important;
    color: {badge_text} !important;
}}

.badge-neutral {{
    background-color: {bg_surface} !important;
    border: 1px solid {border_color} !important;
    color: {text_secondary} !important;
}}

/* ==============================================================================
   7. BUTTONS, TABLES & INPUTS
   ============================================================================== */
.stButton > button {{
    background-color: {primary_accent} !important;
    border: 1px solid {primary_accent} !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    padding: 7px 16px !important;
    border-radius: 6px !important;
    transition: background-color 0.15s ease !important;
    box-shadow: 0 1px 2px rgba(41, 45, 50, 0.04) !important;
}}

.stButton > button:hover {{
    background-color: #53695E !important;
    border-color: #53695E !important;
}}

.stDownloadButton > button {{
    background-color: {bg_card} !important;
    border: 1px solid {border_color} !important;
    color: {text_primary} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    padding: 7px 16px !important;
    border-radius: 6px !important;
    transition: all 0.15s ease !important;
}}

.stDownloadButton > button:hover {{
    border-color: {primary_accent} !important;
    color: {primary_accent} !important;
    background-color: {highlight_tint} !important;
}}

div[data-baseweb="input"] {{
    background-color: {bg_card} !important;
    border: 1px solid {border_color} !important;
    border-radius: 6px !important;
    color: {text_primary} !important;
}}

div[data-baseweb="select"] > div {{
    background-color: {bg_card} !important;
    border: 1px solid {border_color} !important;
    border-radius: 6px !important;
    color: {text_primary} !important;
}}

.ph-code-box {{
    background-color: {code_bg} !important;
    border: 1px solid {border_color} !important;
    border-radius: 6px !important;
    padding: 12px 14px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    color: {text_primary} !important;
    line-height: 1.55 !important;
    overflow-x: auto !important;
}}

div[data-testid="stExpander"] {{
    background-color: {bg_card} !important;
    border: 1px solid {border_color} !important;
    border-radius: 8px !important;
}}

div[data-testid="stExpander"] summary {{
    background-color: {bg_card} !important;
    color: {text_primary} !important;
    border-radius: 8px !important;
}}

div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] summary p {{
    color: {text_primary} !important;
    font-weight: 600 !important;
}}

[data-testid="column"] {{
    min-width: 0 !important;
}}
</style>
"""

# Harmonious, scientific, creamy theme color palette for 8 astrophysical classes
CLASS_PALETTE = {
    "planet": "#4E7A68",             # Sage Green (Exoplanet transit)
    "eclipsing_binary": "#5B7C99",   # Slate Blue (Stellar binary eclipse)
    "background_binary": "#8B7A9E",  # Muted Purple (Astrometric false positive)
    "starspots": "#C49A45",          # Ochre Amber (Rotational modulation)
    "pulsating_star": "#738A58",     # Olive Green (Harmonic pulsations)
    "flare_star": "#B85D43",         # Terracotta Rose (Eruptive reconnection)
    "instrument_glitch": "#8A939E",  # Muted Slate Steel (Hardware glitch)
    "quiet_star": "#A58B65"          # Warm Bronze / Sand (Constant star)
}

def get_class_colors(theme: str = "creamy") -> dict:
    """Returns color dictionary matching the creamy scientific theme."""
    return CLASS_PALETTE

def get_plotly_layout(theme: str = "creamy") -> dict:
    """Returns clean, scientific Plotly layout tokens matching creamy palette."""
    font_color = "#292D32"
    grid_color = "#E7E0D3"
    sub_color = "#70736F"

    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"family": "Inter, sans-serif", "color": font_color, "size": 12},
        "title_font": {"family": "Inter, sans-serif", "size": 14, "color": font_color},
        "xaxis": {
            "gridcolor": grid_color,
            "zerolinecolor": grid_color,
            "tickfont": {"family": "Inter, sans-serif", "color": sub_color, "size": 11},
            "showline": True,
            "linecolor": grid_color
        },
        "yaxis": {
            "gridcolor": grid_color,
            "zerolinecolor": grid_color,
            "tickfont": {"family": "Inter, sans-serif", "color": sub_color, "size": 11},
            "showline": True,
            "linecolor": grid_color
        },
        "margin": {"l": 50, "r": 30, "t": 35, "b": 35}
    }
