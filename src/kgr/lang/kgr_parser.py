
from kgr.lang.schema.schema_factory import SchemaFactory


class KangarooParser:
    """
    Produce a structure that can be interpreted by the Kangaroo runtime.

    KangarooParser is a reverse parser that:
        - walks the tree of already pre-parsed nodes of python built-in types 
          (originally parsed from YAML based on kgr schema)
        - generate a new tree of typed nodes that can be interpreted by the
          Kangaroo runtime.
    """

    def __init__(self, manifest_info: dict):
        self.manifest_info = manifest_info
        self.schema = SchemaFactory.create_schema(manifest_info)

    def _visit(self, node: dict, _schema: dict) -> list:
        errors = []
        for field, field_type in _schema.fields.items():
            if field not in node:
                errors.append(f"Missing field: {field}")
                continue
            field_errors = field_type.validate(node[field])
            errors.extend(field_errors)

    def parse(self):
        """
        Walk the manifest and validate it against the schema.
        """
        # Build AST Node structure from manifest data

        # Visit the AST Node structure
        result = self._visit(self.manifest_info, self.schema)
        if result.failed:
            raise ValueError(result.error)
            return result.value