from ..result import Result, Ok


class RuleNode:
    """
    Most basic node type. It is a function that takes some arguments and returns a Result.
    """

    def __call__(self, *args, **kwds) -> Result:
        return Ok()
