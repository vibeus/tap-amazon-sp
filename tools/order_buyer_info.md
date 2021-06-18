|**AmazonOrderId**  <br>*required*|An Amazon-defined order identifier, in 3-7-7 format.|string|
|**BuyerEmail**  <br>*optional*|The anonymized email address of the buyer.|string|
|**BuyerName**  <br>*optional*|The name of the buyer.|string|
|**BuyerCounty**  <br>*optional*|The county of the buyer.|string|
|**BuyerTaxInfo**  <br>*optional*|Tax information about the buyer.|[BuyerTaxInfo](#buyertaxinfo)|
|**PurchaseOrderNumber**  <br>*optional*|The purchase order (PO) number entered by the buyer at checkout. Returned only for orders where the buyer entered a PO number at checkout.|string|
