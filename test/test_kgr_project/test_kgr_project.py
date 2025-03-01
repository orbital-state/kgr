from kgr.project import KangarooProject
import subprocess


def test_init_kgr_project(tmp_path):
    project = KangarooProject(tmp_path)
    assert project.name == tmp_path.name
    assert project.kgr_folder_path == tmp_path / '.kgr'
    assert project.kgr_folder_path.exists() is False
    assert project.initialize() is True
    assert project.kgr_folder_path.exists() is True
    # finally, test that we cannot initialize the project again
    assert project.initialize() is False

def test_load_manifests(tmp_path):
    project = KangarooProject(tmp_path)
    project.initialize()
    manifest_file = project.kgr_folder_path / "example_manifest.kgr.yaml"
    manifest_file.write_text("kind: example\nspec:\n  foo: bar\n")
    manifests = project.load_manifests()
    assert len(manifests) == 1
    assert manifests[0]["kind"] == "example"
    assert manifests[0]["spec"]["foo"] == "bar"

def test_lint_manifests(tmp_path):
    project = KangarooProject(tmp_path)
    project.initialize()
    manifest_file = project.kgr_folder_path / "example_manifest.kgr.yaml"
    manifest_file.write_text("spec:\n  foo: bar\n")
    manifests = project.load_manifests()
    assert len(manifests) == 1
    errors = project.lint_manifests()
    assert len(errors) == 1
    assert "Missing 'kind' in manifest" in errors[0]

def test_validate_schema(tmp_path):
    project = KangarooProject(tmp_path)
    project.initialize()
    manifest_file = project.kgr_folder_path / "example_manifest.kgr.yaml"
    manifest_file.write_text("kind: example\nspec:\n  foo: bar\n")
    manifests = project.load_manifests()
    assert len(manifests) == 1
    errors = project.validate_schema()  
    assert len(errors) == 0
