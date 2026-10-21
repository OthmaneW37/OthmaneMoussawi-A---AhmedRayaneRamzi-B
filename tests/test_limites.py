"""Tests aux limites du contrat d'entrée (TP4, étape B).

PredictRequest promet un champ « text », chaîne de 1 à 2000 caractères.
Ce fichier vérifie cette promesse à ses frontières, puis au hasard (hypothesis).
"""
import json
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


@pytest.fixture(scope="module")
def client():
    """Portée « module » : l'API démarre une fois pour tout le fichier (hypothesis l'exige)."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as c:  # le « with » exécute le lifespan : le modèle est chargé
        yield c


def en_json(valeur: object) -> bytes:
    """Corps de requête JSON, sous forme d'octets : permet aussi d'envoyer un corps invalide."""
    return json.dumps(valeur).encode("utf-8")


# Le blanc U+0085 est un cas explicite : str.strip() le considère comme vide.
CAS = [
    pytest.param(en_json({"text": ""}), 422, id="texte-vide"),
    pytest.param(en_json({"text": "   "}), 422, id="espaces"),
    pytest.param(en_json({"text": "\u0085"}), 422, id="blanc-unicode"),
    pytest.param(en_json({"text": "a"}), 200, id="un-caractere"),
    pytest.param(en_json({"text": "a" * 2000}), 200, id="2000-caracteres"),
    pytest.param(en_json({"text": "a" * 2001}), 422, id="2001-caracteres"),
    pytest.param(en_json({}), 422, id="champ-absent"),
    pytest.param(en_json({"text": 42}), 422, id="nombre"),
    pytest.param(b"pas du json", 422, id="json-invalide"),
]


@pytest.mark.parametrize("corps, code_attendu", CAS)
def test_frontieres_du_contrat(client, corps, code_attendu):
    reponse = client.post("/predict", content=corps, headers={"Content-Type": "application/json"})
    assert reponse.status_code == code_attendu
    if code_attendu == 422:
        verifier_erreur(reponse.json())
    else:
        verifier_prediction(reponse.json())


def verifier_erreur(corps):
    assert isinstance(corps["detail"], list)
    assert corps["detail"]
    for erreur in corps["detail"]:
        assert {"loc", "msg", "type"} <= erreur.keys()


def verifier_prediction(corps):
    assert corps["label"] in {"POSITIVE", "NEGATIVE", "INDETERMINE"}
    assert 0 <= corps["score"] <= 1


@settings(deadline=None, max_examples=100)
@given(texte=st.text(min_size=1, max_size=2000).filter(lambda texte: bool(texte.strip())))
def test_tout_texte_non_blanc_accepte(client, texte):
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 200
    verifier_prediction(reponse.json())


BLANCS = tuple(chr(code) for code in range(0x110000) if chr(code).isspace())


@settings(deadline=None, max_examples=100)
@given(texte=st.text(alphabet=BLANCS, min_size=1, max_size=2000))
def test_tout_texte_blanc_refuse(client, texte):
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 422
    verifier_erreur(reponse.json())
