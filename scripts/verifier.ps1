param([switch]$Detail)

$ErrorActionPreference = 'Stop'
$racineProjet = Split-Path -Parent $PSScriptRoot
$pythonProjet = Join-Path $racineProjet '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonProjet)) {
    throw 'Créer .venv puis installer requirements.txt et requirements-dev.txt (voir README.md).'
}

function Invoke-Etape {
    param([string]$Titre, [string[]]$ArgumentsPython)
    Write-Host "`n$Titre" -ForegroundColor Cyan
    & $pythonProjet -X utf8 @ArgumentsPython
    if ($LASTEXITCODE -ne 0) {
        throw "Échec : $Titre (code $LASTEXITCODE)."
    }
}

Push-Location $racineProjet
try {
    git log --oneline -10
    git status
    Invoke-Etape 'TP1 : diagnostic' @('scripts/check_setup.py')
    Invoke-Etape 'TP2 : données' @('src/make_demo.py')
    Invoke-Etape 'TP2 : entraînement de démonstration' @('src/train.py')
    Invoke-Etape 'TP2 : évaluation' @('src/evaluate.py')
    Invoke-Etape 'TP4 : courbe du seuil' @('src/courbe_seuil.py')
    Invoke-Etape "TP4 : bilan du jeu d'or" @('src/bilan_jeu_or.py')
    Invoke-Etape 'Qualité : ruff' @('-m', 'ruff', 'check', '.')
    Invoke-Etape 'Qualité : mypy' @('-m', 'mypy', 'api')
    Invoke-Etape 'Tous les tests et couverture API' @(
        '-m', 'pytest', '-q', '--cov=api', '--cov-report=term-missing', '--cov-fail-under=95'
    )
    if ($Detail) {
        Invoke-Etape 'Tests détaillés' @('-m', 'pytest', 'tests/', '-v')
        foreach ($fichierTest in @('test_api.py', 'test_limites.py', 'test_jeu_or.py', 'test_client.py')) {
            Invoke-Etape $fichierTest @('-m', 'pytest', "tests/$fichierTest", '-q')
        }
    }
}
finally {
    Pop-Location
}
