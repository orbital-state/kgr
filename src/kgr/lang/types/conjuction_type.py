from ..error import Error
from ..result import Result


class ConjuctionType:
    def __init__(self, rules: list):
        self.rules = rules

    def __call__(self, *args, **kwds) -> Result:
        errors = []
        for idx, rule in enumerate(self.rules):
            res: Result = rule(*args, **kwds)
            if not res.success:
                errors.append(res.error)
        if errors:
            combined_error = Error("Conjunction failed", __file__)
            for err in errors:
                combined_error.add_child(err)
            return Result(value=False, error=combined_error)
        return Result(value=True)
