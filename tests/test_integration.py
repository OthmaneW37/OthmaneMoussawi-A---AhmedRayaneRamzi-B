"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D).

Les tests du TP3 vérifient des réponses ; ceux-ci vérifient le démarrage de l'API
et son comportement quand le modèle manque ou tombe en panne.
"""
from pathlib import Path

import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


def test_demarrage_reel_charge_le_modele():
    """D.1 (donné en exemple) : un client ouvert par « with » exécute le lifespan."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_modele_absent_refuse_demarrage(monkeypatch, tmp_path):
    from fastapi.testclient import TestClient

    import predict
    from api.main import app

    predict.charger_modele.cache_clear()
    monkeypatch.setattr(predict, "MODELE", tmp_path / "absent.joblib")
    try:
        with pytest.raises(FileNotFoundError), TestClient(app):
            pass
    finally:
        predict.charger_modele.cache_clear()


@pytest.mark.parametrize("route", ["/health", "/predict"])
def test_modele_retire_repond_503(monkeypatch, route):
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        monkeypatch.delattr(app.state, "classifier")
        reponse = client.get(route) if route == "/health" else client.post(
            route, json={"text": "Livraison soignée"}
        )
    assert reponse.status_code == 503
    assert reponse.json() == {"detail": "Modèle non chargé"}


@pytest.mark.parametrize("erreur", [RuntimeError("bug interne"), ValueError("bug interne")])
def test_panne_modele_repond_500_sans_detail_interne(monkeypatch, erreur):
    from fastapi.testclient import TestClient

    from api.main import app

    class EnPanne:
        def predict(self, texte):
            raise erreur

    with TestClient(app) as client:
        monkeypatch.setattr(app.state, "classifier", EnPanne())
        reponse = client.post("/predict", json={"text": "Livraison soignée"})
    assert reponse.status_code == 500
    assert reponse.json() == {"detail": "Erreur interne du serveur"}
    assert "bug interne" not in reponse.text


def test_classes_inconnues_refusees(monkeypatch):
    import joblib
    from fastapi.testclient import TestClient

    import predict
    from api.main import app

    class ModeleIncompatible:
        classes_ = ["negative", "neutre", "positive"]

    predict.charger_modele.cache_clear()
    monkeypatch.setattr(joblib, "load", lambda chemin: ModeleIncompatible())
    try:
        with pytest.raises(ValueError, match="classes"), TestClient(app):
            pass
    finally:
        predict.charger_modele.cache_clear()
