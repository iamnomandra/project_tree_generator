
import argparse
import ast
import os
from pathlib import Path

from rich.console import Console
from rich.tree import Tree


class ProjectTree:
    EXCLUDE_FILES = {
        ".vscode",
        ".DS_Store",
        "__pycache__",
        ".idp-env",
        "database",
        "models",
        "documents",
        "data",
    }

    DESCRIPTIONS = {
        "app.py": "Entry point",
        ".env": "Project config like api key, url etc..",
        "config.py": "Project config classes colors, app config etc..",
        "nom_pipeline.py": "Actual orchestration engine Main Orchestrator",
        "requirements.txt": "Reproducible environment installation",
        "pyproject.toml": "Package/project metadata + build + dependency definition",
        "ingestion": "→ Document to Receive/Load",
        "preprocessing": "→ Document to Clean/Prepare",
        "classification": "→ Document type",
        "ocr": "→ Text extraction",
        "layout": "→ Visual structure",
        "extraction": "→ Semantic Fields/Entities/Tables",
        "normalization": "→ Values standardize",
        "validation": "→ Correctness",
        "confidence": "→ Confidence scoring",
        "rules": "→ Business decisions",
        "rules_files": "→ Business decisions rules file (json, yaml etc.)",
        "workflow": "→ State/Approval/Action",
        "knowledge": "→ RAG/Graph/Search",
        "storage": "→ Persistence",
        "contracts": "→ Canonical data contracts & pipeline result schemas",
        "observability": "→ Production telemetry: logs, metrics, traces & audit",
        "async_execution": "→ Distributed job execution, retries, queues & workers",
    }

    SPECIFIC_FILES = {
        "nom_pipeline.py",
        "app.py",
    }

    MAX_FILENAME_WIDTH = 30

    def __init__(self):
        self.console = Console()

    # ---------------------------------------------------------
    # Function parameters
    # ---------------------------------------------------------
    def get_parameters(self, node):
        params = []
        args = node.args

        positional_only = getattr(args, "posonlyargs", [])
        positional = args.args
        all_positional = positional_only + positional

        defaults_start = len(all_positional) - len(args.defaults)

        for i, arg in enumerate(all_positional):
            if i >= defaults_start:
                default = args.defaults[i - defaults_start]

                try:
                    default_value = ast.unparse(default)
                except Exception:
                    default_value = "..."

                params.append(f"{arg.arg}={default_value}")
            else:
                params.append(arg.arg)

        # *args
        if args.vararg:
            params.append(f"*{args.vararg.arg}")

        # Keyword-only arguments
        for arg, default in zip(args.kwonlyargs, args.kw_defaults):
            if default is None:
                params.append(arg.arg)
            else:
                try:
                    default_value = ast.unparse(default)
                except Exception:
                    default_value = "..."

                params.append(f"{arg.arg}={default_value}")

        # **kwargs
        if args.kwarg:
            params.append(f"**{args.kwarg.arg}")

        return ", ".join(params)

    # ---------------------------------------------------------
    # Python class/function tree
    # ---------------------------------------------------------
    def fun_class(self, path):
        label = ""

        try:
            with open(path, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)

            def walk_nodes(nodes, indent="    "):
                nonlocal label

                for node in nodes:

                    # -----------------------------
                    # CLASS
                    # -----------------------------
                    if isinstance(node, ast.ClassDef):

                        label += (
                            f"\n{indent}└── "
                            f"🔗 [yellow]Class: [/yellow]{node.name}"
                        )

                        # Base classes
                        if node.bases:
                            bases = []

                            for base in node.bases:
                                try:
                                    bases.append(ast.unparse(base))
                                except Exception:
                                    pass

                            if bases:
                                label += (
                                    f" [dim](extends: "
                                    f"{', '.join(bases)})[/dim]"
                                )

                        # Class body
                        walk_nodes(
                            node.body,
                            indent + "      ",
                        )

                    # -----------------------------
                    # FUNCTION / METHOD
                    # -----------------------------
                    elif isinstance(
                        node,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef,
                        ),
                    ):

                        prefix = (
                            "async def:"
                            if isinstance(node, ast.AsyncFunctionDef)
                            else "def:"
                        )

                        params = self.get_parameters(node)

                        label += (
                            f"\n{indent}└── "
                            f"🔹 [cyan]{prefix}[/cyan] "
                            f"{node.name}"
                            f"([dim green]{params}[/dim green])"
                        )

                        # Nested class/function
                        nested = [
                            child
                            for child in node.body
                            if isinstance(
                                child,
                                (
                                    ast.ClassDef,
                                    ast.FunctionDef,
                                    ast.AsyncFunctionDef,
                                ),
                            )
                        ]

                        if nested:
                            walk_nodes(
                                nested,
                                indent + "      ",
                            )

            # Start from module-level nodes
            walk_nodes(tree.body)

        except (
            SyntaxError,
            UnicodeDecodeError,
            OSError,
        ):
            pass

        return label

    # ---------------------------------------------------------
    # Build directory tree
    # ---------------------------------------------------------
    def build_tree(self, root, tree=None):

        if tree is None:
            project_name = Path.cwd().name
            root_name = project_name if root in (".", "") else root

            tree = Tree(
                f"[bold purple]📦 {root_name}"
            )

        entries = sorted(
            e
            for e in os.listdir(root)
            if e not in self.EXCLUDE_FILES
        )

        for entry in entries:

            # Skip selected files
            if entry in {
                "setup_env.py",
                "test_minimum.py",
            }:
                continue

            path = os.path.join(root, entry)
            desc = self.DESCRIPTIONS.get(entry, "")

            # -------------------------------------------------
            # DIRECTORY
            # -------------------------------------------------
            if os.path.isdir(path):

                folder_name = entry

                label = (
                    f"📂 {folder_name:<25}"
                    f"  {desc}"
                )

                subtree = tree.add(
                    f"[bold cyan]{label}[/bold cyan]"
                )

                self.build_tree(
                    path,
                    subtree,
                )

            # -------------------------------------------------
            # FILE
            # -------------------------------------------------
            else:

                file_size = os.path.getsize(path)

                file_name_with_size = (
                    f"{entry:<26}"
                    f"[green] 📦 "
                    f"{file_size / 1024:.2f} KB"
                    f"[/green]"
                )

                padded_entry = file_name_with_size.ljust(
                    self.MAX_FILENAME_WIDTH
                )

                # File icon
                if entry.endswith(".py"):
                    icon = "🐍"

                elif entry.endswith(".env"):
                    icon = "🔐"

                elif entry.endswith(".json"):
                    icon = "📦"

                elif entry.endswith(".toml"):
                    icon = "⚙️ "

                else:
                    icon = "📄"

                label = f"{icon} {padded_entry}"

                if desc:
                    label += (
                        f"  [dim]# {desc}[/dim]"
                    )

                # -------------------------------------------------
                # Python class/function information
                # only for selected files
                # -------------------------------------------------
                if (
                    path.endswith(".py")
                    and entry in self.SPECIFIC_FILES
                ):
                    label += self.fun_class(path)

                tree.add(
                    f"[green]{label}"
                )

        return tree

    # ---------------------------------------------------------
    # Run
    # ---------------------------------------------------------
    def run_tree(self, path):

        self.console.clear()

        root_folder = (
            os.path.basename(
                os.path.abspath(path)
            )
            or os.path.abspath(path)
        )

        self.console.rule(
            f"[bold green]📂 "
            f"{root_folder.upper()}"
        )

        tree = self.build_tree(path)

        self.console.print(tree)

    # ---------------------------------------------------------
    # CLI
    # ---------------------------------------------------------
    def main(self):

        parser = argparse.ArgumentParser(
            description=(
                "📦 Folder Power Tree Generator "
                "with Aligned Descriptions"
            )
        )

        parser.add_argument(
            "path",
            type=str,
            nargs="?",
            default=".",
            help=(
                "Root folder path "
                "(default: current directory)"
            ),
        )

        args = parser.parse_args()

        if os.path.exists(args.path):
            self.run_tree(args.path)
        else:
            self.console.print(
                "[red]❌ Error: "
                "Path does not exist![/red]"
            )


if __name__ == "__main__":
    ProjectTree().main()
