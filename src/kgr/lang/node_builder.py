from .node_types.component_node import ComponentNode
from .schema.schema_factory import SchemaFactory


class AstBuilder:
    """
    Produce a structure that can be interpreted by the Kangaroo runtime.
    
    Builder acts as a reverse parser that:
        - walks the tree of already pre-parsed nodes of python built-in types 
          (originally parsed from YAML based on kgr schema)
        - generate a new tree of typed nodes that can be interpreted by the
          Kangaroo runtime.
    """
    def __init__(self):
        # Do we really need this?
        self.stack = []
        self.root = None

    def _build_node(self, data, schema):
        kgr_type = schema.get("kgr_type")
        if not kgr_type:
            return None

    def _build_component_node(self, data, schema):
        assert schema.kind == 'application' or schema.kind == 'resource'
        for field, field_type in schema.items():
            if field in data:
                if field == "expects":
                    variables = data[field].get("variables", {})
                    secrets = data[field].get("secrets", {})
                    expects = ExpectationsNode(variables, secrets)
                elif field == "requires":
                    resources = data[field].get("resources", [])
                    applications = data[field].get("applications", [])
                    requires = RequirementsNode(resources, applications)
                elif field == "implements":
                    implementations = data[field]
                    implements = ImplementationsNode(implementations)
                elif field == "satisfies":
                    satisfies = data[field]
        return ComponentNode(
            name=data.get("name", ""),
            meta=data.get("meta", {}),
            expects=expects,
            requires=requires,
            implements=implements,
            satisfies=satisfies,
        )

    def from_data(self, yaml_data) -> AstNode:
        schema = SchemaFactory.get_schema(yaml_data)
        if schema.kind == 'application' or schema.kind == 'resource':
            self.root = self._build_component_node(yaml_data, schema)
        self.root = self._build_node(yaml_data, schema)
        return self.root