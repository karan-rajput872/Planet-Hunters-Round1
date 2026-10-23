export interface ClassInfo {
  id: string;
  name: string;
  display: string;
  count: number;
  percentage: number;
  color: string;
  description: string;
  diagnosticMarker: string;
  f1Score: number;
}

export interface MetricCard {
  label: string;
  value: string;
  subtext: string;
  badge?: string;
  type?: 'primary' | 'secondary' | 'neutral';
}

export interface FeaturePillar {
  title: string;
  count: number;
  color: string;
  description: string;
  keyFeatures: string[];
  astrophysicalRationale: string;
}

export interface BenchmarkStep {
  phase: string;
  name: string;
  macroF1: number;
  gain: string;
  description: string;
  isChampion?: boolean;
}

export interface VerificationCheck {
  id: number;
  stage: 'A' | 'B';
  rule: string;
  criteria: string;
  status: 'PASS' | 'BLOCKED' | 'FAIL';
  note: string;
}

export interface DocLink {
  title: string;
  category: string;
  path: string;
  description: string;
  badge: string;
}

export const PLATFORM_INFO = {
  title: "Planet Hunters",
  subtitle: "Find New Worlds in Starlight",
  author: "Priyanshu Karan",
  competition: "ML Challenge Hack4Hack 2026 — Round 1",
  status: "Competition Round 1 Completed • Audited Champion Pipeline",
  repoUrl: "https://github.com/karan-rajput872/Planet-Hunters-Round1",
  liveStreamlitUrl: "https://planet-hunters-round1-3bvwv7d4umhsshfcvsvc8h.streamlit.app/",
  approvedChecksum: "6A378EAE06765A28A39D41A322F47FF25512A43A47827FF4576940282B74330E",
  approvedFile: "submissions/submission_FINAL.csv",
  trainSize: 18000,
  testSize: 7000,
  classesCount: 8,
  featureCount: 88,
  oofF1: 0.6455,
  detectorOofF1: 0.6336,
  problemStatement: "High-precision space telescopes collect continuous photometric time-series observations across thousands of stellar targets. Planet Hunters analyzes stellar light curves to distinguish exoplanet transit signatures from other astronomical phenomena and spacecraft instrumental systematics."
};

export const METRIC_CARDS: MetricCard[] = [
  {
    label: "Standard OOF Macro F1",
    value: "0.6455",
    subtext: "Internal 5-fold cross-validation across 18,000 stars",
    badge: "Champion Offline Metric",
    type: "primary"
  },
  {
    label: "Detector-Channel OOF F1",
    value: "0.6336",
    subtext: "Spatial holdout validating camera generalization",
    badge: "Leakage-Free Gate",
    type: "secondary"
  },
  {
    label: "Training Dataset",
    value: "18,000",
    subtext: "Stellar light curve observations with labels",
    badge: "Class-Balanced Folds",
    type: "neutral"
  },
  {
    label: "Test Target Stars",
    value: "7,000",
    subtext: "Approved test candidate predictions generated",
    badge: "7,001 Rows Verified",
    type: "neutral"
  },
  {
    label: "Classification Categories",
    value: "8",
    subtext: "Astrophysical objects & instrumental glitches",
    badge: "Multi-Class Macro F1",
    type: "neutral"
  }
];

