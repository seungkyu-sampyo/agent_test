from uuid6 import UUID, uuid7


class ReMiConDispatch:

    def __init__(
        self,
        id_: UUID | None = None,
        invoice_no: str = "",
        ship_date: str = "",
        plant_code: str = "",
        quantity: int = 0,
    ):
        self.id_: UUID = id_ or uuid7()
        self.invoice_no = invoice_no
        self.ship_date = ship_date
        self.plant_code = plant_code
        self.quantity = quantity
