# tap-gocardless

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from [GoCardless](https://gocardless.com/)
- Extracts the following resources:
  - [Events](https://developer.gocardless.com/api-reference/#events-list-events)
  - [Payments](https://developer.gocardless.com/api-reference/#payments-list-payments)
  - [Payouts](https://developer.gocardless.com/api-reference/#payouts-list-payouts)
  - [Payout Items](https://developer.gocardless.com/api-reference/#payout-items-get-all-payout-items-in-a-single-payout)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

---

Copyright &copy; 2021 @morrislaptop
