import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

RATES_TO_KZT = {
    "KZT": 1.0,
    "USD": 480.0,
    "EUR": 520.0,
    "RUB": 5.5,
    "CNY": 66.0,
}


def convert(amount, from_cur, to_cur):
    """Convert amount from one currency to another via KZT."""
    from_cur = from_cur.upper()
    to_cur = to_cur.upper()
    if from_cur not in RATES_TO_KZT:
        raise ValueError(f"unknown currency: {from_cur}")
    if to_cur not in RATES_TO_KZT:
        raise ValueError(f"unknown currency: {to_cur}")
    if amount < 0:
        raise ValueError("amount must not be negative")
    result = amount * RATES_TO_KZT[from_cur] / RATES_TO_KZT[to_cur]
    return round(result, 2)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        query = parse_qs(url.query)

        if url.path == "/":
            self.send_json(200, {"message": "Currency converter"})
        elif url.path == "/healthz":
            self.send_json(200, {"status": "ok"})
        elif url.path == "/rates":
            self.send_json(200, RATES_TO_KZT)
        elif url.path == "/convert":
            try:
                amount = float(query["amount"][0])
                from_cur = query["from"][0]
                to_cur = query.get("to", ["KZT"])[0]
                self.send_json(200, {"result": convert(amount, from_cur, to_cur)})
            except (KeyError, ValueError) as e:
                self.send_json(400, {"error": str(e)})
        else:
            self.send_json(404, {"error": "not found"})

    def send_json(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())


def make_server(port):
    return ThreadingHTTPServer(("0.0.0.0", port), Handler)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    print(f"Listening on port {port}")
    make_server(port).serve_forever()