"""Frontière du seuil et contrat de sortie de l'adaptateur API."""

import pytest
from pydantic import ValidationError

from api import model
from api.schemas import PredictResponse


@pytest.mark.parametrize(
    "score, attendu", [(0.5999, "INDETERMINE"), (0.6, "POSITIVE"), (0.6001, "POSITIVE")]
)
def test_frontiere_du_seuil(monkeypatch, score, attendu):
    class Pipeline:
        classes_ = ["negative", "positive"]

    monkeypatch.setattr(model, "charger_modele", lambda: Pipeline())
    monkeypatch.setattr(model, "_predict", lambda texte: {"label": "positive", "score": score})
    resultat = model.SentimentClassifier().predict("x" * 150)
    assert resultat == {"label": attendu, "score": score, "text": "x" * 100}


def test_contrat_refuse_une_etiquette_hors_vocabulaire():
    with pytest.raises(ValidationError):
        PredictResponse.model_validate({"label": "NEUTRE", "score": 0.8, "text": "Un avis"})
