"""
Phase 8: Top 30 Rank Improvement - Competitive Intelligence & Targeted Optimization Experiments
"""
import os
import json
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, precision_recall_fscore_support, confusion_matrix
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from scipy.optimize import minimize

CLASSES = [
    'background_binary',
    'eclipsing_binary',
    'flare_star',
    'instrument_glitch',
    'planet',
    'pulsating_star',
    'quiet_star',
    'starspots'
]

def load_data():
    train_stars = pd.read_csv('data/raw/train_stars.csv')
    test_stars = pd.read_csv('data/raw/test_stars.csv')
    y_train = train_stars['label'].values
    train_meta = train_stars
    test_meta = test_stars
    
    oof_lgb = np.load('scratch/phase6_det_oof_lgb.npy')
    oof_hgb = np.load('scratch/phase6_det_oof_hgb.npy')
    oof_cb = np.load('scratch/phase6_det_oof_cb.npy')
    folds = np.load('scratch/phase6_det_fold_assignments.npy')
    
    test_lgb = np.load('scratch/phase6_test_lgb.npy')
    test_hgb = np.load('scratch/phase6_test_hgb.npy')
    test_cb = np.load('scratch/phase6_test_cb.npy')
    
    df_train_feats = pd.read_parquet('data/processed/train_features_v5.parquet')
    df_test_feats = pd.read_parquet('data/processed/test_features_v5.parquet')
    
    return y_train, train_meta, test_meta, oof_lgb, oof_hgb, oof_cb, folds, test_lgb, test_hgb, test_cb, df_train_feats, df_test_feats

def eval_macro_f1(y_true, probs):
    preds = np.array(CLASSES)[np.argmax(probs, axis=1)]
    return f1_score(y_true, preds, labels=CLASSES, average='macro')

def eval_per_fold(y_true, probs, folds):
    fold_scores = []
    for f in range(5):
        mask = (folds == f)
        fold_scores.append(eval_macro_f1(y_true[mask], probs[mask]))
    return fold_scores, np.mean(fold_scores), np.std(fold_scores)

