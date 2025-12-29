from transformers import pipeline
from ..config import settings

_sent = None

def get_sentiment():
    global _sent
    if _sent is None:
        _sent = pipeline("sentiment-analysis")  # default distilled SST-2
    return _sent

def predict(text: str):
    result = get_sentiment()(text)[0]
    # {'label': 'POSITIVE', 'score': 0.998...}
    return result["label"], float(result["score"])