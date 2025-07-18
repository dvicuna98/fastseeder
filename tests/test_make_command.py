import os
from typer.testing import CliRunner
from fastseeder.runner import app

runner = CliRunner()

def test_make_seed_creates_file():
    result = runner.invoke(app, ["make", "example-seed"])
    assert result.exit_code == 0

    files = os.listdir("database/seeds")
    assert any("example-seed" in f for f in files)
