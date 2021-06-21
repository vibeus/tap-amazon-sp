import singer
import json
import time
from singer import metadata
from sp_api import api
from sp_api.base import SellingApiRequestThrottledException, Marketplaces
from datetime import datetime, timedelta

LOGGER = singer.get_logger()
BACKOFF_SECONDS = 10


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

    def get_tap_data(self, config, state):
        credentials = {
            "lwa_app_id": config["lwa_client_id"],
            "lwa_client_secret": config["lwa_client_secret"],
            "aws_access_key": config["access_key_id"],
            "aws_secret_key": config["secret_access_key"],
            "role_arn": config.get("sp_role_arn"),
        }

        for account in config.get("accounts", []):
            account_credentials = credentials.copy()
            account_credentials["refresh_token"] = account["refresh_token"]
            yield from self.get_account_data(config, state, account, account_credentials)

    def get_account_data(self, config, state, account, credentials):
        account_id = account["selling_partner_id"]
        for market_name in account["marketplaces"]:
            LOGGER.info(f"Loading orders for account {account_id}, market {market_name}...")
            marketplace = getattr(Marketplaces, market_name)
            orders_api = api.Orders(credentials=credentials, marketplace=marketplace, account=account_id)
            yield from self.get_orders(config, state, orders_api)

    def get_orders(self, config, state, orders_api):
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        start_date = config.get("start_date", today)
        state_date = state.get(self.name, start_date)
        after = max(start_date, state_date)

        next_token = ""
        while True:
            try:
                resp = orders_api.get_orders(LastUpdatedAfter=after, NextToken=next_token)
                for order in resp.payload["Orders"]:
                    yield self.get_order_details(orders_api, order)

                next_token = resp.payload.get("NextToken")
                if not next_token:
                    break
            except SellingApiRequestThrottledException:
                LOGGER.warning(f"Rate limit exceeded. Waiting {BACKOFF_SECONDS} seconds...")
                time.sleep(BACKOFF_SECONDS)

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
                LOGGER.warning(f"Rate limit exceeded. Waiting {BACKOFF_SECONDS} seconds...")
                time.sleep(BACKOFF_SECONDS)

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
        return resp.payload["ShippingAddress"]
