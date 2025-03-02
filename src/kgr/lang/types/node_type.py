
class NodeType:
    """
    Base class for all nodes in the AST of the language.
    """

    def __init__(self):
        self.parent = None
        self.children = []

    def _visit(self, visitor):
        """
        Visit this node and its children.
        """
        visitor.visit(self)
        for child in self.children:
            child._visit(visitor)