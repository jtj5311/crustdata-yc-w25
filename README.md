# crustdata-search

A tiny Python CLI that uses the [Crustdata](https://crustdata.com) Company Search API to find the biggest YC W25 companies by headcount.

Built as a quickstart against the [Crustdata Company Search endpoint](https://docs.crustdata.com/company-docs/search).

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/jtj5311/crustdata-yc-w25
cd crustdata-search
cp .env.example .env
# paste your Crustdata API key after CRUSTDATA_API_KEY=
uv run search.py
```

Get an API key from the [Crustdata dashboard](https://crustdata.com). See the [API introduction](https://docs.crustdata.com/general/introduction) for headers, versioning, and pricing.

## Example output

```
top 20 YC W25 companies by headcount:

name                       domain              founded  headcount  funding_usd  country
-------------------------  ------------------  -------  ---------  -----------  -------
Harper (YC W25)            harperinsure.com    2024     29         47500000.0
G LNK (YC W25)             glnkco.com          2024     21         500000.0
Spott (YC W25)             spott.io            2024     20         3200000.0
...
```

## Tweaking the query

Edit constants at the top of `search.py`:

- `BATCH` — YC batch code to match (`"W25"`, `"S24"`, etc.)
- `LIMIT` — number of results (1–1000)

The filter payload lives just below and is a plain dict — swap operators, add conditions, or change the sort column. See the [Crustdata filter operator reference](https://docs.crustdata.com/company-docs/search) for the full list.

## How the batch filter works (and its limits)

Crustdata has no dedicated "YC batch" field. This script approximates by combining two filters:

1. `funding.investors` exact-token match on `"Y Combinator"`
2. `basic_info.name` exact-token match on the batch code (e.g. `"W25"`)

Condition 2 works because Crustdata embeds the batch in the company name for many YC entries (e.g. `"Harper (YC W25)"`). **The tradeoff**: any W25 company whose Crustdata record doesn't embed the batch in its name will be missed. For exhaustive coverage, cross-reference with the [YC W25 launch list](https://www.ycombinator.com/companies?batch=W2025).

## Links

- [Crustdata](https://crustdata.com)
- [Crustdata docs](https://docs.crustdata.com/general/introduction)
- [Company Search API](https://docs.crustdata.com/company-docs/search)
- [uv](https://docs.astral.sh/uv/)
