"""Archived TF-IDF and balanced logistic-regression baseline."""

from collections.abc import Sequence

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def build_baseline(*, random_seed: int = 42) -> Pipeline:
    """Construct the exact feature and classifier settings used in the study."""
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(max_features=5000, ngram_range=(1, 2)),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=random_seed,
                ),
            ),
        ]
    )


def fit_baseline(
    clause_texts: Sequence[str], labels: Sequence[str], *, random_seed: int = 42
) -> Pipeline:
    """Fit and return the archived classical baseline pipeline."""
    model = build_baseline(random_seed=random_seed)
    model.fit(clause_texts, labels)
    return model
