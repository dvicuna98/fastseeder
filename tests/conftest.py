import pytest
from unittest.mock import MagicMock
from sqlalchemy import MetaData
import os
import shutil

@pytest.fixture(autouse=True)
def clean_seed_folder():
    if os.path.exists("database/seeds"):
        shutil.rmtree("database/seeds")
    yield
    if os.path.exists("database/seeds"):
        shutil.rmtree("database/seeds")

@pytest.fixture
def fake_db():
    engine = MagicMock()
    session = MagicMock()
    metadata = MetaData()
    SessionMaker = MagicMock(return_value=session)
    return engine, SessionMaker, metadata, session
