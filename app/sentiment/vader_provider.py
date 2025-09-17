from typing import List

try:
    from nltk.sentiment import SentimentIntensityAnalyzer  # type: ignore

    _analyzer = SentimentIntensityAnalyzer()

    def _score(text: str) -> float:
        return _analyzer.polarity_scores(text)["compound"]

except Exception:  # pragma: no cover
    positive_words = {"gain", "rally", "surge", "beat"}
    negative_words = {"drop", "fall", "miss", "loss"}

    def _score(text: str) -> float:
        tokens = text.lower().split()
        score = 0
        for token in tokens:
            if token in positive_words:
                score += 0.5
            if token in negative_words:
                score -= 0.5
        return max(min(score, 1.0), -1.0)


def score_texts(texts: List[str]) -> float:
    if not texts:
        return 0.0
    scores = [_score(text) for text in texts]
    return float(sum(scores) / len(scores))
