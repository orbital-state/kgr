from .component_schema import ComponentSchema

class ApplicationSchema(ComponentSchema):
    def __init__(self):
        super().__init__("Application")
        # Override: AppSchema should only allow 'Application' as the kind
        self._schema["kind"]["allowed"] = ["Application"]

    def validate(self, data: dict) -> list:
        errors = super().validate(data)
        # Additional check: ensure kind is exactly 'Application'
        if data.get("kind") != "Application":
            errors.append("Invalid 'kind': expected 'Application'.")
        return errors