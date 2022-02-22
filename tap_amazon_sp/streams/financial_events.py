import singer
import json
import time
from singer import metadata
from sp_api import api
from sp_api.base import SellingApiRequestThrottledException, Marketplaces
from datetime import datetime, timedelta

LOGGER = singer.get_logger()
DEFAULT_BACKOFF_SECONDS = 60


class financialEvents:
    def __init__(self):
        self.__start_date = ""
        self.__state = {}

    @property
    def name(self):
        return "financialEvents"

    @property
    def key_properties(self):
        return ["AmazonOrderId"]

    @property
    def replication_key(self):
        return "PostedDate"

    @property
    def replication_method(self):
        return "INCREMENTAL"

    @property
    def state(self):
        return self.__state

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
        self.__start_date = config.get("start_date", today)
        self.__backoff_seconds = config.get("rate_limit_backoff_seconds", DEFAULT_BACKOFF_SECONDS)
        self.__state = state.copy()

        for account in config.get("accounts", []):
            account_credentials = credentials.copy()
            account_credentials["refresh_token"] = account["refresh_token"]
            yield from self.get_account_data(account, account_credentials)

    def get_account_data(self, account, credentials):
        account_id = account["selling_partner_id"]
        # for market_name in account["marketplaces"]:
        LOGGER.info(f"Loading financial events for account {account_id}...")
        marketplace = getattr(Marketplaces, account["marketplaces"][0])
        finances_api = api.Finances(credentials=credentials, marketplace=marketplace, account=account_id)
        yield from self.get_financialEvents(finances_api)

    def get_financialEvents(self, finances_api):
        state_date = self.__state.get(finances_api.marketplace_id, self.__start_date)
        after = max(self.__start_date, state_date)
        max_rep_key = after
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        before = min(datetime.fromisoformat(today), datetime.fromisoformat(after.replace("Z", "")) + timedelta(days=180)).isoformat()

        next_token = ""
        while True:
            try:
                resp = finances_api.list_financial_events(PostedAfter=after, PostedBefore=before, NextToken=next_token)
                for event in resp.payload["FinancialEvents"]["ShipmentEventList"]:
                    rep_key = event.get(self.replication_key)
                    if rep_key and rep_key > max_rep_key:
                        max_rep_key = rep_key
                    
                    yield self.get_event_details(event, "Charge")

                for event in resp.payload["FinancialEvents"]["RefundEventList"]:
                    rep_key = event.get(self.replication_key)
                    if rep_key and rep_key > max_rep_key:
                        max_rep_key = rep_key

                    yield self.get_event_details(event, "Refund")

                next_token = resp.payload.get("NextToken")
                if not next_token:
                    # break
                    if before < today:
                        next_token = ""
                        after = before
                        before = min(datetime.fromisoformat(today), datetime.fromisoformat(after.replace("Z", "")) + timedelta(days=180)).isoformat()
                    else:
                        break
            except SellingApiRequestThrottledException:
                LOGGER.warning(f"Rate limit exceeded. Waiting {self.__backoff_seconds} seconds...")
                time.sleep(self.__backoff_seconds)

        self.__state[finances_api.marketplace_id] = max_rep_key
        
    def get_event_details(self, event, type):
        if type == "Refund":
            for key in list(event.keys()):
                if "Adjustment" in key: 
                    new_key = key.replace("Adjustment", "")
                    event[new_key] = event.pop(key)
            for item in event["ShipmentItemList"]:
                for key in list(item.keys()):
                    if "Adjustment" in key: 
                        new_key = key.replace("Adjustment", "")
                        item[new_key] = item.pop(key)
                    if "CostOfPoints" in key:
                        item["CostOfPoints"] = item.pop(key)
        
        event["EventType"]=type

        return event

