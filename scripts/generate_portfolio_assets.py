"""
Generate High-Quality Visual Assets for Planet Hunters Portfolio & Repository
"""
import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = Path("assets/portfolio")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set high DPI and aesthetic styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

def generate_project_cover():
    """Generate high-resolution 16:9 project cover image."""
    fig = plt.figure(figsize=(16, 9), dpi=150)
    ax = fig.add_subplot(111)
    
    # Deep space gradient background
    ax.set_facecolor('#070B14')
    fig.patch.set_facecolor('#070B14')
    
    # Generate background star field
    np.random.seed(42)
    n_stars = 350
    sx = np.random.uniform(0, 16, n_stars)
    sy = np.random.uniform(0, 9, n_stars)
    s_sizes = np.random.exponential(1.5, n_stars) + 0.5
    s_alpha = np.random.uniform(0.15, 0.75, n_stars)
    for x, y, s, a in zip(sx, sy, s_sizes, s_alpha):
        ax.scatter(x, y, s=s, color='#E2E8F0', alpha=a, edgecolors='none')
        
    # Subtle nebula glow in background
    gx, gy = np.mgrid[0:16:100j, 0:9:100j]
    g_glow = np.exp(-((gx - 11)**2 / 12 + (gy - 4.5)**2 / 6)) * 0.18
    ax.imshow(g_glow.T, extent=[0, 16, 0, 9], origin='lower', cmap='Purples', alpha=0.35, zorder=1)
    
    # Transit lightcurve waveform in the lower half
    t = np.linspace(1.5, 14.5, 600)
    # Simulated star flux with transit dip and noise
    baseline = 2.8 + 0.05 * np.sin(t * 1.2)
    transit = - 0.75 * np.exp(-((t - 8.0)**2) / 0.18)
    noise = np.random.normal(0, 0.03, len(t))
    flux = baseline + transit + noise
    
    # Plot lightcurve with glow effect
    ax.plot(t, flux, color='#3B82F6', alpha=0.25, lw=5, zorder=3)
    ax.plot(t, flux, color='#60A5FA', alpha=0.6, lw=2.5, zorder=4)
    ax.scatter(t[::3], flux[::3], s=4, color='#93C5FD', alpha=0.7, zorder=5)
    
    # Model transit fit line
    fit_line = baseline + transit
    ax.plot(t, fit_line, color='#F59E0B', lw=2, linestyle='--', alpha=0.85, zorder=6, label='Transit Model BLS Fit')
    
    # Exoplanet silhouette & transit ingress/egress annotations
    planet_circle = patches.Circle((8.0, 2.05), radius=0.22, facecolor='#0F172A', edgecolor='#38BDF8', lw=2, zorder=7)
    ax.add_patch(planet_circle)
    ax.annotate("EXOPLANET TRANSIT INGRESS\nΔF/F = -0.75% | SNR = 18.4", xy=(8.0, 2.05), xytext=(8.0, 0.9),
                arrowprops=dict(facecolor='#38BDF8', shrink=0.08, width=1.5, headwidth=6),
                color='#38BDF8', fontsize=11, fontweight='bold', ha='center', zorder=8,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#0B132B', edgecolor='#1E293B', alpha=0.9))

    # Badge: Hack4Hack 2026
    ax.text(1.5, 7.8, "HACK4HACK 2026  •  ROUND 1 COMPLETED  •  ASTROPHYSICAL ML",
            fontsize=12, fontweight='bold', color='#A855F7',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#1E1B4B', edgecolor='#4C1D95', alpha=0.85))
    
    # Main Title
    ax.text(1.5, 6.7, "PLANET HUNTERS", fontsize=44, fontweight='heavy', color='#F8FAFC',
            family='sans-serif', zorder=10)
    ax.text(1.5, 5.9, "Find New Worlds in Starlight", fontsize=22, fontweight='normal', color='#38BDF8',
            family='sans-serif', zorder=10)
    
    # Subtitle / Description
    desc = ("Autonomous Multiclass Photometric Time-Series Classification\n"
            "5-Fold Heterogeneous Tri-Ensemble (LightGBM + HistGradientBoosting + CatBoost)\n"
            "Detector-Level Cotrending Basis Vectors (CBV) & 88 Physics-Grounded Astrometric Features")
    ax.text(1.5, 4.6, desc, fontsize=12, color='#94A3B8', linespacing=1.6, zorder=10)
    
    # Key Telemetry Cards on right side
    cards = [
        ("0.6336", "DETECTOR OOF F1", "#10B981", "Cross-Camera Generalization"),
        ("0.6455", "STANDARD OOF F1", "#3B82F6", "Stratified 5-Fold Validation"),
        ("88", "ASTRONOMICAL FEATURES", "#8B5CF6", "Transit, Centroid & BLS Vetting"),
        ("18,000", "TRAINING LIGHTCURVES", "#F59E0B", "1,315 Cadence Observational Series")
    ]
    
    card_x = 11.2
    for i, (val, label, col, sub) in enumerate(cards):
        cy = 7.7 - i * 1.25
        rect = patches.FancyBboxPatch((card_x, cy - 0.45), 3.8, 1.05,
                                     boxstyle="round,pad=0.15",
                                     facecolor='#0F172A', edgecolor='#1E293B', lw=1.5, alpha=0.9, zorder=8)
        ax.add_patch(rect)
        ax.text(card_x + 0.3, cy + 0.25, val, fontsize=18, fontweight='bold', color=col, zorder=9)
        ax.text(card_x + 0.3, cy - 0.05, label, fontsize=9, fontweight='bold', color='#E2E8F0', zorder=9)
        ax.text(card_x + 0.3, cy - 0.3, sub, fontsize=8, color='#64748B', zorder=9)

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    cover_path = OUTPUT_DIR / "project_cover.png"
    plt.tight_layout()
    plt.savefig(cover_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Generated {cover_path}")

def generate_architecture_diagram():
    """Generate professional architecture flow diagram."""
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
    ax.set_facecolor('#0B0F19')
    fig.patch.set_facecolor('#0B0F19')
    
    stages = [
        {"title": "1. Raw Space Photometry", "items": ["1,315 Cadence Flux Array", "2D Millipixel Centroid Track", "Stellar Physical Metadata"], "color": "#2563EB", "x": 1.0},
        {"title": "2. Systematic Cotrending", "items": ["Camera/CCD Median CBV", "Thermal Drift Subtraction", "-60.3% Feature KS Drift"], "color": "#7C3AED", "x": 4.0},
        {"title": "3. Astrophysical Features", "items": ["BLS Transit SNR & Depth", "Centroid In/Out Dip Vetting", "88 Vectorized Descriptors"], "color": "#059669", "x": 7.0},
        {"title": "4. Tri-Model Ensemble", "items": ["LightGBM (50%, 63 leaves)", "HistGradBoost (40%, d=8)", "CatBoost (10%, oblivious)"], "color": "#D97706", "x": 10.0},
        {"title": "5. Evaluation & Output", "items": ["0.6336 Detector OOF F1", "14-Point Rule Validator", "7,000 Verified Test Targets"], "color": "#0284C7", "x": 13.0}
    ]
    
    for i, s in enumerate(stages):
        # Card box
        box = patches.FancyBboxPatch((s["x"] - 1.2, 2.0), 2.4, 4.2, boxstyle="round,pad=0.2",
                                    facecolor='#131D2E', edgecolor=s["color"], lw=2, alpha=0.95)
        ax.add_patch(box)
        
        # Header box
        hdr = patches.FancyBboxPatch((s["x"] - 1.2, 5.4), 2.4, 0.8, boxstyle="round,pad=0.1",
                                    facecolor=s["color"], edgecolor=s["color"], alpha=0.85)
        ax.add_patch(hdr)
        ax.text(s["x"], 5.8, s["title"], color='#FFFFFF', fontsize=10, fontweight='bold', ha='center', va='center')
        
        # Bullet items
        for j, item in enumerate(s["items"]):
            ax.text(s["x"], 4.6 - j * 0.9, f"• {item}", color='#CBD5E1', fontsize=9, ha='center', va='center')
            
        # Arrow connecting stages
        if i < len(stages) - 1:
            ax.annotate("", xy=(s["x"] + 1.6, 4.1), xytext=(s["x"] + 1.2, 4.1),
                        arrowprops=dict(facecolor='#64748B', edgecolor='#64748B', width=2, headwidth=8, headlength=6))

    ax.text(7.5, 7.3, "END-TO-END MACHINE LEARNING ENGINEERING PIPELINE", fontsize=16, fontweight='bold', color='#F8FAFC', ha='center')
    ax.text(7.5, 6.9, "Autonomous Photometric Preprocessing, Systematic Cotrending & Heterogeneous Tree Ensembling", fontsize=11, color='#94A3B8', ha='center')
    
    ax.set_xlim(-0.5, 15.5)
    ax.set_ylim(1.0, 8.0)
    ax.axis('off')
    
    arch_path = OUTPUT_DIR / "architecture_diagram.png"
    plt.tight_layout()
    plt.savefig(arch_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Generated {arch_path}")

def generate_model_comparison():
    """Generate model progression benchmark chart."""
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    ax.set_facecolor('#0B0F19')
    fig.patch.set_facecolor('#0B0F19')
    
    models = [
        "Phase 4 Baseline\n(Uncotrended)",
        "Phase 5 Dual\n(Cotrended)",
        "Phase 5 Tri-Ensemble\n(Champion)",
        "Phase 7 Blend\n(45/45/10)",
        "Phase 8 Power\n(p=1.5)"
    ]
    det_oof = [0.5161, 0.6322, 0.6336, 0.6338, 0.6341]
    colors = ['#EF4444', '#3B82F6', '#10B981', '#6366F1', '#8B5CF6']
    
    bars = ax.bar(models, det_oof, color=colors, width=0.55, edgecolor='#1E293B', linewidth=1.5, zorder=3)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.008,
                f"{height:.4f}", ha='center', va='bottom', color='#F8FAFC', fontweight='bold', fontsize=10)
        
    # Baseline comparison line
    ax.axhline(0.6336, color='#10B981', linestyle=':', alpha=0.6, label='Approved Champion Benchmark (0.6336)')
    ax.axhline(0.6336 + 0.003, color='#F59E0B', linestyle='--', alpha=0.7, label='Acceptance Gate (+0.0030 Threshold)')
    
    ax.set_ylabel("Stratified Detector-Channel OOF Macro F1", color='#E2E8F0', fontsize=11, fontweight='bold')
    ax.set_title("Detector-Channel Cross-Validation Progression Across Development Phases", color='#F8FAFC', fontsize=13, fontweight='bold', pad=15)
    ax.tick_params(colors='#94A3B8', which='both')
    ax.set_ylim(0.45, 0.68)
    ax.grid(axis='y', linestyle='--', alpha=0.15, zorder=0)
    ax.legend(facecolor='#131D2E', edgecolor='#1E293B', labelcolor='#E2E8F0', loc='lower right')
    
    for spine in ax.spines.values():
        spine.set_color('#1E293B')
        
    comp_path = OUTPUT_DIR / "model_comparison.png"
    plt.tight_layout()
    plt.savefig(comp_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Generated {comp_path}")

def generate_experiment_timeline():
    """Generate Phase 1-8 Experiment Timeline graphic."""
    fig, ax = plt.subplots(figsize=(14, 7), dpi=150)
    ax.set_facecolor('#0B0F19')
    fig.patch.set_facecolor('#0B0F19')
    
    phases = [
        {"p": "P1", "name": "Exploratory Baselines", "f1": 0.5512, "decision": "Baseline Established", "status": "Done"},
        {"p": "P2", "name": "Pseudo-Labeling Test", "f1": 0.5480, "decision": "REJECTED (Confirmation Bias)", "status": "Rejected"},
        {"p": "P3", "name": "Dual Ensemble (LGB+HGB)", "f1": 0.5915, "decision": "Promoted to Phase 4", "status": "Promoted"},
        {"p": "P4", "name": "First Full Release", "f1": 0.5161, "decision": "Diagnosed Drift (LB 0.4214)", "status": "Diagnosed"},
        {"p": "P5", "name": "Astro Cotrending + Tri-Ensemble", "f1": 0.6336, "decision": "APPROVED CHAMPION", "status": "Champion"},
        {"p": "P6", "name": "Simplex Weight Search", "f1": 0.6338, "decision": "REJECTED (+0.0002 < Gate)", "status": "Rejected"},
        {"p": "P7", "name": "Error Diagnostics & Stability", "f1": 0.6338, "decision": "REJECTED (Retained P5)", "status": "Rejected"},
        {"p": "P8", "name": "Stacking & Power Ensembling", "f1": 0.6341, "decision": "REJECTED (+0.00046 < Gate)", "status": "Rejected"}
    ]
    
    xs = np.arange(len(phases))
    ys = [p["f1"] for p in phases]
    
    # Line connecting points
    ax.plot(xs, ys, color='#475569', lw=2, linestyle='-', zorder=2)
    
    colors = {
        "Champion": "#10B981",
        "Promoted": "#3B82F6",
        "Done": "#64748B",
        "Diagnosed": "#EF4444",
        "Rejected": "#F59E0B"
    }
    
    for i, p in enumerate(phases):
        col = colors.get(p["status"], "#64748B")
        ax.scatter(xs[i], ys[i], s=160, color=col, edgecolor='#FFFFFF', lw=2, zorder=5)
        
        # Labels
        offset_y = 0.012 if i % 2 == 0 else -0.018
        ax.text(xs[i], ys[i] + offset_y, f"{p['p']}: {p['name']}\n{p['f1']:.4f}\n{p['decision']}",
                fontsize=8.5, ha='center', va='center', color='#F1F5F9',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#131D2E', edgecolor=col, alpha=0.9, lw=1.2),
                zorder=6)
                
    ax.set_title("Development Journey: Eight-Phase Experimental Progression & Decision Milestones", color='#F8FAFC', fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("Detector-Channel OOF Macro F1", color='#E2E8F0', fontsize=11, fontweight='bold')
    ax.set_xticks(xs)
    ax.set_xticklabels([p["p"] for p in phases], color='#94A3B8', fontsize=10, fontweight='bold')
    ax.tick_params(colors='#94A3B8')
    ax.set_ylim(0.48, 0.68)
    ax.grid(axis='y', linestyle='--', alpha=0.15)
    
    for spine in ax.spines.values():
        spine.set_color('#1E293B')
        
    time_path = OUTPUT_DIR / "experiment_timeline.png"
    plt.tight_layout()
    plt.savefig(time_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Generated {time_path}")

def generate_classification_overview():
    """Generate 8-class overview graphic with F1 scores and support."""
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    ax.set_facecolor('#0B0F19')
    fig.patch.set_facecolor('#0B0F19')
    
    classes = [
        ("instrument_glitch", 0.7752, "Sensor cosmic ray / momentum dump", "#10B981", 1721),
        ("pulsating_star", 0.7375, "Periodic acoustic / Fourier modes", "#059669", 1973),
        ("eclipsing_binary", 0.7359, "Deep geometric binary eclipse", "#3B82F6", 2247),
        ("flare_star", 0.6589, "Magnetic reconnection burst", "#6366F1", 1804),
        ("quiet_star", 0.6047, "Gaussian photometric baseline", "#8B5CF6", 3624),
        ("background_binary", 0.5660, "Blended dip with centroid offset", "#F59E0B", 1604),
        ("starspots", 0.5338, "Quasi-periodic rotational modulation", "#F97316", 2882),
        ("planet", 0.4571, "Shallow exoplanetary transit dip", "#EF4444", 2145)
    ]
    
    y_pos = np.arange(len(classes))
    f1_vals = [c[1] for c in classes]
    bar_cols = [c[3] for c in classes]
    labels = [c[0] for c in classes]
    
    bars = ax.barh(y_pos, f1_vals, color=bar_cols, height=0.6, edgecolor='#1E293B', lw=1.2, zorder=3)
    
    for i, bar in enumerate(bars):
        w = bar.get_width()
        desc = classes[i][2]
        supp = classes[i][4]
        ax.text(w + 0.015, bar.get_y() + bar.get_height()/2.,
                f"F1: {w:.4f}  |  Support: {supp:,}  •  {desc}",
                va='center', color='#CBD5E1', fontsize=9, fontweight='500')
                
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, color='#F8FAFC', fontsize=10, fontweight='bold')
    ax.invert_yaxis()
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("Class-Specific Out-of-Fold F1 Score (Approved Champion)", color='#E2E8F0', fontsize=11, fontweight='bold')
    ax.set_title("Eight-Class Astronomical Taxonomy: Empirical Performance & Phenomenological Signatures", color='#F8FAFC', fontsize=12, fontweight='bold', pad=15)
    ax.tick_params(colors='#94A3B8')
    ax.grid(axis='x', linestyle='--', alpha=0.15, zorder=0)
    
    for spine in ax.spines.values():
        spine.set_color('#1E293B')
        
    class_path = OUTPUT_DIR / "classification_overview.png"
    plt.tight_layout()
    plt.savefig(class_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Generated {class_path}")

if __name__ == '__main__':
    print("Generating visual assets...")
    generate_project_cover()
    generate_architecture_diagram()
    generate_model_comparison()
    generate_experiment_timeline()
    generate_classification_overview()
    print("All portfolio assets generated successfully!")
