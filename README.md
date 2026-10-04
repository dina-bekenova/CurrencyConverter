# Currency Converter

A small HTTP service that converts money between currencies. Exchange rates are
hard-coded (not live), so the service needs no internet and no API keys.

Written in Python 3, standard library only — nothing to install.

## Endpoints

| Method | Path | What it returns |
|---|---|---|
| GET | `/` | Greeting and usage hint |
| GET | `/healthz` | `{"status": "ok"}` — health check |
| GET | `/rates` | All rates relative to KZT |
| GET | `/convert?from=USD&to=KZT&amount=100` | Conversion result (`to` defaults to KZT) |

Supported currencies: KZT, USD, EUR, RUB, CNY. Unknown currency or a bad
amount returns `400`, an unknown path returns `404`.

## How to run

```bash
scripts/run.sh
```

## Port

The service listens on the port given in the `PORT` environment variable,
and on **8080** if it is not set:

```bash
PORT=9000 scripts/run.sh
curl "localhost:9000/convert?from=USD&amount=100"
```

## How to test

```bash
scripts/test.sh
```

Prints a summary line like `TESTS: 5/5` and exits 0 when all tests pass.
