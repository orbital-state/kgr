from .component_schema import ComponentSchema

class ResourceSchema(ComponentSchema):
    def __init__(self):
        super().__init__("Resource")
        # Override: AppSchema should only allow 'Resource' as the kind
        self._schema["kind"]["allowed"] = ["Resource"]

    def validate(self, data: dict) -> list:
        errors = super().validate(data)
        # Additional check: ensure kind is exactly 'Resource'
        if data.get("kind") != "Resource":
            errors.append("Invalid 'kind': expected 'Resource'.")
        return errors
