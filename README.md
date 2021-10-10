# tap-gocardless

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from [GoCardless](https://gocardless.com/)
- Extracts the following resources:
  - [Events](https://developer.gocardless.com/api-reference/#events-list-events)
  - [Payments](https://developer.gocardless.com/api-reference/#payments-list-payments)
  - [Payouts](https://developer.gocardless.com/api-reference/#payouts-list-payouts)
  - [Payout Items](https://developer.gocardless.com/api-reference/#payout-items-get-all-payout-items-in-a-single-payout)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

## Quick Start

Install the tap and helpers

    python3 -m venv ~/.virtualenvs/tap-gocardless
    source ~/.virtualenvs/tap-gocardless/bin/activate
    pip3 install tap-gocardless https://github.com/chrisgoddard/singer-discover/archive/master.zip

Obtain an access token via https://developer.gocardless.com/getting-started/api/making-your-first-request/#creating-an-access-token

Create a `config.json` file with the following

```
{
  "access_token": "sandbox_xxxxxx",
  "start_date": "2017-01-01T00:00:00.000Z",
  "user_agent": "<user-agent>"
}
```

Run the tap in Discover mode and select which data you would like to extract:

    tap-gocardless --config config.json --discover | singer-discover -o catalog.json

Run the tap in sync mode

    tap-gocardless --config config.json --catalog catalog.json

Run the tap with a target, e.g. postgres

    tap-gocardless --config config.json --catalog catalog.json | target-postgres --config config.postgres.json >> state.json
    tail -1 state.json > state.json.tmp && mv state.json.tmp state.json

---

Copyright &copy; 2021 @morrislaptop
