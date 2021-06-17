# tap-amazon-sp (Working in progress...)

This is a [Singer][1] tap that produces JSON-formatted data following the [Singer spec][2].

This tap:

- Pulls raw data from [Amazon SP API][3]
- Extracts the following resources:
  - [Orders][4]
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

---

Copyright &copy; 2021 Vibe Inc

[1]: https://singer.io
[2]: https://github.com/singer-io/getting-started/blob/master/SPEC.md
[3]: https://github.com/amzn/selling-partner-api-docs
[4]: https://github.com/amzn/selling-partner-api-docs/blob/main/references/orders-api/ordersV0.md
