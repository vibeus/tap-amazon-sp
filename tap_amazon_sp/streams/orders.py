from singer import metadata


class Orders:
    @property
    def name(self):
        return "orders"

    @property
    def key_properties(self):
        return ["AmazonOrderId"]

    @property
    def replication_key(self):
        return "LastUpdateDate"

    @property
    def replication_method(self):
        return "INCREMENTAL"

    def get_metadata(self, schema):
        mdata = metadata.get_standard_metadata(
            schema=schema,
            key_properties=self.key_properties,
            valid_replication_keys=[self.replication_key],
            replication_method=self.replication_method,
        )

        return mdata

    def get_tap_data(self, state):
        return []
