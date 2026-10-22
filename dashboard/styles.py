"""
Planet Hunters — Scientific Intelligence Design System
Enterprise SaaS & Scientific Research Platform Aesthetic
Dual Theme Engine: Light (Default) and Dark with Complete Contrast and Typography Guardrails
"""

def get_theme_css(theme: str = "light") -> str:
    """Generates complete, strict CSS rules for Light or Dark theme with bulletproof contrast."""
    is_dark = (theme == "dark")

    if is_dark:
        # Dark Theme Palette (Restrained, deep astronomical navy)
        bg_app = "#0B111E"
        bg_card = "#131D2E"
        bg_card_hover = "#19263C"
        border_color = "#1E2D44"
        border_subtle = "#182438"
        text_primary = "#F1F5F9"
        text_secondary = "#94A3B8"
        text_muted = "#64748B"
        primary_blue = "#3B82F6"
        navy_accent = "#1E293B"
        teal_accent = "#14B8A6"
        badge_bg = "rgba(59, 130, 246, 0.14)"
        badge_border = "rgba(59, 130, 246, 0.3)"
        badge_text = "#60A5FA"
        success_bg = "rgba(16, 185, 129, 0.14)"
        success_border = "rgba(16, 185, 129, 0.3)"
        success_text = "#34D399"
        sidebar_bg = "#0D1524"
        sidebar_text = "#F1F5F9"
        sidebar_sub = "#94A3B8"
        sidebar_active_bg = "rgba(59, 130, 246, 0.16)"
        sidebar_active_border = "#3B82F6"
        table_header_bg = "#182438"
        code_bg = "#080D18"
    else:
        # Light Theme Palette (Default enterprise scientific SaaS)
        bg_app = "#F5F7FA"
        bg_card = "#FFFFFF"
        bg_card_hover = "#F8FAFC"
        border_color = "#E5EAF1"
        border_subtle = "#EDF2F7"
        text_primary = "#172033"
        text_secondary = "#667085"
        text_muted = "#98A2B3"
        primary_blue = "#2457D6"
        navy_accent = "#101B33"
        teal_accent = "#0F9D91"
        badge_bg = "#EEF4FF"
        badge_border = "#C7D7FE"
        badge_text = "#2457D6"
        success_bg = "#ECFDF3"
        success_border = "#ABEFC6"
        success_text = "#067647"
        sidebar_bg = "#FFFFFF"
        sidebar_text = "#172033"
        sidebar_sub = "#667085"
        sidebar_active_bg = "#EEF4FF"
        sidebar_active_border = "#2457D6"
        table_header_bg = "#F8FAFC"
        code_bg = "#F8FAFC"

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

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
   1. GLOBAL BOX-SIZING & ROOT CONTAINER
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

/* Main container constraints */
.main .block-container {{
    max-width: 1440px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 3.5rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}}

/* ==============================================================================
   2. TYPOGRAPHY HIERARCHY
   ============================================================================== */
h1 {{
    font-family: 'Space Grotesk', 'Inter', sans-serif !important;
    font-size: 2.25rem !important; /* 36px */
    font-weight: 800 !important;
    line-height: 1.2 !important;
    letter-spacing: -0.03em !important;
    color: {text_primary} !important;
    margin-top: 0 !important;
    margin-bottom: 0.5rem !important;
}}

h2 {{
    font-family: 'Space Grotesk', 'Inter', sans-serif !important;
    font-size: 1.55rem !important; /* 25px */
    font-weight: 700 !important;
    line-height: 1.25 !important;
    letter-spacing: -0.02em !important;
    color: {text_primary} !important;
    margin-top: 0 !important;
    margin-bottom: 0.4rem !important;
}}

h3 {{
    font-family: 'Space Grotesk', 'Inter', sans-serif !important;
    font-size: 1.2rem !important; /* 19px */
    font-weight: 700 !important;
    line-height: 1.3 !important;
    color: {text_primary} !important;
    margin-top: 0 !important;
    margin-bottom: 0.35rem !important;
}}

h4, h5, h6 {{
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important; /* 16px */
    font-weight: 600 !important;
    color: {text_primary} !important;
    margin: 0 !important;
}}

p, label, input, button, select, textarea {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}

/* Strictly preserve Material Symbols and icon ligatures */
[class*="material-symbols"],
[class*="material-icons"],
[data-testid*="Icon"],
[data-testid="stIconMaterial"],
i.material-icons,
span.material-symbols-rounded {{
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    font-style: normal !important;
    font-variant: normal !important;
    text-transform: none !important;
    letter-spacing: normal !important;
    word-wrap: normal !important;
    white-space: nowrap !important;
    direction: ltr !important;
}}

