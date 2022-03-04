|**ASIN**  <br>*required*|The Amazon Standard Identification Number (ASIN) of the item.|string|
|**SellerSKU**  <br>*optional*|The seller stock keeping unit (SKU) of the item.|string|
|**OrderItemId**  <br>*required*|An Amazon-defined order item identifier.|string|
|**Title**  <br>*optional*|The name of the item.|string|
|**QuantityOrdered**  <br>*required*|The number of items in the order.|integer|
|**QuantityShipped**  <br>*optional*|The number of items shipped.|integer|
|**ProductInfo**  <br>*optional*|Product information for the item.|[ProductInfoDetail](#productinfodetail)|
|**PointsGranted**  <br>*optional*|The number and value of Amazon Points granted with the purchase of an item.|[PointsGrantedDetail](#pointsgranteddetail)|
|**ItemPrice**  <br>*optional*|The selling price of the order item. Note that an order item is an item and a quantity. This means that the value of ItemPrice is equal to the selling price of the item multiplied by the quantity ordered. Note that ItemPrice excludes ShippingPrice and GiftWrapPrice.|[Money](#money)|
|**ShippingPrice**  <br>*optional*|The shipping price of the item.|[Money](#money)|
|**ItemTax**  <br>*optional*|The tax on the item price.|[Money](#money)|
|**ShippingTax**  <br>*optional*|The tax on the shipping price.|[Money](#money)|
|**ShippingDiscount**  <br>*optional*|The discount on the shipping price.|[Money](#money)|
|**ShippingDiscountTax**  <br>*optional*|The tax on the discount on the shipping price.|[Money](#money)|
|**PromotionDiscount**  <br>*optional*|The total of all promotional discounts in the offer.|[Money](#money)|
|**PromotionDiscountTax**  <br>*optional*|The tax on the total of all promotional discounts in the offer.|[Money](#money)|
|**PromotionIds**  <br>*optional*|A list of promotion identifiers provided by the seller when the promotions were created.|[PromotionIdList](#promotionidlist)|
|**CODFee**  <br>*optional*|The fee charged for COD service.|[Money](#money)|
|**CODFeeDiscount**  <br>*optional*|The discount on the COD fee.|[Money](#money)|
|**IsGift**  <br>*optional*|When true, the item is a gift.|boolean|
|**ConditionNote**  <br>*optional*|The condition of the item as described by the seller.|string|
|**ConditionId**  <br>*optional*|The condition of the item.<br><br>Possible values: New, Used, Collectible, Refurbished, Preorder, Club.|string|
|**ConditionSubtypeId**  <br>*optional*|The subcondition of the item.<br><br>Possible values: New, Mint, Very Good, Good, Acceptable, Poor, Club, OEM, Warranty, Refurbished Warranty, Refurbished, Open Box, Any, Other.|string|
|**ScheduledDeliveryStartDate**  <br>*optional*|The start date of the scheduled delivery window in the time zone of the order destination. In ISO 8601 date time format.|string|
|**ScheduledDeliveryEndDate**  <br>*optional*|The end date of the scheduled delivery window in the time zone of the order destination. In ISO 8601 date time format.|string|
|**PriceDesignation**  <br>*optional*|Indicates that the selling price is a special price that is available only for Amazon Business orders. For more information about the Amazon Business Seller Program, see the [Amazon Business website](https://www.amazon.com/b2b/info/amazon-business). <br><br>Possible values: BusinessPrice - A special price that is available only for Amazon Business orders.|string|
|**TaxCollection**  <br>*optional*|Information about withheld taxes.|[TaxCollection](#taxcollection)|
|**SerialNumberRequired**  <br>*optional*|When true, the product type for this item has a serial number.<br><br>Returned only for Amazon Easy Ship orders.|boolean|
|**IsTransparency**  <br>*optional*|When true, transparency codes are required.|boolean|
|**IossNumber**  <br>*optional*|The IOSS number of the seller. Sellers selling in the EU will be assigned a unique IOSS number that must be listed on all packages sent to the EU.|string|
|**StoreChainStoreId**  <br>*optional*|The store chain store identifier. Linked to a specific store in a store chain.|string|
|**DeemedResellerCategory**  <br>*optional*|The category of deemed reseller. This applies to selling partners that are not based in the EU and is used to help them meet the VAT Deemed Reseller tax laws in the EU and UK.|enum ([DeemedResellerCategory](#deemedresellercategory))|
