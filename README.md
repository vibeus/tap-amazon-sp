# tap-amazon-sp

This is a [Singer][1] tap that produces JSON-formatted data following the [Singer spec][2].

This tap:

- Pulls raw data from [Amazon SP API][3]
- Extracts the following resources:
  - [Orders][4]
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

## Install

```
pip install tap-amazon-sp
```

## Usage

1. Follow [Singer.io Best Practices][5] for setting up separate `tap` and `target` virtualenvs to avoid version conflicts.
2. Create a [config file][6] ~/config.json with [Amazon Seller Partner API credentials][7]. Multiple accounts across
   different marketplaces are supported. Here is [a list of marketplace names][8].
    ```json
    {
      "accounts": [
        {
          "selling_partner_id": "NA_SELLING_PARTNER_ID",
          "marketplaces": ["US", "MX", "CA"],
          "refresh_token": "env[NA_REFRESH_TOKEN]"
        },
        {
          "selling_partner_id": "AU_SELLING_PARTNER_ID",
          "marketplaces": ["AU"],
          "refresh_token": "env[AU_REFRESH_TOKEN]"
        }
      ],
      "access_key_id": "ACCESS_KEY_ID",
      "secret_access_key": "env[SECRET_ACCESS_KEY]",
      "sp_role_arn": "arn:aws:iam::1234567890:role/RoleName",
      "lwa_client_id": "CLIENT_ID",
      "lwa_client_secret": "env[LWA_CLIENT_SECRET]",
      "start_date": "2021-01-01T00:00:00Z",
      "rate_limit_backoff_seconds": 60
    }
    ```
3. Discover catalog: `tap-amazon-sp -d > catalog.json`
4. Select `orders` stream in the generated `catalog.json`.
    ```
    ...
    "stream": "orders",
    "metadata": [
      {
        "breadcrumb": [],
        "metadata": {
          "table-key-properties": [
            "AmazonOrderId"
          ],
          "forced-replication-method": "INCREMENTAL",
          "valid-replication-keys": [
            "LastUpdateDate"
          ],
          "inclusion": "available",
          "selected": true  <-- Somewhere in the huge catalog file, in stream metadata.
        }
      },
      ...
    ]
    ...
    ```
5. Use following command to sync all orders with order items, buyer info and shipping address (when available).
```bash
tap-amazon-sp -c config.json --catalog catalog.json > output.txt
```

---

Copyright &copy; 2021 Vibe Inc

[1]: https://singer.io
[2]: https://github.com/singer-io/getting-started/blob/master/SPEC.md
[3]: https://github.com/amzn/selling-partner-api-docs
[4]: https://github.com/amzn/selling-partner-api-docs/blob/main/references/orders-api/ordersV0.md
[5]: https://github.com/singer-io/getting-started/blob/master/docs/RUNNING_AND_DEVELOPING.md#running-a-singer-tap-with-a-singer-target
[6]: https://github.com/vibeus/tap-amazon-sp/blob/master/sample_config.json
[7]: https://github.com/amzn/selling-partner-api-docs/blob/main/guides/en-US/developer-guide/SellingPartnerApiDeveloperGuide.md#creating-and-configuring-iam-policies-and-entities
[8]: https://github.com/saleweaver/python-amazon-sp-api/blob/master/sp_api/base/marketplaces.py
