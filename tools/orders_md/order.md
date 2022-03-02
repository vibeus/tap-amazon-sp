|**AmazonOrderId**  <br>*required*|An Amazon-defined order identifier, in 3-7-7 format.|string|
|**SellerOrderId**  <br>*optional*|A seller-defined order identifier.|string|
|**PurchaseDate**  <br>*required*|The date when the order was created.|string|
|**LastUpdateDate**  <br>*required*|The date when the order was last updated.<br><br>Note: LastUpdateDate is returned with an incorrect date for orders that were last updated before 2009-04-01.|string|
|**OrderStatus**  <br>*required*|The current order status.|enum ([OrderStatus](#orderstatus))|
|**FulfillmentChannel**  <br>*optional*|Whether the order was fulfilled by Amazon (AFN) or by the seller (MFN).|enum ([FulfillmentChannel](#fulfillmentchannel))|
|**SalesChannel**  <br>*optional*|The sales channel of the first item in the order.|string|
|**OrderChannel**  <br>*optional*|The order channel of the first item in the order.|string|
|**ShipServiceLevel**  <br>*optional*|The shipment service level of the order.|string|
|**OrderTotal**  <br>*optional*|The total charge for this order.|[Money](#money)|
|**NumberOfItemsShipped**  <br>*optional*|The number of items shipped.|integer|
|**NumberOfItemsUnshipped**  <br>*optional*|The number of items unshipped.|integer|
|**PaymentExecutionDetail**  <br>*optional*|Information about sub-payment methods for a Cash On Delivery (COD) order.<br><br>Note: For a COD order that is paid for using one sub-payment method, one PaymentExecutionDetailItem object is returned, with PaymentExecutionDetailItem/PaymentMethod = COD. For a COD order that is paid for using multiple sub-payment methods, two or more PaymentExecutionDetailItem objects are returned.|[PaymentExecutionDetailItemList](#paymentexecutiondetailitemlist)|
|**PaymentMethod**  <br>*optional*|The payment method for the order. This property is limited to Cash On Delivery (COD) and Convenience Store (CVS) payment methods. Unless you need the specific COD payment information provided by the PaymentExecutionDetailItem object, we recommend using the PaymentMethodDetails property to get payment method information.|enum ([PaymentMethod](#paymentmethod))|
|**PaymentMethodDetails**  <br>*optional*|A list of payment methods for the order.|[PaymentMethodDetailItemList](#paymentmethoddetailitemlist)|
|**MarketplaceId**  <br>*optional*|The identifier for the marketplace where the order was placed.|string|
|**ShipmentServiceLevelCategory**  <br>*optional*|The shipment service level category of the order.<br><br>Possible values: Expedited, FreeEconomy, NextDay, SameDay, SecondDay, Scheduled, Standard.|string|
|**EasyShipShipmentStatus**  <br>*optional*|The status of the Amazon Easy Ship order. This property is included only for Amazon Easy Ship orders.<br><br>Possible values: PendingPickUp, LabelCanceled, PickedUp, OutForDelivery, Damaged, Delivered, RejectedByBuyer, Undeliverable, ReturnedToSeller, ReturningToSeller.|string|
|**CbaDisplayableShippingLabel**  <br>*optional*|Custom ship label for Checkout by Amazon (CBA).|string|
|**OrderType**  <br>*optional*|The type of the order.|enum ([OrderType](#ordertype))|
|**EarliestShipDate**  <br>*optional*|The start of the time period within which you have committed to ship the order. In ISO 8601 date time format. Returned only for seller-fulfilled orders.<br><br>Note: EarliestShipDate might not be returned for orders placed before February 1, 2013.|string|
|**LatestShipDate**  <br>*optional*|The end of the time period within which you have committed to ship the order. In ISO 8601 date time format. Returned only for seller-fulfilled orders.<br><br>Note: LatestShipDate might not be returned for orders placed before February 1, 2013.|string|
|**EarliestDeliveryDate**  <br>*optional*|The start of the time period within which you have committed to fulfill the order. In ISO 8601 date time format. Returned only for seller-fulfilled orders.|string|
|**LatestDeliveryDate**  <br>*optional*|The end of the time period within which you have committed to fulfill the order. In ISO 8601 date time format. Returned only for seller-fulfilled orders that do not have a PendingAvailability, Pending, or Canceled status.|string|
|**IsBusinessOrder**  <br>*optional*|When true, the order is an Amazon Business order. An Amazon Business order is an order where the buyer is a Verified Business Buyer.|boolean|
|**IsPrime**  <br>*optional*|When true, the order is a seller-fulfilled Amazon Prime order.|boolean|
|**IsPremiumOrder**  <br>*optional*|When true, the order has a Premium Shipping Service Level Agreement. For more information about Premium Shipping orders, see "Premium Shipping Options" in the Seller Central Help for your marketplace.|boolean|
|**IsGlobalExpressEnabled**  <br>*optional*|When true, the order is a GlobalExpress order.|boolean|
|**ReplacedOrderId**  <br>*optional*|The order ID value for the order that is being replaced. Returned only if IsReplacementOrder = true.|string|
|**IsReplacementOrder**  <br>*optional*|When true, this is a replacement order.|boolean|
|**PromiseResponseDueDate**  <br>*optional*|Indicates the date by which the seller must respond to the buyer with an estimated ship date. Returned only for Sourcing on Demand orders.|string|
|**IsEstimatedShipDateSet**  <br>*optional*|When true, the estimated ship date is set for the order. Returned only for Sourcing on Demand orders.|boolean|
|**IsSoldByAB**  <br>*optional*|When true, the item within this order was bought and re-sold by Amazon Business EU SARL (ABEU). By buying and instantly re-selling your items, ABEU becomes the seller of record, making your inventory available for sale to customers who would not otherwise purchase from a third-party seller.|boolean|
|**DefaultShipFromLocationAddress**  <br>*optional*|The recommended location for the seller to ship the items from. It is calculated at checkout. The seller may or may not choose to ship from this location.|[Address](#address)|
|**FulfillmentInstruction**  <br>*optional*|Contains the instructions about the fulfillment like where should it be fulfilled from.|[FulfillmentInstruction](#fulfillmentinstruction)|
|**IsISPU**  <br>*optional*|When true, this order is marked to be picked up from a store rather than delivered.|boolean|
