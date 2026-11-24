"""Transformações compartilhadas entre treinamento e inferência."""


def codificar_binarias(X):
    """Converte variáveis binárias textuais ('t'/'f') em 1/0."""
    return (X == "t").astype(int)
