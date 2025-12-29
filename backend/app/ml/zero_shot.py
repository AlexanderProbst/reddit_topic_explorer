from typing import List, Dict
from transformers import pipeline
from ..config import settings

_classifier = None

def get_zero_shot():
    global _classifier
    if _classifier is None:
        auth = True if settings.hf_token else None
        _classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            token=settings.hf_token or None,
        )
    return _classifier

def classify(text: str, candidate_labels: List[str]) -> Dict[str, float]:
    clf = get_zero_shot()
    out = clf(text, candidate_labels=candidate_labels, multi_label=True)
    return {lbl: float(score) for lbl, score in zip(out["labels"], out["scores"])}