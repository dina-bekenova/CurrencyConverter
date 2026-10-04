#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 - <<'PY'
import sys, unittest
suite = unittest.defaultTestLoader.discover("tests")
result = unittest.TextTestRunner(verbosity=2).run(suite)
total = result.testsRun
passed = total - len(result.failures) - len(result.errors)
print(f"TESTS: {passed}/{total}")
sys.exit(0 if result.wasSuccessful() and total > 0 else 1)
PY