"""Raccord entre l'API et le modèle entraîné au TP2.

L'API n'entraîne rien et ne connaît pas scikit-learn : elle appelle la fonction
predict() de src/predict.py, qui charge models/sentiment.joblib une seule fois.
"""
import sys
from pathlib import Path

from api.schemas import ApiLabel, ApiPrediction

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))
from predict import ModelLabel, charger_modele  # noqa: E402 (le TP2 expose ses scripts dans src/)
from predict import predict as _predict  # noqa: E402 (même module TP2)

SEUIL_ABSTENTION = 0.60
ETIQUETTES: dict[ModelLabel, ApiLabel] = {"negative": "NEGATIVE", "positive": "POSITIVE"}


class SentimentClassifier:
    """Enveloppe du modèle TP2 avec l'interface attendue par l'API."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        pipeline = charger_modele()  # refuse immédiatement un modèle absent
        if set(pipeline.classes_) != set(ETIQUETTES):
            raise ValueError("classes du modèle incompatibles : negative et positive attendues")

    def predict(self, text: str) -> ApiPrediction:
        """Renvoie le verdict du contrat ; s'abstient sous le seuil de confiance."""
        r = _predict(text)  # lève ValueError si le texte est vide
        label: ApiLabel = "INDETERMINE" if r["score"] < SEUIL_ABSTENTION else ETIQUETTES[r["label"]]
        return {"label": label, "score": r["score"], "text": text[:100]}


def load_model() -> SentimentClassifier:
    """Construit le classifier (le cache de chargement est dans src/predict.py)."""
    return SentimentClassifier()
