import os
import yaml
import toml
from pathlib import Path


class KangarooProject:
    def __init__(self, location_path):
        self._location_path = Path(location_path)
        assert self._location_path.exists()
        self.name = self._location_path.name
        self._config = None
        self.manifests = []

    @property
    def kgr_folder_path(self):
        return self._location_path / '.kgr'
    
    def load_config(self):
        """Load project configuration."""
        if self._config:
            return self._config
        config_path = self.kgr_folder_path / 'config.toml'
        assert config_path.exists(), f"Project configuration not found at: {config_path}"
        # Load configuration from toml file
        self._config = toml.load(config_path)
        return self._config

    def initialize(self) -> bool:
        """Populate `.kgr` folder if it does not exists."""
        if self.kgr_folder_path.exists():
            print(f"Project '{self.name}' already initialized.")
            return False
        # Create '.kgr' folder if it does not exist
        print(f"Initializing project '{self.name}'...")
        os.makedirs(self.kgr_folder_path)
        return True

    def load_manifests(self):
        if not self.kgr_folder_path.exists():
            raise FileNotFoundError(f"{self.kgr_folder_path} does not exist")
        for yaml_file in self.kgr_folder_path.glob("*.kgr.yaml"):
            with open(yaml_file, 'r') as file:
                manifest = yaml.safe_load(file)
                self.manifests.append(manifest)
        return self.manifests

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
        return []
