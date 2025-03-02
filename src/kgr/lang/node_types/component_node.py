from .conjunction_node import ConjunctionNode

class ComponentNode(ConjunctionNode):
    """
    A node that represents a component.
    """
    def __init__(self, name: str, meta: dict, expects: dict, requires: dict, implements: list, satisfies: dict):
        super().__init__([
            expects,
            requires,
            implements,
            satisfies,
        ])
        self.name = name
        self.meta = meta
        self.expects = expects
        self.requires = requires
        self.implements = implements
        self.satisfies = satisfies

