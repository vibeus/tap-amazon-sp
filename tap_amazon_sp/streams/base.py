import singer
import json
import time
from singer import metadata
from sp_api import api
from sp_api.base import SellingApiRequestThrottledException, Marketplaces
from datetime import datetime, timedelta

LOGGER = singer.get_logger()
DEFAULT_BACKOFF_SECONDS = 60


class Base:
    def __init__(self):
        self._start_date = ""
        self._state = {}

    @property
    def name(self):
        return "base_stream"

    @property
    def key_properties(self):
        return ["id"]

    @property
    def replication_key(self):
        return "date"

    @property
    def replication_method(self):
        return "INCREMENTAL"

    @property
    def state(self):
        return self._state
    
    @property
    def specific_api(self):
        return api


    def get_metadata(self, schema):
        mdata = metadata.get_standard_metadata(
            schema=schema,
            key_properties=self.key_properties,
            valid_replication_keys=[self.replication_key],
            replication_method=self.replication_method,
        )

        return mdata

    def get_tap_data(self, config, state):
        credentials = {
            "lwa_app_id": config["lwa_client_id"],
            "lwa_client_secret": config["lwa_client_secret"],
            "aws_access_key": config["access_key_id"],
            "aws_secret_key": config["secret_access_key"],
            "role_arn": config.get("sp_role_arn"),
        }

        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        self._start_date = config.get("start_date", today)
        self._backoff_seconds = config.get("rate_limit_backoff_seconds", DEFAULT_BACKOFF_SECONDS)
        self._state = state.copy()

        for account in config.get("accounts", []):
            account_credentials = credentials.copy()
            account_credentials["refresh_token"] = account["refresh_token"]
            yield from self.get_account_data(account, account_credentials)

    def get_account_data(self, account, credentials):
        account_id = account["selling_partner_id"]
        LOGGER.info("Loading {} for account {}...".format(self.name, account_id))
        marketplace = getattr(Marketplaces, account["marketplaces"][0])
        specific_api = self.specific_api(credentials=credentials, marketplace=marketplace, account=account_id)
        yield from self.get_api_data(specific_api)
    
    def get_api_data(self, specific_api):
        state_date = self._state.get(specific_api.marketplace_id, self._start_date)
        after = max(self._start_date, state_date)
        max_rep_key = after

        next_token = ""
        return [{},{}]