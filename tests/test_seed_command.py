import pytest
from unittest.mock import Mock
from typer.testing import CliRunner
import fastseeder.runner as runner_module
from fastseeder.runner import app

runner = CliRunner()

class DummySession:
    def __init__(self):
        self.added = []
        self._committed = False
        self._rolled_back = False

    def query(self, *args, **kwargs):
        return self

    def filter_by(self, **kwargs):
        return self

    def first(self):
        return None

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self._committed = True

    def rollback(self):
        self._rolled_back = True

class DummySeed:
    seed_id = "2025-01-01-00:00:00-dummy"
    ran = False

    def run(self, session):
        self.ran = True

@pytest.fixture
def dummy_seed(monkeypatch):
    dummy = DummySeed()
    monkeypatch.setattr(runner_module, "discover_seed_classes", lambda _: [dummy])
    return dummy

@pytest.fixture
def mock_database(monkeypatch):
    mock_engine = Mock()
    mock_session = DummySession()
    monkeypatch.setattr(runner_module, "get_database", lambda: (mock_engine, lambda: mock_session, None))
    return mock_session

def test_seed_runs_pending(monkeypatch, dummy_seed, mock_database):
    result = runner.invoke(app, ["seed"], input="y\n")
    assert result.exit_code == 0
    assert dummy_seed.ran is True
    assert mock_database._committed is True
