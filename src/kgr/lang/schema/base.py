
_allowed_kinds = ["Resource", "Application", "Component", "Service", "Infrastructure", "Environment"]

class SchemaBase:

    def __init__(self, kind):
        self.kind = kind
        # mapping of field names to field types
        self._schema = {
            "name": {"type": "str", "required": True},
            "kind": {"type": "str", "required": True, "allowed": _allowed_kinds},
            "meta": {
                "type": "dict",
                "schema": {
                    "description": {"type": "str", "required": True},
                    "version": {"type": "str", "required": True},
                    "labels": {"type": "dict", "required": False},
                },
            }
        }

    def _sub_validate(self, data, schema):
        """
        Recursively validate the input data against the schema.

        Returns a list of error messages. An empty list means validation passed.
        """
        errors = []
        for field, field_type in schema.items():
            # validate the required fields
            if field_type["required"] and field not in data and field != "any":
                errors.append(f"Missing '{field}' in manifest")
            # validate the allowed values
            if field in data and "allowed" in field_type:
                if data[field] not in field_type["allowed"]:
                    errors.append(f"Invalid value '{field}': {data[field]}")
            # validate the field types
            if field in data and not isinstance(data[field], field_type["type"]):
                errors.append(f"Invalid type for '{field}' in manifest")
            # validate the nested fields
            if field in data and "schema" in field_type:
                errors.extend(self._sub_validate(data[field], field_type["schema"]))
        return errors

    def validate(self, data: dict) -> list:
        """
        Validate the input data against the schema.
        Returns a list of error messages. An empty list means validation passed.
        """
        errors = []

        # validate the required fields
        for field, field_type in self._schema.items():
            if field_type["required"] and field not in data:
                errors.append(f"Field '{field}' is required")
        
        # validate the field types
        for field, field_type in self._schema.items():
            if field in data:
                if field_type["type"] == "str" and not isinstance(data[field], str):
                    errors.append(f"Field '{field}' must be a string")
                if field_type["type"] == "dict" and not isinstance(data[field], dict):
                    errors.append(f"Field '{field}' must be a dictionary")
                if field_type["type"] == "list" and not isinstance(data[field], list):
                    errors.append(f"Field '{field}' must be a list")
        
        # validate the allowed values
        for field, field_type in self._schema.items():
            if field in data and "allowed" in field_type:
                if data[field] not in field_type["allowed"]:
                    errors.append(f"Invalid value for '{field}'")
        


        # validate the version field in meta
        if "meta" in data and "version" in data["meta"]:
            if not self.validate_semver(data["meta"]["version"]):
                errors.append("Invalid semantic version")
        
        return errors

    def validate_semver(self, version: str) -> bool:
        """Simple check for semantic versioning, ensuring a format like X.Y.Z."""
        pattern = r'^\d+\.\d+\.\d+$'
        return bool(re.match(pattern, version))