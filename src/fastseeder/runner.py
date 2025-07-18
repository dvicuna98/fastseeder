from dotenv import load_dotenv
load_dotenv()
import typer
import os
from datetime import datetime, timezone
from pathlib import Path
from slugify import slugify
from .config.SeedHistoryModel import SeedHistoryModel
from .config.discover import discover_seed_classes
from .db import get_database

SEEDS_DIR = Path(os.environ.get("SEED_LOCATION","database/seeds"))

app = typer.Typer()

@app.command("seed")
def seed(
    yes: bool = typer.Option(False, "--yes", "-y", help="Run seeds without confirmation"),
    skip_errors: bool = typer.Option(False, "--skip", "-s", help="Continue on errors"),
):
    seed_location = os.environ.get("SEED_LOCATION","database/seeds")
    """
    List and run all seeds that haven't been run yet.
    """
    sql_engine, sql_sessionmaker, sql_metadata = get_database()

    # Create seed_history table if it doesn't exist
    SeedHistoryModel.metadata.create_all(bind=sql_engine)

    session = sql_sessionmaker()
    seeds = discover_seed_classes(seed_location)
    seeds.sort(key=lambda s: s.seed_id)  # Ensure date-order execution

    # Filter pending seeds
    pending_seeds = [
        seed for seed in seeds
        if not session.query(SeedHistoryModel).filter_by(id=seed.seed_id).first()
    ]

    if not pending_seeds:
        typer.echo("✅ No pending seeds to run.")
        return

    typer.echo("📋 Pending seeds to run:")
    for seed in pending_seeds:
        typer.echo(f" - {seed.seed_id}")

    if not yes:
        confirm = typer.confirm("⚠️  Run all pending seeds listed above?")
        if not confirm:
            typer.echo("❌ Seed process cancelled.")
            raise typer.Abort()

    for seed in pending_seeds:
        try:
            print(f"🚀 Running seed '{seed.seed_id}'...")
            seed.run(session)
            session.add(SeedHistoryModel(id=seed.seed_id, applied_at=datetime.now(timezone.utc)))
            session.commit()
            print(f"✅ Done with '{seed.seed_id}'")
        except Exception as e:
            print(f"❌ Error while running seed '{seed.seed_id}': {e}")
            session.rollback()
            if hasattr(seed, 'rollback'):
                try:
                    print(f"↩️ Attempting rollback for '{seed.seed_id}'...")
                    seed.rollback(session)
                    session.commit()
                    print(f"✅ Rollback done for '{seed.seed_id}'")
                except Exception as rollback_error:
                    print(f"⚠️ Rollback failed for '{seed.seed_id}': {rollback_error}")
                    session.rollback()
            if not skip_errors:
                raise typer.Exit(code=1)


@app.command("make")
def make_seed(name: str = typer.Argument(..., help="Name of the new seed")):
    """
    Create a new seed file with a timestamp-based ID.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S")
    slug = slugify(name)
    seed_id = f"{now}-{slug}"
    class_name = ''.join(word.capitalize() for word in slug.split('-'))

    file_name = f"{seed_id}.py"
    file_path = SEEDS_DIR / file_name

    content = f'''from fastseeder.config.base_seed import BaseSeed

class {class_name}(BaseSeed):
    seed_id = "{seed_id}"

    def run(self, session):
        # Add seed logic here
        pass
    
    def rollback(self, session):
        # Add rollback logic here
        pass
'''

    SEEDS_DIR.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)

    print(f"✅ Created seed: {file_path}")


if __name__ == "__main__":
    app()

def main():
    app()