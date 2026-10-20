import uuid6


class Thread:

    def __init__(
        self,
        _id: str | None = None,
    ):
        self._id = id or uuid6.uuid7()
