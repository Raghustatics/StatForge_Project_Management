"""The engine stays pure: no web, database or AI imports (AGENTS.md §12)."""

import ast
from pathlib import Path

import statforge_engine

FORBIDDEN = {
    "fastapi",
    "starlette",
    "sqlalchemy",
    "psycopg",
    "boto3",
    "httpx",
    "requests",
    "anthropic",
    "openai",
    "pydantic_ai",
}


def _imported_roots(source: str) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def test_engine_has_no_web_db_ai_imports() -> None:
    package_dir = Path(statforge_engine.__file__).parent
    modules = list(package_dir.rglob("*.py"))
    assert modules
    for module in modules:
        bad = _imported_roots(module.read_text(encoding="utf-8")) & FORBIDDEN
        assert not bad, f"{module.name} imports {sorted(bad)}"


def test_engine_version() -> None:
    assert statforge_engine.__version__ == "0.1.0"
