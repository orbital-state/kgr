import os
import typer
from typing import Dict
from .project import KangarooProject

app = typer.Typer()


def _get_project_path(project_path: str):
    if not project_path:
        project_path = os.getcwd()
        print(f"Project path not provided. Using current directory: {project_path}")
    return project_path

@app.command()
def init(project_path: str = ''):
    """Initialize kangaroo project."""
    project = KangarooProject(_get_project_path(project_path))
    project.load_manifests()
    project.lint_manifests()
    project.initialize()


@app.command()
def run(project_path: str = '', **kwargs):
    """Run kangaroo project."""
    project = KangarooProject(_get_project_path(project_path))
    project.run(**kwargs)

def main():
    app()