/* ==============================================================================
   3. SIDEBAR COMPLETE CONTRAST FIX & STYLING
   ============================================================================== */
section[data-testid="stSidebar"] {{
    background-color: {sidebar_bg} !important;
    border-right: 1px solid {border_color} !important;
    padding-top: 1rem !important;
    width: 290px !important;
    min-width: 260px !important;
}}

/* Hide any collapse button inside sidebar */
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {{
    display: none !important;
    visibility: hidden !important;
}}

/* Force text inside sidebar to use proper contrast without breaking icons */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {{
    color: {sidebar_text} !important;
}}

/* Sidebar radio button items */
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
    color: {primary_blue} !important;
    font-weight: 600 !important;
}}

/* ==============================================================================
   4. CARD & CONTAINER SYSTEM
   ============================================================================== */
.ph-card {{
    background-color: {bg_card} !important;
    border: 1px solid {border_color} !important;
    border-radius: 10px !important;
    padding: 20px 24px !important;
    margin-bottom: 24px !important;
    box-shadow: 0 1px 3px rgba(16, 24, 40, 0.04), 0 1px 2px rgba(16, 24, 40, 0.02) !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    min-width: 0 !important;
    width: 100% !important;
    overflow: hidden !important;
}}

.ph-card:hover {{
    border-color: {primary_blue}44 !important;
}}

.ph-card-accent {{
    border-left: 4px solid {primary_blue} !important;
}}

/* ==============================================================================
   5. RESPONSIVE KPI CARD SYSTEM (NO TRUNCATION)
   ============================================================================== */
.metric-container {{
    background-color: {bg_card} !important;
    border: 1px solid {border_color} !important;
    border-radius: 8px !important;
    padding: 16px 18px !important;
    text-align: left !important;
    min-width: 0 !important;
    width: 100% !important;
    height: 100% !important;
    min-height: 110px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    box-shadow: 0 1px 2px rgba(16, 24, 40, 0.03) !important;
    transition: all 0.15s ease !important;
}}

.metric-container:hover {{
    border-color: {primary_blue}66 !important;
    box-shadow: 0 2px 6px rgba(16, 24, 40, 0.06) !important;
}}

.metric-label {{
    font-family: 'Inter', sans-serif !important;
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
    color: {text_secondary} !important;
    margin-bottom: 4px !important;
    line-height: 1.3 !important;
    word-break: normal !important;
    overflow-wrap: break-word !important;
    white-space: normal !important; /* FIX: Never truncate with ellipsis */
}}

.metric-value {{
    font-family: 'JetBrains Mono', "SF Mono", Consolas, monospace !important;
    font-size: 1.8rem !important; /* 29px */
    font-weight: 700 !important;
    color: {text_primary} !important;
    line-height: 1.2 !important;
    margin: 4px 0 !important;
    word-break: normal !important;
    white-space: normal !important; /* FIX: Never truncate values like Macro F1 */
}}

.metric-caption {{
    font-size: 0.76rem !important;
    color: {text_secondary} !important;
    line-height: 1.35 !important;
    margin-top: 2px !important;
    word-break: normal !important;
}}

/* ==============================================================================
   6. BADGES & STATUS INDICATORS
   ============================================================================== */
.badge-status {{
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    padding: 4px 10px !important;
    border-radius: 6px !important;
    font-size: 0.76rem !important;
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
    background-color: {border_subtle} !important;
    border: 1px solid {border_color} !important;
    color: {text_secondary} !important;
}}

/* ==============================================================================
   7. BUTTONS, TABLES & INPUTS
   ============================================================================== */
.stButton > button {{
    background-color: {primary_blue} !important;
    border: 1px solid {primary_blue} !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    padding: 8px 18px !important;
    border-radius: 6px !important;
    transition: background-color 0.15s ease !important;
    box-shadow: 0 1px 2px rgba(16, 24, 40, 0.05) !important;
}}

.stButton > button:hover {{
    background-color: #1E46B8 !important;
    border-color: #1E46B8 !important;
}}

.stDownloadButton > button {{
    background-color: {bg_card} !important;
    border: 1px solid {border_color} !important;
    color: {text_primary} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    padding: 8px 18px !important;
    border-radius: 6px !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 1px 2px rgba(16, 24, 40, 0.03) !important;
}}