def main():
    print("--- 1. Loading Assets ---")
    y_train, train_meta, test_meta, oof_lgb, oof_hgb, oof_cb, folds, test_lgb, test_hgb, test_cb, df_train_feats, df_test_feats = load_data()
    
    # Baseline: Phase 5 50/40/10
    probs_p5 = 0.50 * oof_lgb + 0.40 * oof_hgb + 0.10 * oof_cb
    p5_f1 = eval_macro_f1(y_train, probs_p5)
    p5_folds, p5_fmean, p5_fstd = eval_per_fold(y_train, probs_p5, folds)
    print(f"Phase 5 Champion Det OOF Macro F1: {p5_f1:.5f} (Fold mean: {p5_fmean:.5f} +/- {p5_fstd:.5f})")
    
    # Baseline: Phase 6/7 45/45/10
    probs_p7 = 0.45 * oof_lgb + 0.45 * oof_hgb + 0.10 * oof_cb
    p7_f1 = eval_macro_f1(y_train, probs_p7)
    p7_folds, p7_fmean, p7_fstd = eval_per_fold(y_train, probs_p7, folds)
    print(f"Phase 6/7 Alternative Det OOF Macro F1: {p7_f1:.5f} (Fold mean: {p7_fmean:.5f} +/- {p7_fstd:.5f})")
    
    print("\n--- 2. Detailed Error Diagnostics & Confusion Analysis ---")
    preds_p5 = np.array(CLASSES)[np.argmax(probs_p5, axis=1)]
    cm = confusion_matrix(y_train, preds_p5, labels=CLASSES)
    cm_df = pd.DataFrame(cm, index=CLASSES, columns=CLASSES)
    
    prec, rec, f1, supp = precision_recall_fscore_support(y_train, preds_p5, labels=CLASSES)
    class_perf = {}
    for i, c in enumerate(CLASSES):
        loss_contrib = (1.0 - f1[i]) / len(CLASSES)
        class_perf[c] = {
            'precision': float(prec[i]),
            'recall': float(rec[i]),
            'f1': float(f1[i]),
            'support': int(supp[i]),
            'loss_contribution': float(loss_contrib)
        }
        print(f"  {c:<20}: F1={f1[i]:.4f}, P={prec[i]:.4f}, R={rec[i]:.4f}, Loss={loss_contrib:.4f}")
    
    # Specific error vectors
    starspots_quiet = cm_df.loc['starspots', 'quiet_star']
    planet_quiet = cm_df.loc['planet', 'quiet_star']
    quiet_starspots = cm_df.loc['quiet_star', 'starspots']
    quiet_planet = cm_df.loc['quiet_star', 'planet']
    bg_eb = cm_df.loc['background_binary', 'eclipsing_binary']
    flare_glitch = cm_df.loc['flare_star', 'instrument_glitch']
    
    print(f"  Confusion starspots -> quiet_star: {starspots_quiet}")
    print(f"  Confusion planet -> quiet_star: {planet_quiet}")
    print(f"  Confusion quiet_star -> starspots: {quiet_starspots}")
    print(f"  Confusion quiet_star -> planet: {quiet_planet}")
    print(f"  Confusion background_binary -> eclipsing_binary: {bg_eb}")
    print(f"  Confusion flare_star -> instrument_glitch: {flare_glitch}")
    
    print("\n--- 3. Targeted Model Diversity Experiments ---")
    results = {}
    
    # Experiment 8.1: Temperature Scaling / Power Ensembling
    print("Testing Power / Temperature Scaling...")
    best_p = 1.0
    best_p_f1 = p5_f1
    for p in [0.7, 0.8, 0.9, 1.1, 1.2, 1.3, 1.5]:
        probs_pow = (oof_lgb**p * 0.50 + oof_hgb**p * 0.40 + oof_cb**p * 0.10)
        probs_pow = probs_pow / np.sum(probs_pow, axis=1, keepdims=True)
        score = eval_macro_f1(y_train, probs_pow)
        if score > best_p_f1:
            best_p_f1 = score
            best_p = p
    folds_p, fmean_p, fstd_p = eval_per_fold(y_train, probs_pow, folds)
    results['power_scaling'] = {
        'best_p': best_p,
        'f1': float(best_p_f1),
        'fold_mean': float(fmean_p),
        'fold_std': float(fstd_p),
        'delta_vs_p5': float(best_p_f1 - p5_f1)
    }
    print(f"  Power Ensembling (p={best_p}): F1={best_p_f1:.5f} (Delta={best_p_f1 - p5_f1:+.5f})")
    
    # Experiment 8.2: Out-Of-Fold Stacking Meta-Learner (Strict Leakage-Free 5-Fold CV)
    print("\nTesting Leakage-Free Out-Of-Fold Stacking (Logistic Regression Meta-Learner)...")
    # Stack features: concatenated probabilities from lgb, hgb, cb (24 features)
    X_meta = np.hstack([oof_lgb, oof_hgb, oof_cb])
    oof_stack_lr = np.zeros_like(oof_lgb)
    test_meta_X = np.hstack([test_lgb, test_hgb, test_cb])
    test_stack_lr = np.zeros_like(test_lgb)
    
    # Map classes to integers 0..7
    label_map = {c: i for i, c in enumerate(CLASSES)}
    y_train_int = np.array([label_map[y] for y in y_train])
    
    for f in range(5):
        val_idx = (folds == f)
        train_idx = ~val_idx
        
        lr_meta = LogisticRegression(C=0.1, max_iter=1000, penalty='l2')
        lr_meta.fit(X_meta[train_idx], y_train_int[train_idx])
        oof_stack_lr[val_idx] = lr_meta.predict_proba(X_meta[val_idx])
        test_stack_lr += lr_meta.predict_proba(test_meta_X) / 5.0
        
    stack_lr_f1 = eval_macro_f1(y_train, oof_stack_lr)
    stack_lr_folds, stack_lr_fmean, stack_lr_fstd = eval_per_fold(y_train, oof_stack_lr, folds)
    results['stacking_logreg'] = {
        'f1': float(stack_lr_f1),
        'fold_mean': float(stack_lr_fmean),
        'fold_std': float(stack_lr_fstd),
        'folds': [float(x) for x in stack_lr_folds],
        'delta_vs_p5': float(stack_lr_f1 - p5_f1)
    }
    print(f"  Stacking LogReg: F1={stack_lr_f1:.5f} (Delta={stack_lr_f1 - p5_f1:+.5f}, Fold mean={stack_lr_fmean:.5f} +/- {stack_lr_fstd:.5f})")
    
    # Experiment 8.3: Stacking with Top Domain Features
    print("\nTesting Stacking LogReg with Top 5 Astro Features (Transit Depth, SNR, MAD, Centroid Disp)...")
    top_cols = ['transit_depth', 'transit_snr', 'flux_mad', 'centroid_disp_max', 'p01']
    available_top = [c for c in top_cols if c in df_train_feats.columns]
    X_top = df_train_feats[available_top].fillna(0).values
    # Standardize
    X_top_std = (X_top - np.mean(X_top, axis=0)) / (np.std(X_top, axis=0) + 1e-8)
    
    X_meta_plus = np.hstack([X_meta, X_top_std])
    oof_stack_plus = np.zeros_like(oof_lgb)
    
    for f in range(5):
        val_idx = (folds == f)
        train_idx = ~val_idx
        
        lr_meta = LogisticRegression(C=0.05, max_iter=1000, penalty='l2')
        lr_meta.fit(X_meta_plus[train_idx], y_train_int[train_idx])
        oof_stack_plus[val_idx] = lr_meta.predict_proba(X_meta_plus[val_idx])
        
    stack_plus_f1 = eval_macro_f1(y_train, oof_stack_plus)
    stack_plus_folds, stack_plus_fmean, stack_plus_fstd = eval_per_fold(y_train, oof_stack_plus, folds)
    results['stacking_with_features'] = {
        'f1': float(stack_plus_f1),
        'fold_mean': float(stack_plus_fmean),
        'fold_std': float(stack_plus_fstd),
        'folds': [float(x) for x in stack_plus_folds],
        'delta_vs_p5': float(stack_plus_f1 - p5_f1)
    }
    print(f"  Stacking + Astro Features: F1={stack_plus_f1:.5f} (Delta={stack_plus_f1 - p5_f1:+.5f})")

    # Experiment 8.4: Rank Averaging
    print("\nTesting Probabilistic Rank Averaging...")
    from scipy.stats import rankdata
    def rank_transform(probs):
        ranked = np.zeros_like(probs)
        for i in range(probs.shape[1]):
            ranked[:, i] = rankdata(probs[:, i]) / probs.shape[0]
        return ranked / np.sum(ranked, axis=1, keepdims=True)
    
    rank_lgb = rank_transform(oof_lgb)
    rank_hgb = rank_transform(oof_hgb)
    rank_cb = rank_transform(oof_cb)
    probs_rank = 0.45 * rank_lgb + 0.45 * rank_hgb + 0.10 * rank_cb
    rank_f1 = eval_macro_f1(y_train, probs_rank)
    rank_folds, rank_fmean, rank_fstd = eval_per_fold(y_train, probs_rank, folds)
    results['rank_averaging'] = {
        'f1': float(rank_f1),
        'fold_mean': float(rank_fmean),
        'fold_std': float(rank_fstd),
        'delta_vs_p5': float(rank_f1 - p5_f1)
    }
    print(f"  Rank Averaging: F1={rank_f1:.5f} (Delta={rank_f1 - p5_f1:+.5f})")

    # Experiment 8.5: Threshold / Multiplier Tuning via Nested Cross Validation
    print("\nTesting Class-Wise Probability Thresholding via Nested 5-Fold CV...")
    # Strict nested CV: for each outer fold f, optimize multipliers on 4 folds, evaluate on holdout fold f
    nested_oof_probs = np.copy(probs_p5)
    outer_fold_scores = []
    
    for outer_f in range(5):
        val_idx = (folds == outer_f)
        train_idx = ~val_idx
        
        # Optimize multipliers on train_idx
        def loss_func(multipliers):
            scaled = probs_p5[train_idx] * multipliers
            preds = np.array(CLASSES)[np.argmax(scaled, axis=1)]
            return -f1_score(y_train[train_idx], preds, labels=CLASSES, average='macro')
        
        res = minimize(loss_func, x0=np.ones(8), method='Nelder-Mead', options={'maxiter': 300})
        best_mult = res.x
        
        # Apply to unseen validation fold
        val_scaled = probs_p5[val_idx] * best_mult
        nested_oof_probs[val_idx] = val_scaled
        f_score = eval_macro_f1(y_train[val_idx], val_scaled)
        outer_fold_scores.append(f_score)
        
    nested_f1 = eval_macro_f1(y_train, nested_oof_probs)
    results['nested_threshold_tuning'] = {
        'f1': float(nested_f1),
        'fold_mean': float(np.mean(outer_fold_scores)),
        'fold_std': float(np.std(outer_fold_scores)),
        'folds': [float(x) for x in outer_fold_scores],
        'delta_vs_p5': float(nested_f1 - p5_f1)
    }
    print(f"  Nested Threshold Tuning: F1={nested_f1:.5f} (Delta={nested_f1 - p5_f1:+.5f})")

    # Experiment 8.6: Optimal Non-Linear Convex Search on Blend Weights
    print("\nTesting Fine-Grained Convex Search on LGB/HGB/CB Weights...")
    best_weights = [0.50, 0.40, 0.10]
    best_blend_f1 = p5_f1
    weight_candidates = [
        [0.50, 0.40, 0.10],
        [0.45, 0.45, 0.10],
        [0.48, 0.44, 0.08],
        [0.46, 0.46, 0.08],
        [0.44, 0.48, 0.08],
        [0.42, 0.50, 0.08],
        [0.40, 0.48, 0.12],
        [0.44, 0.44, 0.12]
    ]
    blend_evals = []
    for w in weight_candidates:
        p = w[0]*oof_lgb + w[1]*oof_hgb + w[2]*oof_cb
        score = eval_macro_f1(y_train, p)
        f_scores, f_mean, f_std = eval_per_fold(y_train, p, folds)
        blend_evals.append({
            'weights': w,
            'f1': float(score),
            'fold_mean': float(f_mean),
            'fold_std': float(f_std),
            'delta': float(score - p5_f1)
        })
        if score > best_blend_f1:
            best_blend_f1 = score
            best_weights = w
            
    results['fine_weight_search'] = {
        'best_weights': best_weights,
        'best_f1': float(best_blend_f1),
        'evals': blend_evals
    }
    print(f"  Best fine weights {best_weights}: F1={best_blend_f1:.5f} (Delta={best_blend_f1 - p5_f1:+.5f})")

    # Summary
    summary = {
        'baselines': {
            'phase5_det_f1': float(p5_f1),
            'phase5_fold_mean': float(p5_fmean),
            'phase5_fold_std': float(p5_fstd),
            'phase5_folds': [float(x) for x in p5_folds],
            'phase7_det_f1': float(p7_f1),
            'phase7_fold_mean': float(p7_fmean),
            'phase7_fold_std': float(p7_fstd),
            'phase7_folds': [float(x) for x in p7_folds]
        },
        'class_performance_p5': class_perf,
        'confusion_hotspots': {
            'starspots_to_quiet': int(starspots_quiet),
            'planet_to_quiet': int(planet_quiet),
            'quiet_to_starspots': int(quiet_starspots),
            'quiet_to_planet': int(quiet_planet),
            'bg_binary_to_eb': int(bg_eb),
            'flare_to_glitch': int(flare_glitch)
        },
        'experiments': results,
        'acceptance_gate': {
            'threshold': 0.0030,
            'best_improvement': float(max([v['delta_vs_p5'] for k, v in results.items() if 'delta_vs_p5' in v] + [best_blend_f1 - p5_f1])),
            'passed': bool(max([v['delta_vs_p5'] for k, v in results.items() if 'delta_vs_p5' in v] + [best_blend_f1 - p5_f1]) >= 0.0030)
        }
    }
    
    with open('scratch/phase8_experiment_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print("\nSaved scratch/phase8_experiment_summary.json successfully.")

if __name__ == '__main__':
    main()
