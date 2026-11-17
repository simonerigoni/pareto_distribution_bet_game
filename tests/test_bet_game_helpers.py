"""Tests for Player and helpers defined in bet_game.ipynb."""

import ast
import json
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = REPO_ROOT / "bet_game.ipynb"


def _notebook_source(path: Path) -> str:
    notebook = json.loads(path.read_text())
    lines: list[str] = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        for line in "".join(cell.get("source") or []).splitlines():
            stripped = line.lstrip()
            if stripped.startswith(("%%", "%", "!")):
                lines.append(f"# {line}")
            else:
                lines.append(line)
        lines.append("")
    return "\n".join(lines)


def _load_names(names: set[str]) -> dict:
    source = _notebook_source(NOTEBOOK)
    tree = ast.parse(source)
    kept: list[ast.stmt] = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and node.name in names
    ]
    module = ast.Module(body=kept, type_ignores=[])
    namespace = {"np": np}
    exec(compile(module, str(NOTEBOOK), "exec"), namespace)
    return namespace


def test_player_update_money_and_metrics():
    namespace = _load_names({"Player", "count_broke_players", "get_median_money_players"})
    player_cls = namespace["Player"]
    players = [player_cls(1, 100), player_cls(2, 0), player_cls(3, 50)]
    players[0].update_money(20)
    assert players[0].money == 20
    assert namespace["count_broke_players"](players) == 1
    assert namespace["get_median_money_players"](players) == 20
