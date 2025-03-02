from .rule_node import RuleNode
from ..error import Error
from ..result import Result, Ok, Failure


class ConjunctionNode(RuleNode):
    """
    A node in a conjunction tree.
    """

    def __init__(self, rules: list):
        self._rules = rules

    @property
    def rules(self):
        return self._rules

    def __call__(self, *args, **kwds) -> Result:
        errors = []
        for rule in enumerate(self.rules):
            res: Result = rule(*args, **kwds)
            if res.failed:
                errors.append(res.error)
        if errors:
            combined_error = Error("Conjunction failed", __file__)
            for err in errors:
                combined_error.add_child(err)
            return Failure(combined_error)
        return Ok()
