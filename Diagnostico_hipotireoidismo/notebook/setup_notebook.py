from pathlib import Path
import sys


def setup_path():
    """
    Localiza a raiz do projeto a partir da localização deste arquivo
    (notebook/setup_notebook.py) e adiciona a raiz ao sys.path.

    Retorna
    -------
    pathlib.Path
        Caminho absoluto da raiz do projeto.
    """
    notebook_dir = Path(__file__).resolve().parent
    project_root = notebook_dir.parent

    if not (project_root / "src" / "utils.py").is_file():
        raise FileNotFoundError(
            "Não foi possível localizar src/utils.py a partir de "
            f"{notebook_dir}."
        )

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    return project_root
