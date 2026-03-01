from pathlib import Path
from tests.utils import get_imported_modules

FORBIDDEN_IMPORTS = {"fastapi", "sqlmodel", "sqlalchemy", "pydantic"}
CORE_LAYERS = ["src/domain", "src/application"]


def test_no_fastapi_in_core_layers():
    violations = []

    for layer in CORE_LAYERS:
        for file in Path(layer).rglob("*.py"):
            imported_modules = get_imported_modules(file)

            forbidden = imported_modules & FORBIDDEN_IMPORTS
            if forbidden:
                violations.append(
                    f"{file} imports forbidden module(s): {', '.join(forbidden)}"
                )

    assert not violations, "\n".join(violations)
