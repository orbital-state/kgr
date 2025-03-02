import re


_allowed_kinds = ["Resource", "Application", "Component", "Service", "Infrastructure", "Environment"]


class BaseSchema:

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
        # mapping from string type names to actual Python types
        type_mapping = {
            "str": str,
            "int": int,
            "dict": dict,
            "list": list,
            "float": float,
            "bool": bool,
        }
        for field, field_type in schema.items():
            # validate the required fields
            print(f"field: {field}, field_type: {field_type}")
            if field_type.get("required") and field not in data:
                errors.append(f"Missing '{field}' in manifest")
            # validate the allowed values
            if field in data and "allowed" in field_type:
                if data[field] not in field_type["allowed"]:
                    errors.append(f"Invalid value '{field}': {data[field]}")
            # validate the field types using the mapping
            if field in data and field_type["type"] in type_mapping:
                if not isinstance(data[field], type_mapping[field_type["type"]]):
                    errors.append(f"Invalid type for '{field}' in manifest")
            # validate the regex pattern
            if field in data and "regex" in field_type:
                if not field_type["regex"].match(data[field]):
                    errors.append(f"Invalid value for '{field}' in manifest")
            # validate case like: "requires": {"type": "dict", "key": {"type": "str", "regex": re.compile(r"^[a-zA-Z0-9_]+$")},
            if field in data and "key" in field_type:
                for key in data[field]:
                    if not isinstance(key, type_mapping[field_type["key"]["type"]]):
                        errors.append(f"Invalid type for '{field}' in manifest")
                    if not field_type["key"]["regex"].match(key):
                        errors.append(f"Invalid value for '{field}' in manifest")
            # validate the nested fields recursively for: "schema": { ... }
            if field in data and "schema" in field_type:
                errors.extend(self._sub_validate(data[field], field_type["schema"]))
            # validate the nested fields recursively for: "value": { ... }
            # ... values of a list
            if field in data and field_type.get("type") == "list" and "value" in field_type:
                for value in data[field]:
                    if not isinstance(value, type_mapping[field_type["value"]["type"]]):
                        errors.append(f"Invalid type for '{field}' in manifest")
                    if field_type["value"].get("regex"):
                        if not field_type["value"]["regex"].match(value):
                            errors.append(f"Invalid value for '{field}' in manifest")
                    if field_type["value"].get("schema"):
                        errors.extend(self._sub_validate(value, field_type["value"]["schema"]))
            # validate the nested fields recursively for: "value": { ... }
            # ... values of a dict
            if field in data and field_type.get("type") == "dict" and "value" in field_type:
                for key, value in data[field].items():
                    if field_type["value"].get("type"):
                        if not isinstance(value, type_mapping[field_type["value"]["type"]]):
                            errors.append(f"Invalid type for '{field}' in manifest")
                    if field_type["value"].get("regex"):
                        if not field_type["value"]["regex"].match(value):
                            errors.append(f"Invalid value for '{field}' in manifest")
                    if field_type["value"].get("schema"):
                        errors.extend(self._sub_validate(value, field_type["value"]["schema"]))
        return errors

    def validate(self, data: dict) -> list:
        """
        Validate the input data against the schema.
        Returns a list of error messages. An empty list means validation passed.
        """
        errors = []

        # recursively validate the input data
        errors.extend(self._sub_validate(data, self._schema))

        # validate the version field in meta
        if "meta" in data and "version" in data["meta"]:
            if not self.validate_semver(data["meta"]["version"]):
                errors.append("Invalid semantic version")
        
        # finally, name of the schema should match the kind
        if data.get("kind") != self.kind:
            errors.append(f"Invalid 'kind': expected '{self.kind}'.")

        return errors

    def validate_semver(self, version: str) -> bool:
        """Simple check for semantic versioning, ensuring a format like X.Y.Z."""
        pattern = r'^\d+\.\d+\.\d+$'
        return bool(re.match(pattern, version))