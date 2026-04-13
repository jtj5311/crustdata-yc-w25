#!/usr/bin/env python3
"""Find the biggest YC W25 companies via Crustdata's Company Search API.

Crustdata has no explicit YC-batch field, so we approximate: some Crustdata entries
embed the batch directly in the company name (e.g. "nao Labs (YC X25)"). We fuzzy-
match the BATCH string on basic_info.name and require Y Combinator as an investor.
Tweak BATCH / LIMIT below to target a different cohort.
"""
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CRUSTDATA_API_KEY")
if not API_KEY:
    sys.exit("error: CRUSTDATA_API_KEY not set. copy .env.example to .env and fill it in.")

URL = "https://api.crustdata.com/company/search"
HEADERS = {
    "authorization": f"Bearer {API_KEY}",
    "x-api-version": "2025-11-01",
    "content-type": "application/json",
}

BATCH = "W25"
LIMIT = 20

PAYLOAD = {
    "filters": {
        "op": "and",
        "conditions": [
            {"field": "funding.investors", "type": "[.]", "value": "Y Combinator"},
            {"field": "basic_info.name", "type": "[.]", "value": BATCH},
        ],
    },
    "sorts": [{"column": "headcount.total", "order": "desc"}],
    "limit": LIMIT,
    "fields": [
        "basic_info.name",
        "basic_info.primary_domain",
        "basic_info.year_founded",
        "headcount.total",
        "funding.total_investment_usd",
        "funding.last_fundraise_date",
        "locations.hq_country",
    ],
}


def get(d, path, default=""):
    for key in path.split("."):
        if not isinstance(d, dict):
            return default
        d = d.get(key)
    return default if d is None else d


def main() -> None:
    resp = requests.post(URL, headers=HEADERS, json=PAYLOAD, timeout=30)
    if resp.status_code != 200:
        print(f"HTTP {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)

    companies = resp.json().get("companies", [])
    if not companies:
        print("no companies returned — try loosening filters (lower YEAR_FLOOR or change operator).")
        return

    rows = [
        {
            "name": get(c, "basic_info.name"),
            "domain": get(c, "basic_info.primary_domain"),
            "founded": get(c, "basic_info.year_founded"),
            "headcount": get(c, "headcount.total"),
            "funding_usd": get(c, "funding.total_investment_usd"),
            "country": get(c, "locations.hq_country"),
        }
        for c in companies
    ]

    cols = list(rows[0].keys())
    widths = {k: max(len(k), *(len(str(r[k])) for r in rows)) for k in cols}
    print(f"top {len(rows)} YC {BATCH} companies by headcount:\n")
    print("  ".join(k.ljust(widths[k]) for k in cols))
    print("  ".join("-" * widths[k] for k in cols))
    for r in rows:
        print("  ".join(str(r[k]).ljust(widths[k]) for k in cols))


if __name__ == "__main__":
    main()
