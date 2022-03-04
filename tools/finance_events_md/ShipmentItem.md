|**SellerSKU**  <br>*optional*|The seller SKU of the item. The seller SKU is qualified by the seller's seller ID, which is included with every call to the Selling Partner API.|string|
|**OrderItemId**  <br>*optional*|An Amazon-defined order item identifier.|string|
|**QuantityShipped**  <br>*optional*|The number of items shipped.|integer (int32)|
|**ItemChargeList**  <br>*optional*|A list of charges associated with the shipment item.|[ChargeComponentList](#chargecomponentlist)|
|**ItemFeeList**  <br>*optional*|A list of fees associated with the shipment item.|[FeeComponentList](#feecomponentlist)|
|**ItemTaxWithheldList**  <br>*optional*|A list of taxes withheld information for a shipment item.|[TaxWithheldComponentList](#taxwithheldcomponentlist)|
|**PromotionList**  <br>*optional*|A list of promotions.|[PromotionList](#promotionlist)|
|**CostOfPointsGranted**  <br>*optional*|The cost of Amazon Points granted for a shipment item.|[Currency](#currency)|


|**SellerSKU**  <br>*optional*|The seller SKU of the item. The seller SKU is qualified by the seller's seller ID, which is included with every call to the Selling Partner API.|string|
|**OrderAdjustmentItemId**  <br>*optional*|An Amazon-defined order adjustment identifier defined for refunds, guarantee claims, and chargeback events.|string|
|**QuantityShipped**  <br>*optional*|The number of items shipped.|integer (int32)|
|**ItemChargeAdjustmentList**  <br>*optional*|A list of charge adjustments associated with the shipment item. This value is only returned for refunds, guarantee claims, and chargeback events.|[ChargeComponentList](#chargecomponentlist)|
|**ItemFeeAdjustmentList**  <br>*optional*|A list of fee adjustments associated with the shipment item. This value is only returned for refunds, guarantee claims, and chargeback events.|[FeeComponentList](#feecomponentlist)|
|**ItemTaxWithheldList**  <br>*optional*|A list of taxes withheld information for a shipment item.|[TaxWithheldComponentList](#taxwithheldcomponentlist)|
|**PromotionAdjustmentList**  <br>*optional*|A list of promotion adjustments associated with the shipment item. This value is only returned for refunds, guarantee claims, and chargeback events.|[PromotionList](#promotionlist)|
|**CostOfPointsReturned**  <br>*optional*|The cost of Amazon Points returned for a shipment item. This value is only returned for refunds, guarantee claims, and chargeback events.|[Currency](#currency)|