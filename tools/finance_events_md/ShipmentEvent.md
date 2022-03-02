|**AmazonOrderId**  <br>*optional*|An Amazon-defined identifier for an order.|string|
|**SellerOrderId**  <br>*optional*|A seller-defined identifier for an order.|string|
|**MarketplaceName**  <br>*optional*|The name of the marketplace where the event occurred.|string|
|**OrderChargeList**  <br>*optional*|A list of order-level charges. These charges are applicable to Multi-Channel Fulfillment COD orders.|[ChargeComponentList](#chargecomponentlist)|
|**OrderChargeAdjustmentList**  <br>*optional*|A list of order-level charge adjustments. These adjustments are applicable to Multi-Channel Fulfillment COD orders.|[ChargeComponentList](#chargecomponentlist)|
|**ShipmentFeeList**  <br>*optional*|A list of shipment-level fees.|[FeeComponentList](#feecomponentlist)|
|**ShipmentFeeAdjustmentList**  <br>*optional*|A list of shipment-level fee adjustments.|[FeeComponentList](#feecomponentlist)|
|**OrderFeeList**  <br>*optional*|A list of order-level fees. These charges are applicable to Multi-Channel Fulfillment orders.|[FeeComponentList](#feecomponentlist)|
|**OrderFeeAdjustmentList**  <br>*optional*|A list of order-level fee adjustments. These adjustments are applicable to Multi-Channel Fulfillment orders.|[FeeComponentList](#feecomponentlist)|
|**DirectPaymentList**  <br>*optional*|A list of transactions where buyers pay Amazon through one of the credit cards offered by Amazon or where buyers pay a seller directly through COD.|[DirectPaymentList](#directpaymentlist)|
|**PostedDate**  <br>*optional*|The date and time when the financial event was posted.|[Date](#date)|
|**ShipmentItemList**  <br>*optional*|A list of shipment items.|[ShipmentItemList](#shipmentitemlist)|
|**ShipmentItemAdjustmentList**  <br>*optional*|A list of shipment item adjustments.|[ShipmentItemList](#shipmentitemlist)|