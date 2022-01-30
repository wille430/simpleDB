
class Query (list[dict]):

    def __init__(self, data: list[dict]):
        self._results = data
        super().__init__(data)

    def first(self):
        """Return first item in results"""
        return self._results[0]
