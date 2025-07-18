import os
import importlib.util
import inspect
import re
from datetime import datetime
from pathlib import Path
from .base_seed import BaseSeed

SEED_ID_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2}-\d{2}:\d{2}:\d{2})-(.+)$')

def discover_seed_classes(seeds_dir: str = "database/seeds") -> list[BaseSeed]:
    seed_instances = []

    for file in os.listdir(seeds_dir):
        path = Path(seeds_dir) / file

        if path.suffix != ".py" or path.name in ("__init__.py", "base_seed.py", "models.py", "runner.py", "discover.py"):
            continue

        module_name = f"{seeds_dir.replace('/', '.')}.{path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseSeed) and obj is not BaseSeed:
                instance = obj()

                match = SEED_ID_PATTERN.match(instance.seed_id)
                if not match:
                    raise ValueError(
                        f"❌ Seed ID '{instance.seed_id}' in class '{name}' must follow the format: YYYY-MM-DD-HH:MM:SS-name"
                    )

                # Attach parsed datetime for sorting
                instance._parsed_datetime = datetime.strptime(match.group(1), "%Y-%m-%d-%H:%M:%S")
                seed_instances.append(instance)

    # Sort by datetime
    seed_instances.sort(key=lambda seed: seed._parsed_datetime)
    return seed_instances