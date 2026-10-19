"""Gate test-case traceability (AGENTS.md §4.1).

Lists every TC in the active gate's section of the gate map and fails if any TC
has no matching test, or if a mapped test is skipped or xfail. The scan is
static (AST for Python, regex for TS) so it is fast and runs without the stack.

Usage: python scripts/tc_trace.py [--gate G01] [--root .]
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

TC_PATTERN = re.compile(r"TC-\d{2}\.\d+")
GATE_LOG = Path("docs/GATE_LOG.md")
GATE_MAP = Path("docs/StatForge_Gate_Map_v1.0.md")

_ACTIVE_GATE = re.compile(r"\*\*Active gate:\*\*\s*(G\d{2})")
_TEST_NAME = re.compile(r"^test_tc(\d{2})_(\d+)(?:_|$)")
_TS_TITLE = re.compile(
    r"\b(?:test|it|describe)(?:\.(?P<mod>skip|fixme|todo|only))?\(\s*['\"`]\[(?P<tc>TC-\d{2}\.\d+)\]"
)
_SKIP_DIRS = {"node_modules", ".venv", "dist", ".git", "sources", "docs", ".superpowers"}
_DISABLING_MARKS = {"skip", "skipif", "xfail"}


@dataclass(frozen=True)
class TestRef:
    path: str
    name: str
    tc: str
    disabled: bool


@dataclass(frozen=True)
class TraceResult:
    mapped: dict[str, list[TestRef]]
    unmapped: list[str]
    disabled: list[TestRef] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.unmapped and not self.disabled


def active_gate(gate_log: Path) -> str:
    match = _ACTIVE_GATE.search(gate_log.read_text(encoding="utf-8"))
    if match is None:
        raise ValueError(f"No '**Active gate:** Gxx' line in {gate_log}")
    return match.group(1)


def gate_test_cases(gate_map: Path, gate: str) -> list[str]:
    section: list[str] = []
    inside = False
    for line in gate_map.read_text(encoding="utf-8").splitlines():
        if line.startswith("#### "):
            inside = line.startswith(f"#### {gate} ")
            continue
        if inside:
            section.append(line)
    found: list[str] = []
    for tc in TC_PATTERN.findall("\n".join(section)):
        if tc not in found:
            found.append(tc)
    return found


def is_test_file(path: str) -> bool:
    parts = PurePosixPath(path.replace("\\", "/"))
    name = parts.name
    if "e2e" in parts.parts[:-1] and name.endswith((".ts", ".tsx")):
        return True
    if re.search(r"\.(test|spec)\.tsx?$", name):
        return True
    in_tests_dir = "tests" in parts.parts[:-1]
    return (
        in_tests_dir
        and name.endswith(".py")
        and (name.startswith("test_") or name.endswith("_test.py"))
    )


def tc_ids_in(text: str) -> set[str]:
    return set(TC_PATTERN.findall(text))


def _mark_name(node: ast.expr) -> tuple[str, list[ast.expr]] | None:
    """Return (mark, args) for `pytest.mark.<mark>` or `pytest.mark.<mark>(...)`."""
    args: list[ast.expr] = []
    if isinstance(node, ast.Call):
        args = list(node.args)
        node = node.func
    if (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Attribute)
        and node.value.attr == "mark"
    ):
        return node.attr, args
    return None


def _marks(nodes: Sequence[ast.expr]) -> tuple[list[str], bool]:
    tcs: list[str] = []
    disabled = False
    for node in nodes:
        parsed = _mark_name(node)
        if parsed is None:
            continue
        mark, args = parsed
        if mark in _DISABLING_MARKS:
            disabled = True
        if mark == "tc":
            tcs.extend(
                a.value for a in args if isinstance(a, ast.Constant) and isinstance(a.value, str)
            )
    return tcs, disabled


def _module_marks(tree: ast.Module) -> tuple[list[str], bool]:
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "pytestmark" for t in stmt.targets
        ):
            value = stmt.value
            items = list(value.elts) if isinstance(value, (ast.List, ast.Tuple)) else [value]
            return _marks(items)
    return [], False


def _scan_python(rel: str, text: str) -> Iterator[TestRef]:
    tree = ast.parse(text)
    module_tcs, module_disabled = _module_marks(tree)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not node.name.startswith("test"):
            continue
        tcs, disabled = _marks(node.decorator_list)
        named = _TEST_NAME.match(node.name)
        if named:
            tcs.append(f"TC-{named.group(1)}.{int(named.group(2))}")
        for tc in dict.fromkeys([*module_tcs, *tcs]):
            yield TestRef(rel, node.name, tc, disabled or module_disabled)


def _scan_ts(rel: str, text: str) -> Iterator[TestRef]:
    for match in _TS_TITLE.finditer(text):
        disabled = match.group("mod") in {"skip", "fixme", "todo"}
        yield TestRef(rel, match.group(0), match.group("tc"), disabled)


def _walk(root: Path) -> Iterator[Path]:
    for path in root.iterdir():
        if path.is_dir():
            if path.name not in _SKIP_DIRS:
                yield from _walk(path)
        else:
            yield path


def scan_tests(root: Path) -> list[TestRef]:
    refs: list[TestRef] = []
    for path in sorted(_walk(root)):
        rel = path.relative_to(root).as_posix()
        if not is_test_file(rel):
            continue
        text = path.read_text(encoding="utf-8")
        scanner = _scan_python if rel.endswith(".py") else _scan_ts
        refs.extend(scanner(rel, text))
    return refs


def trace(root: Path, gate: str | None = None) -> TraceResult:
    gate = gate or active_gate(root / GATE_LOG)
    tcs = gate_test_cases(root / GATE_MAP, gate)
    refs = [ref for ref in scan_tests(root) if ref.tc in tcs]
    mapped = {tc: [ref for ref in refs if ref.tc == tc] for tc in tcs}
    return TraceResult(
        mapped={tc: found for tc, found in mapped.items() if found},
        unmapped=[tc for tc in tcs if not mapped[tc]],
        disabled=[ref for ref in refs if ref.disabled],
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gate test-case traceability")
    parser.add_argument("--gate", help="gate id, e.g. G01 (default: active gate in GATE_LOG)")
    parser.add_argument("--root", default=".", help="repository root")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    gate = args.gate or active_gate(root / GATE_LOG)
    result = trace(root, gate)
    for tc in gate_test_cases(root / GATE_MAP, gate):
        refs = result.mapped.get(tc, [])
        if not refs:
            print(f"{tc:<9} MISSING")
        for ref in refs:
            status = "DISABLED" if ref.disabled else "OK"
            print(f"{tc:<9} {status:<8} {ref.path}::{ref.name}")
    print(f"tc_trace {gate}: {'PASS' if result.ok else 'FAIL'}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
