from .orders import Orders


def create_stream(stream_id):
    if stream_id == "orders":
        return Orders()

    assert False, f"Unsupported stream: {stream_id}"
