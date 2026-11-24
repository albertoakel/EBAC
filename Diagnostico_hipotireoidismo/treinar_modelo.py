"""Treina e exporta somente o pipeline final Random Forest do projeto."""
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from src.preprocessing import codificar_binarias

ROOT = Path(__file__).resolve().parent
TRAIN_PATH = ROOT / "data" / "df_treino.csv"
MODEL_PATH = ROOT / "models" / "modelo_hipotireoidismo.joblib"
TARGET = "binaryClass"


def main():
    if not TRAIN_PATH.exists():
        raise FileNotFoundError(f"Base de treinamento não encontrada: {TRAIN_PATH}")

    df = pd.read_csv(TRAIN_PATH)
    if TARGET not in df:
        raise KeyError(f"Variável-alvo {TARGET!r} não encontrada.")
    if df[TARGET].isna().any():
        raise ValueError("A variável-alvo contém valores ausentes.")

    X = df.drop(columns=TARGET).copy()
    y = df[TARGET].astype(int)

    constantes = [c for c in X if X[c].nunique(dropna=False) <= 1]
    X = X.drop(columns=constantes)

    categoricas = [c for c in ["sex", "referral source"] if c in X.columns]
    binarias = [
        c for c in X.columns
        if c not in categoricas and set(X[c].dropna().unique()).issubset({"f", "t"})
    ]
    numericas = [c for c in X.columns if c not in binarias + categoricas]
    classificadas = numericas + binarias + categoricas
    if len(classificadas) != len(set(classificadas)) or set(classificadas) != set(X.columns):
        raise ValueError("Há preditores não classificados ou classificados mais de uma vez.")

    transformador_numerico = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    transformador_binario = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", FunctionTransformer(codificar_binarias, feature_names_out="one-to-one")),
    ])
    transformador_categorico = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])
    preprocessor = ColumnTransformer([
        ("num", transformador_numerico, numericas),
        ("bin", transformador_binario, binarias),
        ("cat", transformador_categorico, categoricas),
    ], remainder="drop")

    modelo = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=300, class_weight="balanced", random_state=42, n_jobs=-1
        )),
    ])
    modelo.fit(X, y)

    artefato = {
        "model": modelo,
        "model_name": "Random Forest",
        "target": TARGET,
        "positive_class": 1,
        "features": X.columns.tolist(),
        "constant_features_removed": constantes,
        "numeric_features": numericas,
        "binary_features": binarias,
        "categorical_features": categoricas,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artefato, MODEL_PATH)
    print("Modelo exportado:", MODEL_PATH)
    print(f"Registros de treinamento: {len(X):,} | Preditores: {X.shape[1]}")


if __name__ == "__main__":
    main()
