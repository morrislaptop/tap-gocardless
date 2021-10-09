#!/usr/bin/env python3
import os
import json
import singer
from singer import utils
from tap_gocardless.client import GocardlessClient
from tap_gocardless.discover import discover
from tap_gocardless.sync import sync

REQUIRED_CONFIG_KEYS = ["start_date", "access_token"]
LOGGER = singer.get_logger()

@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    client = GocardlessClient(args.config['access_token'], args.config['user_agent'])

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover()

        sync(client, catalog, args.state, args.config['start_date'])

if __name__ == "__main__":
    main()
