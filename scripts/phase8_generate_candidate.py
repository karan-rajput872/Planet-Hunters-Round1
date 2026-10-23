"""
Generate and audit Phase 8 Candidate 01
"""
import hashlib
import numpy as np
import pandas as pd

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

def compute_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest().upper()

def main():
    test_stars = pd.read_csv('data/raw/test_stars.csv')
    test_lgb = np.load('scratch/phase6_test_lgb.npy')
    test_hgb = np.load('scratch/phase6_test_hgb.npy')
    test_cb = np.load('scratch/phase6_test_cb.npy')
    
    # Best experimental model: Power scaled ensemble p=1.5 on 45/45/10
    p = 1.5
    probs_pow = (test_lgb**p * 0.45 + test_hgb**p * 0.45 + test_cb**p * 0.10)
    probs_pow = probs_pow / np.sum(probs_pow, axis=1, keepdims=True)
    
    preds = np.array(CLASSES)[np.argmax(probs_pow, axis=1)]
    
    out_df = pd.DataFrame({
        'id': test_stars['id'],
        'label': preds
    })
    
    out_path = 'submissions/submission_PHASE8_candidate_01.csv'
    out_df.to_csv(out_path, index=False)
    print(f"Generated {out_path} with {len(out_df)} rows.")
    
    cand_sha = compute_sha256(out_path)
    print(f"Candidate SHA-256: {cand_sha}")
    
    final_path = 'submissions/submission_FINAL.csv'
    final_sha = compute_sha256(final_path)
    print(f"Approved Final SHA-256: {final_sha}")
    
    # Comparison
    final_df = pd.read_csv(final_path)
    diff_mask = (out_df['label'] != final_df['label'])
    n_diff = diff_mask.sum()
    pct_diff = (n_diff / len(out_df)) * 100
    print(f"Changed predictions: {n_diff} / {len(out_df)} ({pct_diff:.2f}%)")
    
    cross_tab = pd.crosstab(final_df['label'], out_df['label'], rownames=['Approved Final'], colnames=['Phase 8 Cand'])
    print("\nTransition Matrix (Approved Final -> Phase 8 Candidate):")
    print(cross_tab)
    
    # Per-class distribution
    print("\nPer-class distribution comparison:")
    dist_df = pd.DataFrame({
        'Final_Count': final_df['label'].value_counts(),
        'Final_Pct': final_df['label'].value_counts(normalize=True)*100,
        'Cand_Count': out_df['label'].value_counts(),
        'Cand_Pct': out_df['label'].value_counts(normalize=True)*100
    })
    dist_df['Delta'] = dist_df['Cand_Count'] - dist_df['Final_Count']
    print(dist_df)
    
    # Check detector distribution of changes
    test_stars['changed'] = diff_mask
    print("\nChanges by Camera:")
    print(test_stars.groupby('camera')['changed'].sum())

if __name__ == '__main__':
    main()
