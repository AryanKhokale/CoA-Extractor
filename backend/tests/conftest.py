import sys
import os
import pytest

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app_dir = os.path.join(backend_dir, "app")

for d in [backend_dir, app_dir]:
    if d not in sys.path:
        sys.path.insert(0, d)

from database.session import init_db

@pytest.fixture(autouse=True, scope="session")
def setup_test_db():
    init_db()
