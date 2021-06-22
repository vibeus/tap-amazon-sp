import singer
import json
import time
from singer import metadata
from sp_api import api
from sp_api.base import SellingApiRequestThrottledException, Marketplaces
from datetime import datetime, timedelta

LOGGER = singer.get_logger()
DEFAULT_BACKOFF_SECONDS = 60


class Orders:
    def __init__(self):
        self.__start_date = ""
        self.__state = {}

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
        for market_name in account["marketplaces"]:
            LOGGER.info(f"Loading orders for account {account_id}, market {market_name}...")
            marketplace = getattr(Marketplaces, market_name)
            orders_api = api.Orders(credentials=credentials, marketplace=marketplace, account=account_id)
            yield from self.get_orders(orders_api)

    def get_orders(self, orders_api):
        state_date = self.__state.get(orders_api.marketplace_id, self.__start_date)
        after = max(self.__start_date, state_date)
        max_rep_key = after

        next_token = ""
        while True:
            try:
                resp = orders_api.get_orders(LastUpdatedAfter=after, NextToken=next_token)
                for order in resp.payload["Orders"]:
                    rep_key = order.get(self.replication_key)
                    if rep_key and rep_key > max_rep_key:
                        max_rep_key = rep_key

                    yield self.get_order_details(orders_api, order)

                next_token = resp.payload.get("NextToken")
                if not next_token:
                    break
            except SellingApiRequestThrottledException:
                LOGGER.warning(f"Rate limit exceeded. Waiting {self.__backoff_seconds} seconds...")
                time.sleep(self.__backoff_seconds)

        self.__state[orders_api.marketplace_id] = max_rep_key

    def get_order_details(self, orders_api, order):
        while True:
            try:
                order_id = order["AmazonOrderId"]
                LOGGER.info(f"Loading details for order id {order_id}...")

                order["OrderItems"] = self.get_order_items(orders_api, order_id)
                order["BuyerInfo"] = self.get_buyer_info(orders_api, order_id)
                order["ShippingAddress"] = self.get_order_address(orders_api, order_id)
                return order
            except SellingApiRequestThrottledException:
                LOGGER.warning(f"Rate limit exceeded. Waiting {self.__backoff_seconds} seconds...")
                time.sleep(self.__backoff_seconds)

    def get_order_items(self, orders_api, order_id):
        order_items = []
        next_token = ""
        while True:
            resp = orders_api.get_order_items(order_id, NextToken=next_token)
            order_items.extend(resp.payload["OrderItems"])
            next_token = resp.payload.get("NextToken")
            if not next_token:
                break

        return order_items

    def get_buyer_info(self, orders_api, order_id):
        resp = orders_api.get_order_buyer_info(order_id)
        return resp.payload

    def get_order_address(self, orders_api, order_id):
        resp = orders_api.get_order_address(order_id)
        return resp.payload.get("ShippingAddress")
