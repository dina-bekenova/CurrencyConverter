import json
import os
import sys
import threading
import unittest
import urllib.error
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
import main 


class ConverterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = main.make_server(0)
        cls.port = cls.server.server_address[1]
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def get(self, path):
        with urllib.request.urlopen(f"http://127.0.0.1:{self.port}{path}") as r:
            return r.status, json.loads(r.read())

    def test_root(self):
        status, body = self.get("/")
        self.assertEqual(status, 200)

    def test_healthz(self):
        status, body = self.get("/healthz")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "ok")

    def test_convert(self):
        status, body = self.get("/convert?from=USD&amount=100")
        self.assertEqual(body["result"], 48000.0)

    def test_unknown_currency(self):
        with self.assertRaises(urllib.error.HTTPError) as e:
            self.get("/convert?from=XYZ&amount=1")
        self.assertEqual(e.exception.code, 400)

    def test_unknown_path(self):
        with self.assertRaises(urllib.error.HTTPError) as e:
            self.get("/nope")
        self.assertEqual(e.exception.code, 404)


if __name__ == "__main__":
    unittest.main()