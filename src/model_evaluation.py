import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import f1_score, precision_recall_fscore_support, confusion_matrix, classification_report

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import config

def evaluate_predictions(y_true, y_pred, model_name: str = "Model", save_artifacts: bool = True):
    """
    Evaluates predictions using Macro F1 and per-class metrics.
    Generates classification report and confusion matrix plot.
    """
    macro_f1 = f1_score(y_true, y_pred, average="macro")
    weighted_f1 = f1_score(y_true, y_pred, average="weighted")

    prec, rec, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=config.CLASSES, zero_division=0
    )

    metrics_df = pd.DataFrame({
        "class": config.CLASSES,
        "precision": np.round(prec, 4),
        "recall": np.round(rec, 4),
        "f1": np.round(f1, 4),
        "support": support
    })

    print("\n" + "=" * 60)
    print(f"EVALUATION RESULTS: {model_name}")
    print(f"--> MACRO F1-SCORE: {macro_f1:.4f} <--")
    print(f"--> Weighted F1:    {weighted_f1:.4f}")
    print("=" * 60)
    print(metrics_df.to_string(index=False))

    if save_artifacts:
        # Save classification report text
        clf_rep = classification_report(y_true, y_pred, labels=config.CLASSES, digits=4, zero_division=0)
        report_file = config.REPORTS_DIR / f"classification_report_{model_name.lower().replace(' ', '_')}.txt"
        with open(report_file, "w") as f:
            f.write(f"Model: {model_name}\n")
            f.write(f"Macro F1: {macro_f1:.4f}\n\n")
            f.write(clf_rep)

        # Save confusion matrix plot
        cm = confusion_matrix(y_true, y_pred, labels=config.CLASSES)
        cm_norm = cm.astype('float') / (cm.sum(axis=1)[:, np.newaxis] + 1e-8)

        plt.figure(figsize=(9, 7))
        sns.heatmap(
            cm_norm,
            annot=True,
            fmt=".2f",
            cmap="Blues",
            xticklabels=config.CLASSES,
            yticklabels=config.CLASSES,
            cbar=True
        )
        plt.title(f"Confusion Matrix: {model_name} (Macro F1: {macro_f1:.4f})", fontsize=12, fontweight="bold")
        plt.xlabel("Predicted Class", fontsize=11)
        plt.ylabel("True Class", fontsize=11)
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)
        plt.tight_layout()

        cm_file = config.REPORTS_DIR / f"confusion_matrix_{model_name.lower().replace(' ', '_')}.png"
        plt.savefig(cm_file, dpi=200)
        plt.close()
        print(f"Saved artifacts to {report_file} and {cm_file}")

    return {
        "model": model_name,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "per_class": metrics_df
    }
