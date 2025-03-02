from .base_schema import BaseSchema
import re


class ComponentSchema(BaseSchema):
    def __init__(self):
        super().__init__("component")
        self._schema.update({
            "kind": {
                "type": "str", 
                "required": True, 
                # restrict inheritance to these kinds
                # TODO: improve error message
                "allowed": ["Component", "Resource", "Application"],
                "kgr_type": "ComponentType",
            },
            "extends": {
                "type": "dict",
                "schema": {
                    "base": {"type": "str", "required": True},
                    "overlays": {"type": "list", "schema": {"type": "str"}, "required": False},
                },
                "kgr_type": "ConstraintType",
            },
            "expects": {
                "type": "dict",
                "schema": {
                    "variables": {
                        "type": "dict", 
                        "required": False,
                    },
                    "secrets": {
                        "type": "dict", 
                        "required": False
                    },
                },
                "kgr_type": "ConstraintType",
            },
            "requires": {
                "type": "dict",
                "key": {"type": "str", "regex": re.compile(r"^[a-zA-Z0-9_]+$")},
                "valueschema": { 
                    "type": "dict",
                    "schema": {
                        "resources": {"type": "list", "value": {"type": "str"}, "required": False},
                        "applications": {"type": "list", "value": {"type": "str"}, "required": False},
                    },
                },
                "required": False,
                "kgr_type": "ConstraintType",
            },
            "implements": {
                "type": "list", 
                "value": {"type": "str"}, 
                "required": False,
                "kgr_type": "ConstraintType",
            },
            "satisfies": {
                "type": "dict",
                "key": {"type": "str", "regex": re.compile(r"^[a-zA-Z0-9_]+$")},
                "valueschema": { 
                    "type": "dict",
                    "schema": {
                        "resources": {"type": "list", "value": {"type": "str"}, "required": False},
                        "applications": {"type": "list", "value": {"type": "str"}, "required": False},
                    },
                },
                "required": True,
                "kgr_type": "ConstraintType",
            },
        })

    def validate(self, data: dict) -> list:
        """
        Validate the input data against the schema.
        Returns a list of error messages. An empty list means validation passed.

        additional validation:

        """
        errors = []

        # Validate with BaseSchema logic
        errors.extend(super().validate(data))

        return errors