export const TAXONOMY: ClassInfo[] = [
  {
    id: "quiet_star",
    name: "quiet_star",
    display: "Quiet / Constant Star",
    count: 1912,
    percentage: 27.3,
    color: "#647C70", // Sage Green
    description: "Photometrically stable stellar baseline exhibiting only photon Poisson noise and Gaussian instrumental scatter.",
    diagnosticMarker: "Flat flux time-series, near-zero variance, strictly Gaussian histogram.",
    f1Score: 0.646
  },
  {
    id: "starspots",
    name: "starspots",
    display: "Rotational Modulation / Starspots",
    count: 1122,
    percentage: 16.0,
    color: "#7C3AED", // Purple
    description: "Quasi-sinusoidal flux variations driven by dark stellar magnetic active regions rotating across the visible stellar disk.",
    diagnosticMarker: "Broad multi-day sinusoidal oscillation with slowly drifting amplitude and phase.",
    f1Score: 0.612
  },
  {
    id: "planet",
    name: "planet",
    display: "Exoplanetary Transit Signature",
    count: 793,
    percentage: 11.3,
    color: "#2563EB", // Blue
    description: "Periodic, sharp, box-shaped dips in stellar flux caused by an exoplanet transiting across the stellar disk.",
    diagnosticMarker: "Strict geometric periodicity, flat-bottomed ingress/egress, zero centroid pixel shift.",
    f1Score: 0.672
  },
  {
    id: "pulsating_star",
    name: "pulsating_star",
    display: "Stellar Pulsation / Variable Star",
    count: 785,
    percentage: 11.2,
    color: "#059669", // Emerald
    description: "Rapid, coherent intrinsic brightness oscillations caused by physical radial and non-radial acoustic/gravity stellar modes.",
    diagnosticMarker: "High-frequency Fourier spectrum peak, sawtooth or multi-harmonic periodicities.",
    f1Score: 0.684
  },
  {
    id: "instrument_glitch",
    name: "instrument_glitch",
    display: "Instrumental Glitch / Systematic",
    count: 777,
    percentage: 11.1,
    color: "#6B7280", // Slate Grey
    description: "Non-astrophysical artifacts caused by cosmic ray pixel impacts, reaction wheel momentum dumps, or spacecraft jitter.",
    diagnosticMarker: "Single-cadence discontinuities, step-function level shifts, detector-correlated glitches.",
    f1Score: 0.730
  },
  {
    id: "eclipsing_binary",
    name: "eclipsing_binary",
    display: "Eclipsing Binary System",
    count: 685,
    percentage: 9.8,
    color: "#D97706", // Amber
    description: "Gravitationally bound binary star systems exhibiting deep primary and secondary V-shaped eclipses with ellipsoidal variations.",
    diagnosticMarker: "Deep symmetrical flux drops, alternating primary/secondary eclipse depths.",
    f1Score: 0.741
  },
  {
    id: "flare_star",
    name: "flare_star",
    display: "Stellar Flare Eruption",
    count: 505,
    percentage: 7.2,
    color: "#EA580C", // Orange
    description: "Sudden, explosive magnetic reconnection events releasing massive energy, characterized by rapid rise and exponential decay.",
    diagnosticMarker: "Asymmetric impulsive flux surge followed by exponential thermal cooling curve.",
    f1Score: 0.551
  },
  {
    id: "background_binary",
    name: "background_binary",
    display: "Background Blend / False Positive",
    count: 421,
    percentage: 6.0,
    color: "#DC2626", // Red
    description: "Astrophysical false positive where light from a faint background eclipsing binary blends into the primary target star's photometric mask.",
    diagnosticMarker: "In-transit centroid pixel displacement directly correlated with photometric flux minima.",
    f1Score: 0.528
  }
];

export const ENSEMBLE_MODELS = [
  {
    name: "LightGBM Classifier",
    weight: "50%",
    share: 0.50,
    color: "#647C70",
    role: "Primary Gradient Booster",
    details: "Gradient boosting on decision trees with leaf-wise expansion, histogram binning, and fast multi-class log-loss convergence. Primary anchor for exoplanet and eclipsing binary separation."
  },
  {
    name: "HistGradientBoosting Classifier",
    weight: "40%",
    share: 0.40,
    color: "#A58B65",
    role: "Nonlinear Regularizer",
    details: "Scikit-Learn native histogram-based boosting with monotonic constraints and early stopping. Provides regularized probabilistic distributions that soften overconfident margin predictions."
  },
  {
    name: "CatBoost Classifier",
    weight: "10%",
    share: 0.10,
    color: "#475569",
    role: "Symmetric Tree Regularizer",
    details: "Oblivious decision trees preventing overfitting on subtle centroid motion descriptors and statistical quantile ratios. Stabilizes rare-class boundary decisions."
  }
];

export const PIPELINE_STEPS = [
  {
    step: "01",
    title: "Stellar Telemetry Ingestion",
    desc: "Ingestion of raw photometric light curves for 18,000 training stars and 7,000 blind test targets with time, flux, and centroid coordinates."
  },
  {
    step: "02",
    title: "Cotrending & Normalization",
    desc: "Application of common-mode cotrending basis vectors (CBV), 3-sigma outlier clipping, and spline baseline trend removal to isolate true astrophysical signals."
  },
  {
    step: "03",
    title: "88-Feature Extraction",
    desc: "Engineering of 88 astrophysical descriptors across physical summary moments, distribution shapes, transit morphology, and CCD centroid motion."
  },
  {
    step: "04",
    title: "Tri-Ensemble Inference",
    desc: "Weighted probability blending across 5-fold cross-validated LightGBM (50%), HistGradientBoosting (40%), and CatBoost (10%) models."
  },
  {
    step: "05",
    title: "Calibrated Classification",
    desc: "Deterministic argmax probability assignment yielding calibrated multi-class predictions across all 8 astronomical categories."
  }
];

