import tomllib
from pathlib import Path


def get_version():
    pyproject_path = (
        Path(__file__).parent.parent.parent.parent / "pyproject.toml"
    )
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)
    return pyproject["project"]["version"]
