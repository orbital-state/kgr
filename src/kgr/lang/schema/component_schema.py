from .base_schema import BaseSchema
import re


class ComponentSchema(BaseSchema):
    def __init__(self, kind: str):
        super().__init__(kind) # kind is required as component is base class
        self._schema.update({
            "kind": {
                "type": "str",
                "required": True,
                # restrict inheritance to these kinds
                # TODO: improve error message
                "allowed": ["Component", "Resource", "Application"],
            },
            "extends": {
                "type": "dict",
                "schema": {
                    "base": {"type": "str", "required": True},
                    "overlays": {"type": "list", "schema": {"type": "str"}, "required": False},
                },
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
            },
            "requires": {
                "type": "dict",
                "key": {"type": "str", "regex": re.compile(r"^[a-zA-Z0-9_]+$")},
                "value": { 
                    "type": "dict",
                    # TODO: test if this gets validated
                    "schema": {
                        "resources": {"type": "list", "value": {"type": "str"}, "required": False},
                        "applications": {"type": "list", "value": {"type": "str"}, "required": False},
                    },
                },
                "required": False,
            },
            "implements": {
                "type": "list", 
                "value": {"type": "str"},
                "required": False,
            },
            "satisfies": {
                "type": "dict",
                "key": {
                    "type": "str", 
                    "regex": re.compile(r"^[a-zA-Z0-9_]+$"),
                },
                "value": { 
                    "type": "list",
                    "value": {
                        "type": "dict",
                        "required": True,
                    },
                },
                "required": True,
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