export const FEATURE_PILLARS: FeaturePillar[] = [
  {
    title: "Cotrended Physical Summary Statistics",
    count: 32,
    color: "#647C70",
    description: "Robust statistical summary descriptors derived from cotrended flux light curves.",
    keyFeatures: [
      "Flux median, mean, and trimmed statistics",
      "Robust IQR and percentile spreads (p01, p05, p95, p99)",
      "Inter-quartile to total-range variance ratios",
      "Median Absolute Deviation (MAD) scale estimators"
    ],
    astrophysicalRationale: "Separates quiet constant stars from active rotators and variable stars by isolating true stellar variability from sensor background noise."
  },
  {
    title: "Flux Distribution & Statistical Moments",
    count: 24,
    color: "#A58B65",
    description: "Higher-order probability distribution metrics capturing flux asymmetries.",
    keyFeatures: [
      "Fisher-Pearson flux skewness",
      "Excess kurtosis and heavy-tail markers",
      "Jarque-Bera normality departure scores",
      "Quantile dispersion and variance ratios"
    ],
    astrophysicalRationale: "Transits and eclipses create strongly negative skewness (dips below baseline), whereas stellar flares create distinct positive skewness (spikes above baseline)."
  },
  {
    title: "Temporal Transit Morphology & Dynamics",
    count: 16,
    color: "#2563EB",
    description: "Time-domain autocorrelation and periodicity descriptors isolating orbital transit shapes.",
    keyFeatures: [
      "Autocorrelation function (ACF) decay timescales",
      "Box Least-Squares (BLS) transit depth estimates",
      "Transit ingress/egress duration ratios",
      "Periodic phase-folded U-shape vs. V-shape metrics"
    ],
    astrophysicalRationale: "Critical for distinguishing planetary transits (flat-bottomed U-shape, brief duration) from eclipsing binaries (deep V-shape, dual alternating dips)."
  },
  {
    title: "CCD Centroid Variance & Motion Tracking",
    count: 16,
    color: "#DC2626",
    description: "Spatial centroid motion tracking on the telescope pixel sensor array.",
    keyFeatures: [
      "X and Y centroid coordinate variance",
      "Flux-weighted centroid displacement vectors",
      "In-transit vs. out-of-transit centroid shifts",
      "Aperture pixel mask contamination indicators"
    ],
    astrophysicalRationale: "The definitive diagnostic against background blended binaries: if the optical center of light shifts during a dip, the eclipse originates from a background star, not the target."
  }
];

export const BENCHMARK_PROGRESSION: BenchmarkStep[] = [
  {
    phase: "Phase 1",
    name: "Baseline Random Forest",
    macroF1: 0.4214,
    gain: "Baseline",
    description: "Initial benchmark using raw uncleaned flux statistics. High vulnerability to detector systematics and class imbalance."
  },
  {
    phase: "Phase 2",
    name: "Single LightGBM Model",
    macroF1: 0.4633,
    gain: "+0.0419",
    description: "Gradient boosting with histogram optimization. Improved convergence on majority classes but struggled on rare background binaries."
  },
  {
    phase: "Phase 3",
    name: "Feature Engineering Overhaul",
    macroF1: 0.5180,
    gain: "+0.0547",
    description: "Addition of 48 astrophysical features including skewness, kurtosis, and basic ACF decay metrics."
  },
  {
    phase: "Phase 4",
    name: "Dual Ensemble (LGBM + HGB)",
    macroF1: 0.5915,
    gain: "+0.0735",
    description: "Soft voting ensemble combining LightGBM and HistGradientBoosting. Stabilized decision margins across intermediate classes."
  },
  {
    phase: "Phase 5",
    name: "Tri-Ensemble + Cotrending (Champion)",
    macroF1: 0.6455,
    gain: "+0.0540",
    description: "Approved champion: 88 features with common-mode cotrending, centroid shift metrics, and tri-model weighting (50/40/10).",
    isChampion: true
  }
];

