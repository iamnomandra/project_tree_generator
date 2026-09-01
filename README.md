# 📦 Project Tree Generator

🐍 A Rich-powered Python CLI that visualizes project structure, file sizes, classes, functions, nested definitions, and function parameters.

* 📂 Folder hierarchy
* 📄 File listing
* 📦 File sizes
* 📝 File/folder descriptions
* 🐍 Python file detection
* 🏛️ Python classes
* ⚙️ Functions and methods
* 🧩 Nested classes and functions
* 🔹 Function parameters
* 🔗 Class inheritance
* 🎨 Rich terminal formatting

---

## ✨ Features

### 📂 Directory Tree

Displays the complete project structure recursively while allowing specific files/folders to be excluded.

```text
📂 ingestion
📂 preprocessing
📂 classification
📂 extraction
📂 validation
📂 workflow
📂 storage
```

### 📄 File Information

Each file displays its type, name, size, and optional description.

```text
🐍 pipeline.py          📦 39.28 KB
📄 requirements.txt         📦 2.41 KB
📦 config.json              📦 1.82 KB
🔐 .env                     📦 0.91 KB
```

### 🐍 Python Code Structure

Selected Python files are parsed using Python's built-in `ast` module.

The tool extracts:

* Classes
* Nested classes
* Functions
* Methods
* Nested functions
* Function parameters
* Default parameter values
* `*args`
* `**kwargs`
* Async functions
* Base classes / inheritance

Example:

```text
📦 nom_idp
├── 🔐 .env                       📦 0.00 KB  # Project config like api key, url etc..
├── 🐍 __init__.py                📦 0.00 KB
├── 🐍 app.py                     📦 10.79 KB  # Entry point
🐍 pipeline.py          📦 39.28 KB
      └── Class: Pipeline
            └── def: __init__(self, config)
            └── def: process(self, document, debug=False)
            └── Class: PipelineError
                  └── def: __init__(self, message, code=None)      
      └── def: create_pipeline(config, debug=False)
            └── def: validate_config(config)
```

---

## 🧠 How It Works

The project uses Python's `ast` module to analyze `.py` files without executing them.

```text
Project Directory
        │
        ▼
   Directory Scan
        │
        ├── Folders
        │
        └── Files
              │
              └── *.py
                    │
                    ▼
                 AST Parser
                    │
                    ├── Classes
                    ├── Nested Classes
                    ├── Functions
                    ├── Methods
                    └── Parameters
                    │
                    ▼
               Rich Tree Output
```

---

## 📦 Requirements

Python 3.9+

Install the required dependency:

```bash
pip install rich
```

---

## 🚀 Usage

Run the script from your project directory:

```bash
python project_tree.py
```

Or provide a specific project path:

```bash
python project_tree.py /path/to/project
```

---

## ⚙️ Configuration

### Excluded Files/Folders

The following entries are ignored by default:

```python
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
```

Add or remove entries according to your project.

---

### Python Files to Analyze

Only the Python files listed in `SPECIFIC_FILES` will have their internal classes/functions displayed.

```python
SPECIFIC_FILES = {
    "pipeline.py",
    "app.py",
}
```

For example:

```python
SPECIFIC_FILES = {
    "pipeline.py",
    "app.py",
    "config.py",
    "state_machine.py",
}
```

This keeps the output readable for large projects.

---

## 📝 File Descriptions

Descriptions can be configured through the `DESCRIPTIONS` dictionary.

```python
DESCRIPTIONS = {
    "app.py": "Entry point",
    "config.py": "Project configuration",
    "pipeline.py": "Main orchestration engine",
    "ingestion": "→ Document to Receive/Load",
    "preprocessing": "→ Document to Clean/Prepare",
}
```

These descriptions are displayed beside the corresponding file or folder.

---

## 🏗️ Class Structure

The project is implemented as a single `ProjectTree` class.

```text
ProjectTree
│
├── get_parameters()
│
├── fun_class()
│
├── build_tree()
│
├── run_tree()
│
└── main()
```

### `get_parameters()`

Extracts function and method parameters from the AST.

Supports:

```python
def process(self, data, timeout=30):
    ...

def create(*args, **kwargs):
    ...

async def load(path, debug=False):
    ...
```

---

### `fun_class()`

Parses a Python file and builds its class/function hierarchy.

It does not execute the target Python file.

---

### `build_tree()`

Recursively scans folders and files and creates the Rich directory tree.

---

### `run_tree()`

Clears the console, displays the root project name, builds the tree, and renders it.

---

### `main()`

Provides the command-line interface using `argparse`.

---

## 🎨 Rich Formatting

The output uses [Rich](https://github.com/Textualize/rich) for terminal rendering.

Examples:

```text
🟣 Project Root
🔵 Folders
🟢 Files
🟡 Classes
🔷 Functions
```

Function parameters are intentionally displayed using a dimmed style so they remain readable without overpowering the function name.

---

## 🔒 Safe Code Inspection

Python source files are parsed using:

```python
ast.parse(source)
```

The source code is **not imported or executed** during inspection.

This makes the tool suitable for inspecting project structures without triggering application code.

---

## 📌 Example

Running:

```bash
python project_tree.py .
```

can produce an output similar to:

```text
────────────────── 📂 MYPROJECT ──────────────────

📦 myproject

├── 📂 ingestion
│   ├── 🐍 loader.py             📦 4.21 KB
│   └── 🐍 parser.py             📦 8.17 KB

├── 📂 preprocessing
│   └── 🐍 clean.py              📦 6.42 KB

├── 📂 workflow
│   └── 🐍 state_machine.py      📦 39.28 KB
│
│                    └── Class: StateMachine
│                          └── def: __init__(self, config)
│                          └── def: transition(self, state, event)
│                          └── Class: GuardRejectedError
│                                └── def: __init__(self, guard, state)
│
├── 🐍 nom_pipeline.py           📦 39.28 KB
│                    └── Class: NomPipeline
│                          └── def: __init__(self, config)
│                          └── def: process(self, document, debug=False)
│
├── 🐍 app.py                    📦 5.12 KB
│                    └── def: main(path=None)
│
└── 📄 requirements.txt          📦 1.24 KB
```

---

## 📁 Project Structure

A recommended layout:

```text
project-tree/
│
├── project_tree.py
├── README.md
└── requirements.txt
```

---

## 🛠️ Technology

Built with:

* **Python**
* **Rich**
* **AST (`ast`)**
* **Argparse**

No external parser or code execution engine is required.

---

## 📜 License

Add your preferred license here, for example:

```text
MIT License
```

---

## ⭐ Purpose

This utility is useful for quickly understanding large Python projects by combining **filesystem structure** with **Python code structure** in a single terminal view.

Instead of opening every Python file individually, you can quickly see:

```text
Project
  → Modules
      → Classes
          → Methods
              → Parameters
```

### 💬 Questions? Contributions?

- Feel free to open an **Issue** or start a **Discussion** on GitHub. 

--- 
 
> 🚀 Ready to improve your `CLI debugging`?
 
> 💡 Found this useful? Give it a ⭐ and share with your `Python friends`!

> 🖂 Contact me any help 
