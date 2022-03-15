import singer
import json
import time
from sp_api import api
from sp_api.base import SellingApiRequestThrottledException, Marketplaces
from datetime import datetime, timedelta

from .base import Base

LOGGER = singer.get_logger()

class FinancialEvents(Base):
    @property
    def name(self):
        return "financial_events"

    @property
    def key_properties(self):
        return ["AmazonOrderId", "EventType", "PostedDate"]

    @property
    def replication_key(self):
        return "PostedDate"
    
    @property
    def specific_api(self):
        return api.Finances

    def market_places(self, marketplaces):
        return [", ".join(marketplaces)], [getattr(Marketplaces,marketplaces[0])]

    def get_api_data(self, specific_api, marketplace):
        state_date = self._state.get(specific_api.marketplace_id, self._start_date)
        after = max(self._start_date, state_date)
        max_rep_key = after
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        before = min(datetime.fromisoformat(today), datetime.fromisoformat(after.replace("Z", "")) + timedelta(days=180)).isoformat()

        next_token = ""
        while True:
            try:
                resp = specific_api.list_financial_events(PostedAfter=after, PostedBefore=before, NextToken=next_token)
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
                    if before < today:
                        next_token = ""
                        after = before
                        before = min(datetime.fromisoformat(today), datetime.fromisoformat(after.replace("Z", "")) + timedelta(days=180)).isoformat()
                    else:
                        break
            except SellingApiRequestThrottledException:
                LOGGER.warning(f"Rate limit exceeded. Waiting {self.__backoff_seconds} seconds...")
                time.sleep(self.__backoff_seconds)

        self._state[specific_api.marketplace_id] = max_rep_key
        
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
        
        event["EventType"] = type

        return event