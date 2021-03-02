class JiraProject:

    def __init__(self, id: int, key: str, name: str):
        self._id = id
        self._key = key
        self._name = name

    def __repr__(self) -> str:
        return f"<JiraProject `{self.name}`>"

    @property
    def id(self) -> int:
        return self._id

    @property
    def key(self) -> str:
        return self._key

    @property
    def name(self) -> str:
        return self._name
