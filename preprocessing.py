
import pandas as pd
from schema import model_features, categorical_features

def validate_schema(df: pd.DataFrame):
    missing = set(model_features) - set(df.columns)
    if missing:
        raise ValueError(f'Colunas ausentes no dataset: {missing}')

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Validação
    validate_schema(df)

    # Selecionar apenas colunas esperadas
    df = df[model_features]

    # Tratamento categórico (regra congelada)
    if 'CODE_GENDER' in df.columns:
        df['CODE_GENDER'] = (
            df['CODE_GENDER']
            .astype(str)
            .map({'M': 1, 'F': 0})
            .fillna(-1)
        )

    # Garantir numéricos
    for col in df.columns:
        if col != 'CODE_GENDER':
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Tratamento de nulos
    df = df.fillna(0)

    return df