export const VERIFICATION_CHECKS: VerificationCheck[] = [
  {
    id: 1,
    stage: 'A',
    rule: "File Presence",
    criteria: "submission_FINAL.csv exists in submissions/ directory",
    status: 'PASS',
    note: "File exists with valid path"
  },
  {
    id: 2,
    stage: 'A',
    rule: "Readable CSV Format",
    criteria: "Successfully parsed as valid UTF-8 CSV without corruption",
    status: 'PASS',
    note: "Valid UTF-8 encoding verified"
  },
  {
    id: 3,
    stage: 'A',
    rule: "Target Row Count",
    criteria: "Contains exactly 7,000 predictions (7,001 rows including header)",
    status: 'PASS',
    note: "Exactly 7,001 lines verified"
  },
  {
    id: 4,
    stage: 'A',
    rule: "Two-Column Schema",
    criteria: "File schema has exactly 2 columns",
    status: 'PASS',
    note: "Verified 2-column tabular structure"
  },
  {
    id: 5,
    stage: 'A',
    rule: "Header Naming",
    criteria: "Header strictly matches ['id', 'label']",
    status: 'PASS',
    note: "Columns match exact specification"
  },
  {
    id: 6,
    stage: 'A',
    rule: "No Extra Index Columns",
    criteria: "No unformatted index or unnamed columns present",
    status: 'PASS',
    note: "Zero unnamed or index columns"
  },
  {
    id: 7,
    stage: 'A',
    rule: "Zero Null Target IDs",
    criteria: "All 7,000 star IDs are strictly valid non-null strings",
    status: 'PASS',
    note: "0 null or missing IDs"
  },
  {
    id: 8,
    stage: 'A',
    rule: "Unique ID Sequence",
    criteria: "Zero duplicate IDs in test predictions",
    status: 'PASS',
    note: "7,000 distinct unique stellar IDs"
  },
  {
    id: 9,
    stage: 'A',
    rule: "Zero Null Labels",
    criteria: "Zero null, NaN, or infinite prediction values",
    status: 'PASS',
    note: "100% complete prediction labels"
  },
  {
    id: 10,
    stage: 'A',
    rule: "Clean String Tokens",
    criteria: "No empty or whitespace-only prediction strings",
    status: 'PASS',
    note: "Zero whitespace or empty tokens"
  },
  {
    id: 11,
    stage: 'A',
    rule: "Valid Class Vocabulary",
    criteria: "All predictions belong to the 8 permitted astronomical classes",
    status: 'PASS',
    note: "100% vocabulary compliance"
  },
  {
    id: 12,
    stage: 'A',
    rule: "All 8 Classes Represented",
    criteria: "No category dropped (astrophysically balanced predictions)",
    status: 'PASS',
    note: "All 8 classes actively populated"
  },
  {
    id: 13,
    stage: 'B',
    rule: "Target Set ID Match",
    criteria: "Set of predicted IDs matches test_stars.csv exactly",
    status: 'PASS',
    note: "Verified against competition test manifest (100% ID set match)"
  },
  {
    id: 14,
    stage: 'B',
    rule: "Strict Sequence Ordering",
    criteria: "Rows match target test star index order exactly",
    status: 'PASS',
    note: "Deterministic row sequence aligned with test manifest"
  }
];

export const DOCUMENTATION_LINKS: DocLink[] = [
  {
    title: "README & Project Overview",
    category: "Architecture & Quickstart",
    path: "README.md",
    description: "Complete project guide with installation steps, CLI usage, and pipeline reproduction instructions.",
    badge: "Core Doc"
  },
  {
    title: "Technical Engineering Report",
    category: "Methodology & Modeling",
    path: "docs/TECHNICAL_REPORT.md",
    description: "In-depth scientific breakdown of common-mode cotrending, 88-feature derivation, and tri-ensemble design.",
    badge: "Scientific Report"
  },
  {
    title: "Model Evaluation & Error Analysis",
    category: "Diagnostics & Auditing",
    path: "docs/MODEL_EVALUATION.md",
    description: "Detailed per-class F1 metrics, detector-channel holdout analysis, confusion matrix breakdown, and ablation findings.",
    badge: "Evaluation Doc"
  },
  {
    title: "Final Handover & Reproducibility Guide",
    category: "Deployment & Verification",
    path: "docs/FINAL_HANDOVER.md",
    description: "Forensic audit documentation, verification checklists, and deterministic artifact checksum certificates.",
    badge: "Handover Doc"
  },
  {
    title: "Dashboard Documentation",
    category: "Visualization Platform",
    path: "DASHBOARD_README.md",
    description: "Technical reference for the Streamlit intelligence platform, Plotly visualizations, and data loaders.",
    badge: "Dashboard Doc"
  },
  {
    title: "License & Status Certificate",
    category: "Compliance & Governance",
    path: "LICENSE_STATUS.md",
    description: "Official declaration of competition completion, open-source licensing, and submission finalization.",
    badge: "Compliance"
  }
];
