from stac_check.lint import Linter  # type: ignore


class StacLint:
    def __init__(
        self,
        stac_file: str = None,
    ):
        self.stac_file = stac_file

    def create_message(self):
        linter = Linter(self.stac_file, assets=True, links=True, recursive=False)
        return linter.best_practices_msg()
