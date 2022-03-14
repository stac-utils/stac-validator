from stac_check.lint import Linter  # type: ignore


class StacCheck:
    def __init__(
        self,
        stac_file: str = None,
    ):
        self.stac_file = stac_file

    def lint_message(self):
        linter = Linter(self.stac_file)
        return linter.create_best_practices_dict()
