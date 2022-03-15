import singer
import json
import time
from sp_api import api
from sp_api.base import SellingApiRequestThrottledException, Marketplaces
from datetime import datetime, timedelta

from .base import Base

LOGGER = singer.get_logger()

class Orders(Base):
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
    def specific_api(self):
        return api.Orders

    def get_api_data(self, specific_api, marketplace):
        state_date = self._state.get(specific_api.marketplace_id, self._start_date)
        after = max(self._start_date, state_date)
        max_rep_key = after

        next_token = ""
        while True:
            try:
                resp = specific_api.get_orders(LastUpdatedAfter=after, NextToken=next_token)
                for order in resp.payload["Orders"]:
                    rep_key = order.get(self.replication_key)
                    if rep_key and rep_key > max_rep_key:
                        max_rep_key = rep_key

                    yield self.get_order_details(specific_api, order)

                next_token = resp.payload.get("NextToken")
                if not next_token:
                    break
            except SellingApiRequestThrottledException:
                LOGGER.warning(f"Rate limit exceeded. Waiting {self._backoff_seconds} seconds...")
                time.sleep(self._backoff_seconds)

        self._state[specific_api.marketplace_id] = max_rep_key

    def get_order_details(self, specific_api, order):
        while True:
            try:
                order_id = order["AmazonOrderId"]
                LOGGER.info(f"Loading details for order id {order_id}...")

                order["OrderItems"] = self.get_order_items(specific_api, order_id)
                order["BuyerInfo"] = self.get_buyer_info(specific_api, order_id)
                order["ShippingAddress"] = self.get_order_address(specific_api, order_id)
                return order
            except SellingApiRequestThrottledException:
                LOGGER.warning(f"Rate limit exceeded. Waiting {self._backoff_seconds} seconds...")
                time.sleep(self._backoff_seconds)

    def get_order_items(self, specific_api, order_id):
        order_items = []
        next_token = ""
        while True:
            resp = specific_api.get_order_items(order_id, NextToken=next_token)
            order_items.extend(resp.payload["OrderItems"])
            next_token = resp.payload.get("NextToken")
            if not next_token:
                break

        return order_items

    def get_buyer_info(self, specific_api, order_id):
        resp = specific_api.get_order_buyer_info(order_id)
        return resp.payload

    def get_order_address(self, specific_api, order_id):
        resp = specific_api.get_order_address(order_id)
        return resp.payload.get("ShippingAddress")
