"""Contrats d'entrée et de sortie de l'API (Pydantic v2)."""
from typing import Literal, TypedDict

from pydantic import BaseModel, Field, field_validator

ApiLabel = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]


class ApiPrediction(TypedDict):
    label: ApiLabel
    score: float
    text: str


class PredictRequest(BaseModel):
    """Requête de prédiction."""
    text: str = Field(..., min_length=1, max_length=2000, description="Texte à classifier",
                      examples=["Livraison rapide, produit conforme, très satisfait"])

    @field_validator("text")
    @classmethod
    def refuser_texte_blanc(cls, texte: str) -> str:
        if not texte.strip():
            raise ValueError("texte vide")
        return texte


class PredictResponse(BaseModel):
    """Réponse de prédiction."""
    label: ApiLabel = Field(..., description="POSITIVE, NEGATIVE ou INDETERMINE sous le seuil d'abstention")
    score: float = Field(..., ge=0, le=1, description="Confiance de la classe prédite")
    text: str = Field(..., description="Aperçu du texte analysé (100 caractères)")


class HealthResponse(BaseModel):
    """Réponse de l'endpoint de santé."""
    status: str = Field(..., description="OK si le modèle est chargé")
    model: str = Field(..., description="Nom du modèle servi")


class ErrorResponse(BaseModel):
    """Format standard des erreurs FastAPI."""
    detail: str
