import yaml
from .application_schema import ApplicationSchema
from .resource_schema import ResourceSchema
from .component_schema import ComponentSchema

class SchemaFactory:
    @staticmethod
    def create_schema(data: dict):
        """
        Create the appropriate schema instance based on the 'kind' field in data.
        Defaults to ComponentSchema if kind is not specifically recognized.
        """
        kind = data.get("kind")
        if not kind:
            raise ValueError("Missing 'kind' in manifest.")

        if kind == "Application":
            return ApplicationSchema()
        elif kind == "Resource":
            return ResourceSchema()
        else:
            return ComponentSchema()

    @staticmethod
    def load_yaml_and_validate(yaml_path: str) -> list:
        """
        Loads a YAML file, instantiates its schema, and returns the list of validation errors.
        """
        with open(yaml_path, "r") as file:
            data = yaml.safe_load(file)
        schema = SchemaFactory.create_schema(data)
        errors = schema.validate(data)
        return errors