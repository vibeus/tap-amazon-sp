#!/usr/bin/env python3
import os
import re
import json
import singer
from singer import utils, metadata, Transformer
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema
from tap_amazon_sp.streams import create_stream


REQUIRED_CONFIG_KEYS = ["start_date", "access_key_id", "secret_access_key", "lwa_client_id", "lwa_client_secret"]
LOGGER = singer.get_logger()


def expand_env(config):
    assert isinstance(config, dict)

    def repl(match):
        env_key = match.group(1)
        return os.environ.get(env_key, "")

    def expand(v):
        assert not isinstance(v, dict)
        if isinstance(v, str):
            return re.sub(r"env\[(\w+)\]", repl, v)
        else:
            return v

    copy = {}
    for k, v in config.items():
        if isinstance(v, dict):
            copy[k] = expand_env(v)
        elif isinstance(v, list):
            copy[k] = [expand_env(x) if isinstance(x, dict) else expand(x) for x in v]
        else:
            copy[k] = expand(v)

    return copy


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas():
    """Load schemas from schemas folder"""
    schemas = {}
    for filename in os.listdir(get_abs_path("schemas")):
        path = get_abs_path("schemas") + "/" + filename
        file_raw = filename.replace(".json", "")
        with open(path) as file:
            schemas[file_raw] = Schema.from_dict(json.load(file))
    return schemas


def discover():
    raw_schemas = load_schemas()
    streams = []
    for stream_id, schema in raw_schemas.items():
        stream = create_stream(stream_id)

        streams.append(
            CatalogEntry(
                tap_stream_id=stream_id,
                stream=stream_id,
                schema=schema,
                key_properties=stream.key_properties,
                metadata=stream.get_metadata(schema.to_dict()),
                replication_key=stream.replication_key,
                replication_method=stream.replication_method,
                is_view=None,
                database=None,
                table=None,
                row_count=None,
                stream_alias=None,
            )
        )
    return Catalog(streams)


def sync(config, state, catalog):
    """Sync data from tap source"""

    for catalog_stream in catalog.get_selected_streams(state):
        stream_id = catalog_stream.tap_stream_id
        LOGGER.info("Syncing stream:" + stream_id)

        singer.write_schema(
            stream_name=stream_id,
            schema=catalog_stream.schema.to_dict(),
            key_properties=catalog_stream.key_properties,
        )

        stream = create_stream(stream_id)
        stream_state = state.get(stream_id, {})

        t = Transformer()
        for row in stream.get_tap_data(config, stream_state):
            schema = catalog_stream.schema.to_dict()
            mdata = metadata.to_map(catalog_stream.metadata)
            record = t.transform(row, schema, mdata)

            singer.write_records(stream_id, [record])

        singer.write_state({stream_id: stream.state})


@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover()

        args.config = expand_env(args.config)
        sync(args.config, args.state, catalog)


if __name__ == "__main__":
    main()
