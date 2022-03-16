import singer
import json
import time
from sp_api import api
from sp_api.base import SellingApiRequestThrottledException, Marketplaces
from datetime import datetime, timedelta

from .base import Base

LOGGER = singer.get_logger()

class Inventories(Base):
    @property
    def name(self):
        return "inventories"

    @property
    def key_properties(self):
        return ["marketplaceId", "asin", "sellerSku"]

    @property
    def replication_key(self):
        return "lastUpdatedTime"
    
    @property
    def specific_api(self):
        return api.Inventories

    def get_api_data(self, specific_api, marketplace):
        state_date = self._state.get(specific_api.marketplace_id, self._start_date)
        after = max(self._start_date, state_date)
        max_rep_key = after

        try:
            resp = specific_api.get_inventory_summary_marketplace(**{ "details": True, "marketplaceIds": [ marketplace.value[1]] })
            for item in resp.payload["inventorySummaries"]:
                rep_key = item.get(self.replication_key)
                if rep_key and rep_key > max_rep_key:
                    max_rep_key = rep_key
                
                yield self.unnest_record(item, marketplace.value[1])

        except SellingApiRequestThrottledException:
            LOGGER.warning(f"Rate limit exceeded. Waiting {self.__backoff_seconds} seconds...")
            time.sleep(self.__backoff_seconds)

        self._state[specific_api.marketplace_id] = max_rep_key
    
    def unnest_record(self, item, marketplaceId):
        item["marketplaceId"] = marketplaceId

        item.update(item['inventoryDetails'])
        item.pop('inventoryDetails', None)

        item.update(item['reservedQuantity'])
        item.pop('reservedQuantity', None)

        item.update(item['researchingQuantity'])
        item.pop('researchingQuantity', None)
        for researchingQuantity in item['researchingQuantityBreakdown']:
            item[researchingQuantity['name']] = researchingQuantity["quantity"]
        item.pop('researchingQuantityBreakdown', None)

        item.update(item['unfulfillableQuantity'])
        item.pop('unfulfillableQuantity', None)

        item.update(item['futureSupplyQuantity'])
        item.pop('futureSupplyQuantity', None)

        return item

        
