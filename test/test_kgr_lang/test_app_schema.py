import yaml
from pathlib import Path
from kgr.lang.schema.application_schema import ApplicationSchema


_examples_path = (Path(__file__).parent / "../../examples").resolve()


def test_load_app_schema():
    # Load the schema from examples folder: `../examples/web-app/apps/webapp.kgr.yaml`
    schema_file = _examples_path / "web-app/apps/webapp.kgr.yaml"
    with schema_file.open("r") as f:
        app_manifest = f.read()
        app_manifest_data = yaml.safe_load(app_manifest)
    # Validate the schema
    app_schema = ApplicationSchema()
    errors = app_schema.validate(app_manifest_data)
    assert len(errors) == 0, errors