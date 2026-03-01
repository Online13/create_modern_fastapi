import ast
from pathlib import Path


def get_imported_modules(file_path: Path):
    tree = ast.parse(file_path.read_text(encoding="utf-8"))
    modules = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split(".")[0])

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.add(node.module.split(".")[0])

    return modules


def module_to_file(module: str) -> Path:
    return Path(module.replace(".", "/") + ".py")


def format_graph_error(importer, imported, chain, graph):
    lines = []

    header = f"\n🚫 CLEAN ARCHITECTURE VIOLATION\n────────────────────────────────\n{importer} must NOT depend on {imported}\n"
    lines.append(header)

    for a, b in zip(chain, chain[1:]):
        details = graph.get_import_details(importer=a, imported=b)
        for d in details:
            file = module_to_file(d["importer"])
            lineno = d["line_number"]
            code = d["line_contents"].strip()
            pointer = " " * (len(code) - len(code.lstrip())) + "^"
            lines.append(
                f"""
📄 File: {file}
🔢 Line: {lineno}

    {code}
    {pointer}

❌ Illegal import:
   {d['importer']}
   → {d['imported']}
"""
            )

    return "\n".join(lines)
