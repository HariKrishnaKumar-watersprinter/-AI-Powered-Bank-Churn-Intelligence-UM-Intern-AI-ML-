import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score
import pandas as pd
def evaluate_thresholds(y_true, y_probs):
    thresholds = np.linspace(0.1, 0.9, 50)

    results = []

    for t in thresholds:
        preds = (y_probs >= t).astype(int)

        results.append({
            "threshold": t,
            "precision": precision_score(y_true, preds),
            "recall": recall_score(y_true, preds),
            "f1": f1_score(y_true, preds)
        })

    return results