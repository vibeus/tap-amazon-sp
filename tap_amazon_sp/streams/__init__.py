from .orders import Orders
from .financial_events import FinancialEvents
from .inventories import Inventories


def create_stream(stream_id):
    if stream_id == "orders":
        return Orders()
    if stream_id == "financial_events":
        return FinancialEvents()
    if stream_id == "inventories":
        return Inventories()

    assert False, f"Unsupported stream: {stream_id}"