.stDownloadButton > button:hover {{
    border-color: {primary_blue} !important;
    color: {primary_blue} !important;
    background-color: {badge_bg} !important;
}}

/* Form elements & inputs */
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

/* Clean Alerts */
.ph-alert-info {{
    background-color: {badge_bg} !important;
    border-left: 3px solid {primary_blue} !important;
    border-radius: 6px !important;
    padding: 12px 16px !important;
    margin: 12px 0 !important;
    font-size: 0.86rem !important;
    color: {text_primary} !important;
    line-height: 1.5 !important;
}}

.ph-alert-success {{
    background-color: {success_bg} !important;
    border-left: 3px solid {success_text} !important;
    border-radius: 6px !important;
    padding: 12px 16px !important;
    margin: 12px 0 !important;
    font-size: 0.86rem !important;
    color: {text_primary} !important;
    line-height: 1.5 !important;
}}

/* Code & formula blocks */
.ph-code-box {{
    background-color: {code_bg} !important;
    border: 1px solid {border_color} !important;
    border-radius: 6px !important;
    padding: 14px 16px !important;
    font-family: 'JetBrains Mono', "SF Mono", Consolas, monospace !important;
    font-size: 0.82rem !important;
    color: {text_primary} !important;
    line-height: 1.6 !important;
    overflow-x: auto !important;
    word-break: normal !important;
    white-space: pre !important;
}}

/* Universal Table & Cell Contrast Protection */
table, tr, td {{
    color: {text_primary} !important;
}}

th {{
    color: {text_secondary} !important;
}}

/* Streamlit Expander Contrast Protection in Light & Dark Themes */
div[data-testid="stExpander"] {{
    background-color: {bg_card} !important;
    border: 1px solid {border_color} !important;
    border-radius: 8px !important;
}}

div[data-testid="stExpander"] details {{
    background-color: transparent !important;
}}

div[data-testid="stExpander"] summary {{
    background-color: {bg_card} !important;
    color: {text_primary} !important;
    border-radius: 8px !important;
}}

div[data-testid="stExpander"] summary:hover {{
    color: {primary_blue} !important;
}}

div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] summary p {{
    color: {text_primary} !important;
    font-weight: 600 !important;
}}

div[data-testid="stExpander"] summary svg {{
    fill: {text_primary} !important;
    color: {text_primary} !important;
}}

div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {{
    background-color: {bg_card} !important;
    color: {text_primary} !important;
}}

/* Column shrink guard */
[data-testid="column"] {{
    min-width: 0 !important;
}}
</style>
"""

# Harmonious Scientific Palette for 8 Classes
CLASS_PALETTE_LIGHT = {
    "pulsating_star": "#7C3AED",      # Violet (27.2%)
    "instrument_glitch": "#DC2626",   # Crimson (19.6%)
    "quiet_star": "#059669",          # Emerald (13.2%)
    "starspots": "#D97706",           # Amber (11.8%)
    "eclipsing_binary": "#0284C7",    # Sky Blue (9.8%)
    "planet": "#1D4ED8",              # Royal Blue (7.4%)
    "flare_star": "#E11D48",          # Coral Rose (6.7%)
    "background_binary": "#6366F1"    # Indigo (4.2%)
}

CLASS_PALETTE_DARK = {
    "pulsating_star": "#A78BFA",
    "instrument_glitch": "#F87171",
    "quiet_star": "#34D399",
    "starspots": "#FBBF24",
    "eclipsing_binary": "#60A5FA",
    "planet": "#38BDF8",
    "flare_star": "#FB7185",
    "background_binary": "#818CF8"
}

def get_class_colors(theme: str = "light") -> dict:
    """Returns color dictionary based on theme."""
    return CLASS_PALETTE_DARK if theme == "dark" else CLASS_PALETTE_LIGHT

def get_plotly_layout(theme: str = "light") -> dict:
    """Returns clean, scientific Plotly layout tokens matching current theme."""
    is_dark = (theme == "dark")

    font_color = "#F1F5F9" if is_dark else "#172033"
    grid_color = "#1E2D44" if is_dark else "#E5EAF1"
    sub_color = "#94A3B8" if is_dark else "#667085"

    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"family": "Inter, sans-serif", "color": font_color, "size": 12},
        "title_font": {"family": "Space Grotesk, sans-serif", "size": 15, "color": font_color},
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
        "margin": {"l": 50, "r": 30, "t": 40, "b": 40}
    }
