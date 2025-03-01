import os
import yaml
from pathlib import Path

class KangarooProject:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.manifests = []

    def load_manifests(self):
        kgr_folder = self.project_path / ".kgr"
        if not kgr_folder.exists():
            raise FileNotFoundError(f"{kgr_folder} does not exist")
        
        for yaml_file in kgr_folder.glob("*.kgr.yaml"):
            with open(yaml_file, 'r') as file:
                manifest = yaml.safe_load(file)
                self.manifests.append(manifest)

    def lint_manifests(self):
        errors = []
        for manifest in self.manifests:
            if 'kind' not in manifest:
                errors.append("Missing 'kind' in manifest")
            # Add more linting rules as needed
        return errors

    def validate_schema(self):
        # Placeholder for schema validation logic
        # This should use a schema validation library like jsonschema
        pass

# Example usage:
# project = KangarooProject("/path/to/project")
# project.load_manifests()
# lint_errors = project.lint_manifests()
# if lint_errors:
#     print("Lint errors found:", lint_errors)
# project.validate_schema()
