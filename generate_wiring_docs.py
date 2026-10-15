#!/usr/bin/env python3
"""
generate_wiring_docs.py
=======================
Automated Codebase Wiring & Blast Radius Impact Generator.

Analyzes the entire codebase via Python AST:
1. Maps all modules, classes, and functions with exact line spans.
2. Traces cross-module call graphs, import dependencies, and API routes.
3. Maps database table read/write interactions.
4. Computes upstream & downstream ripple effects (blast radius) for every symbol.
5. Emits/updates SYSTEM_WIRING_AND_IMPACT.md automatically.

Can be run standalone:
    python generate_wiring_docs.py

Or installed as a git hook for automatic update on code changes:
    python generate_wiring_docs.py --install-hook
"""

import ast
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any

WORKSPACE = Path(__file__).parent.resolve()
OUTPUT_FILE = WORKSPACE / "SYSTEM_WIRING_AND_IMPACT.md"

# Files to exclude from deep wiring inspection
EXCLUDED_PATTERNS = [
    r"^\.pytest_cache",
    r"^backups",
    r"^output",
    r"^venv",
    r"^\.git",
    r"^__pycache__",
    r"^graft",
]


class CodeSymbol:
    def __init__(self, name: str, file_path: str, kind: str, start_line: int, end_line: int, docstring: str = "", args: List[str] = None):
        self.name = name
        self.file_path = file_path
        self.kind = kind  # "function", "class", "method", "endpoint"
        self.start_line = start_line
        self.end_line = end_line
        self.docstring = docstring or ""
        self.args = args or []
        self.calls: Set[str] = set()               # symbols called by this symbol
        self.called_by: Set[str] = set()            # symbols that call this symbol
        self.env_vars: Set[str] = set()             # env vars accessed
        self.db_tables: Set[str] = set()            # database tables touched
        self.route_info: str = ""                   # HTTP method + path if endpoint

    @property
    def qualified_name(self) -> str:
        return f"{self.file_path}::{self.name}"


class CodebaseAnalyzer:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.py_files = self._collect_python_files()
        self.symbols: Dict[str, CodeSymbol] = {}
        self.file_imports: Dict[str, Dict[str, str]] = defaultdict(dict)  # file -> {alias/name: source_module}
        self.routes: List[Dict[str, Any]] = []

    def _collect_python_files(self) -> List[Path]:
        files = []
        for p in self.root_dir.glob("*.py"):
            rel = p.relative_to(self.root_dir).as_posix()
            if any(re.match(pat, rel) for pat in EXCLUDED_PATTERNS):
                continue
            files.append(p)
        return sorted(files)

    def analyze(self):
        # Pass 1: Extract symbols and imports
        for p in self.py_files:
            self._parse_file_pass1(p)

        # Pass 2: Extract calls, env vars, and db queries
        for p in self.py_files:
            self._parse_file_pass2(p)

        # Pass 3: Invert call graph (build called_by)
        for sym_id, sym in self.symbols.items():
            for callee_name in sym.calls:
                # Resolve callee in same file or across symbols
                target_ids = self._resolve_callee(sym.file_path, callee_name)
                for tid in target_ids:
                    if tid in self.symbols:
                        self.symbols[tid].called_by.add(sym.qualified_name)

    def _parse_file_pass1(self, path: Path):
        rel_path = path.name
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except Exception:
            return

        for node in tree.body:
            # Imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.file_imports[rel_path][alias.asname or alias.name] = alias.name
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                for alias in node.names:
                    self.file_imports[rel_path][alias.asname or alias.name] = f"{mod}.{alias.name}"

            # Top-level Functions
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._record_func(node, rel_path)

            # Classes and methods
            elif isinstance(node, ast.ClassDef):
                doc = ast.get_docstring(node) or ""
                cls_sym = CodeSymbol(node.name, rel_path, "class", node.lineno, node.end_lineno or node.lineno, doc)
                self.symbols[cls_sym.qualified_name] = cls_sym

                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        method_name = f"{node.name}.{item.name}"
                        m_doc = ast.get_docstring(item) or ""
                        args = [a.arg for a in item.args.args]
                        m_sym = CodeSymbol(method_name, rel_path, "method", item.lineno, item.end_lineno or item.lineno, m_doc, args)
                        self.symbols[m_sym.qualified_name] = m_sym

    def _record_func(self, node: ast.AST, rel_path: str):
        doc = ast.get_docstring(node) or ""
        args = [a.arg for a in node.args.args]
        route_info = ""

        # Check for FastAPI route decorator: @app.get("/api/...")
        for dec in node.decorator_list:
            if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                if dec.func.attr in ("get", "post", "put", "delete", "patch"):
                    if dec.args and isinstance(dec.args[0], ast.Constant):
                        route_info = f"{dec.func.attr.upper()} {dec.args[0].value}"
                        self.routes.append({
                            "method": dec.func.attr.upper(),
                            "path": dec.args[0].value,
                            "function": node.name,
                            "file": rel_path,
                            "line": node.lineno
                        })

        sym = CodeSymbol(node.name, rel_path, "endpoint" if route_info else "function", node.lineno, node.end_lineno or node.lineno, doc, args)
        sym.route_info = route_info
        self.symbols[sym.qualified_name] = sym

    def _parse_file_pass2(self, path: Path):
        rel_path = path.name
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except Exception:
            return

        current_sym = None

        class Visitor(ast.NodeVisitor):
            def __init__(self, analyzer):
                self.analyzer = analyzer
                self.scope_stack = []

            def visit_FunctionDef(self, node):
                sym_id = f"{rel_path}::{node.name}"
                if len(self.scope_stack) > 0:
                    cls_name = self.scope_stack[-1]
                    sym_id = f"{rel_path}::{cls_name}.{node.name}"
                
                old_sym = self.analyzer.symbols.get(sym_id)
                self.scope_stack.append(node.name)
                self.generic_visit(node)
                self.scope_stack.pop()

            visit_AsyncFunctionDef = visit_FunctionDef

            def visit_ClassDef(self, node):
                self.scope_stack.append(node.name)
                self.generic_visit(node)
                self.scope_stack.pop()

            def visit_Call(self, node):
                # Detect symbol call
                callee_name = None
                if isinstance(node.func, ast.Name):
                    callee_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    callee_name = node.func.attr

                current_sym_id = self._current_sym_id()
                if current_sym_id and callee_name:
                    sym = self.analyzer.symbols.get(current_sym_id)
                    if sym:
                        sym.calls.add(callee_name)

                # Detect os.getenv
                if isinstance(node.func, ast.Attribute) and node.func.attr in ("getenv",):
                    if node.args and isinstance(node.args[0], ast.Constant):
                        current_sym_id = self._current_sym_id()
                        if current_sym_id:
                            sym = self.analyzer.symbols.get(current_sym_id)
                            if sym:
                                sym.env_vars.add(str(node.args[0].value))

                # Detect SQL execute
                if isinstance(node.func, ast.Attribute) and node.func.attr in ("execute", "executemany"):
                    if node.args and isinstance(node.args[0], ast.Constant):
                        sql = str(node.args[0].value).lower()
                        tables = re.findall(r'(?:from|into|update|join)\s+["`]?([a-z0-9_]+)["`]?', sql)
                        current_sym_id = self._current_sym_id()
                        if current_sym_id:
                            sym = self.analyzer.symbols.get(current_sym_id)
                            if sym:
                                sym.db_tables.update(tables)

                self.generic_visit(node)

            def _current_sym_id(self):
                if not self.scope_stack:
                    return None
                if len(self.scope_stack) == 1:
                    return f"{rel_path}::{self.scope_stack[0]}"
                return f"{rel_path}::{self.scope_stack[0]}.{self.scope_stack[1]}"

        Visitor(self).visit(tree)

    def _resolve_callee(self, from_file: str, callee_name: str) -> List[str]:
        # Same file
        same_file_id = f"{from_file}::{callee_name}"
        if same_file_id in self.symbols:
            return [same_file_id]

        # Check imports of this file
        matches = []
        for sym_id, sym in self.symbols.items():
            if sym.name == callee_name:
                matches.append(sym_id)
        return matches

    def compute_blast_radius(self, qualified_name: str, max_depth: int = 2) -> Dict[int, Set[str]]:
        """Calculates upstream dependents (who is affected if this symbol changes)."""
        visited = defaultdict(set)
        queue = [(qualified_name, 0)]
        seen = {qualified_name}

        while queue:
            curr, depth = queue.pop(0)
            if depth >= max_depth:
                continue
            sym = self.symbols.get(curr)
            if not sym:
                continue
            for caller in sym.called_by:
                if caller not in seen:
                    seen.add(caller)
                    visited[depth + 1].add(caller)
                    queue.append((caller, depth + 1))
        return visited


def generate_markdown(analyzer: CodebaseAnalyzer) -> str:
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Master Codebase Wiring, Architecture & Ripple-Impact Blueprint",
        "",
        "> **Auto-Generated Verification Document**  ",
        f"> **Last Code Synchronization**: `{now_str}`  ",
        f"> **Analyzed Modules**: `{len(analyzer.py_files)} Python Files` | `{len(analyzer.symbols)} Symbols` | `{len(analyzer.routes)} REST Endpoints`  ",
        "",
        "---",
        "",
        "## 1. System High-Level Topology & Data Pipelines",
        "",
        "The repository operates across 5 decoupled operational layers:",
        "",
        "```mermaid",
        "flowchart TD",
        '    subgraph Ingestion["1. Ingestion Layer"]',
        '        CRM["crm_downloader.py (Softcode/Prepaid CRM)"]',
        '        RawUpload["web_server.py /api/complaints/upload-raw"]',
        '        SRUpload["web_server.py /api/service-request/upload-raw"]',
        "    end",
        "",
        '    subgraph Core["2. Data Processing & Computation Engine"]',
        '        Filter["data_processor.py (Filter rules)"]',
        '        Calc["report_engine.py (Complaint Math Parity)"]',
        '        SRCalc["service_request_engine.py (SR Math Engine)"]',
        '        Layout["report_layout.py (Row & Area Keys)"]',
        "    end",
        "",
        '    subgraph Graphics["3. Graphic Rendering Layer (High-DPI)"]',
        '        Playwright["Playwright Chromium Browser (Scale 2.5x)"]',
        '        ReportGen["report_image_generator.py (Complaint Retina Cards)"]',
        '        SRReportGen["service_request_engine.py (SR Retina Cards)"]',
        "    end",
        "",
        '    subgraph Delivery["4. Notification & Dispatch Layer"]',
        '        WA["whatsapp_sender.py (WhatsApp Web Automation)"]',
        '        TG["telegram_bot.py (Telegram Remote Ops Bot)"]',
        "    end",
        "",
        '    subgraph Persistence["5. Storage, State & Scheduling Layer"]',
        '        DB["db_manager.py (SQLite: regions.db)"]',
        '        Sched["scheduler_utils.py / main.py (24/7 Scheduler)"]',
        '        Log["logger_setup.py (3-Day Rotating Logs)"]',
        "    end",
        "",
        "    CRM --> Filter --> Calc --> ReportGen --> WA",
        "    CRM --> SRCalc --> SRReportGen --> WA",
        "    RawUpload --> Calc",
        "    SRUpload --> SRCalc",
        "    TG --> DB",
        "    Sched --> CRM",
        "    ReportGen --> Log",
        "    WA --> Log",
        "```",
        "",
        "---",
        "",
        "## 2. Core Modules: Detailed Line-by-Line Wiring & Call Mapping",
        ""
    ]

    # Group symbols by module
    by_file = defaultdict(list)
    for sym_id, sym in sorted(analyzer.symbols.items()):
        by_file[sym.file_path].append(sym)

    for file_name in sorted(by_file.keys()):
        syms = by_file[file_name]
        lines.append(f"### `{file_name}`")
        lines.append("")
        lines.append("| Symbol | Type | Line Span | Primary Responsibility | Downstream Calls | Direct Callers |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")

        for s in syms:
            doc_brief = (s.docstring.strip().split("\n")[0] if s.docstring else "—").replace("|", "\\|")
            if s.route_info:
                doc_brief = f"`{s.route_info}` {doc_brief}"
            calls_str = f"`{len(s.calls)}` callee(s)" if s.calls else "0"
            called_by_str = f"`{len(s.called_by)}` caller(s)" if s.called_by else "0 (Entrypoint)"
            lines.append(f"| [`{s.name}`](file:///{WORKSPACE.as_posix()}/{s.file_path}#L{s.start_line}-L{s.end_line}) | {s.kind} | `L{s.start_line}-L{s.end_line}` | {doc_brief} | {calls_str} | {called_by_str} |")

        lines.append("")

    lines.extend([
        "---",
        "",
        "## 3. Ripple Effect & Blast Radius (What Happens if Code Changes?)",
        "",
        "This section documents the upstream cascading impact if any core function or component signature is modified.",
        "",
        "| Core Function / Component | Direct Impact (Hop 1) | Transitive Cascading Impact (Hop 2) | Critical Failure Risk & Invariants |",
        "| :--- | :--- | :--- | :--- |"
    ])

    # Select critical hub symbols for blast radius display
    critical_symbols = [
        "config.py::resolve_target_excel_path",
        "db_manager.py::get_connection",
        "db_manager.py::get_team_leaders",
        "db_manager.py::get_acsos",
        "crm_downloader.py::download_from_crm",
        "crm_downloader.py::download_service_requests_from_crm",
        "data_processor.py::filter_adl",
        "data_processor.py::filter_adtv",
        "data_processor.py::filter_prepaid",
        "data_processor.py::ensure_region_directory_ready",
        "report_engine.py::compute_report",
        "report_layout.py::get_layout_for_region",
        "service_request_engine.py::compute_service_request_reports",
        "service_request_engine.py::render_sr_report_images",
        "report_image_generator.py::generate_report_images",
        "whatsapp_sender.py::flash_report_image",
        "telegram_bot.py::TelegramBotRunner",
        "web_server.py::upload_complaints_raw_endpoint",
        "web_server.py::upload_service_request_raw_endpoint",
    ]

    for sym_id in critical_symbols:
        sym = analyzer.symbols.get(sym_id)
        if not sym:
            continue
        blast = analyzer.compute_blast_radius(sym_id, max_depth=2)
        hop1 = ", ".join(f"`{c.split('::')[-1]}`" for c in sorted(list(blast[1])[:5])) or "None"
        if len(blast[1]) > 5:
            hop1 += f" (+{len(blast[1])-5} more)"
        hop2 = ", ".join(f"`{c.split('::')[-1]}`" for c in sorted(list(blast[2])[:5])) or "None"
        if len(blast[2]) > 5:
            hop2 += f" (+{len(blast[2])-5} more)"

        # Define invariant/risk
        risk_map = {
            "get_connection": "Deadlock / database locked if connection is uncommitted or unclosed. Must use PRAGMA foreign_keys = ON.",
            "download_from_crm": "Stale dispatch risk if allow_stale policy is breached. Must enforce regional query filters.",
            "compute_report": "Calculation divergence from gold-standard Excel parity. Breaks daily QoS metrics.",
            "compute_service_request_reports": "Service Request report failure or wrong region filtering if region_id is omitted.",
            "flash_report_image": "WhatsApp Web session crash, modal block, or duplicate message flooding.",
            "ensure_region_directory_ready": "Prevents invalid report rendering when employee codes don't match the database.",
            "get_layout_for_region": "Breaks all TL / ACSO row alignments and Excel export formulas.",
            "upload_complaints_raw_endpoint": "Cross-region data pollution if region_id is not passed or defaults incorrectly.",
        }
        risk = risk_map.get(sym.name, "Signature mismatch breaks dependent calling workflows.")

        lines.append(f"| `{sym.file_path}::{sym.name}` | {hop1} | {hop2} | {risk} |")

    lines.extend([
        "",
        "---",
        "",
        "## 4. REST API Endpoints Wiring Table",
        "",
        "| Method | Endpoint Path | Handler Function | File | Line |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ])

    for r in sorted(analyzer.routes, key=lambda x: (x["path"], x["method"])):
        lines.append(f"| `{r['method']}` | `{r['path']}` | [`{r['function']}`](file:///{WORKSPACE.as_posix()}/{r['file']}#L{r['line']}) | `{r['file']}` | `L{r['line']}` |")

    lines.extend([
        "",
        "---",
        "",
        "## 5. Automated Documentation Synchronization (How to Keep Wiring Updated)",
        "",
        "To ensure that this wiring blueprint **never becomes stale** when future code edits are made:",
        "",
        "### Automatic Git Post-Commit Hook",
        "Whenever a developer or agent commits changes to git, this document regenerates automatically via `.git/hooks/post-commit`:",
        "```bash",
        "python generate_wiring_docs.py",
        "```",
        "",
        "### Graft Repository Knowledge Graph Sync",
        "This repository is also fully synchronized with `graft/`: small linked markdown nodes that verify symbols and line numbers via:",
        "```bash",
        "graft build",
        "```",
        "",
        "### Verification Test Suite",
        "Before deploying any changes to production, run the automated test suite:",
        "```bash",
        "pytest -v",
        "```",
        ""
    ])

    return "\n".join(lines)


def install_git_hook():
    hooks_dir = WORKSPACE / ".git" / "hooks"
    if not hooks_dir.exists():
        print(f"[!] .git/hooks directory not found at {hooks_dir}")
        return False

    hook_file = hooks_dir / "post-commit"
    hook_script = f"""#!/bin/sh
# Auto-update wiring documentation on every commit
python "{WORKSPACE / 'generate_wiring_docs.py'}"
"""
    hook_file.write_text(hook_script, encoding="utf-8")
    print(f"[+] Installed automated git post-commit hook at: {hook_file}")
    return True


def main():
    print("=" * 60)
    print("Codebase Wiring & Blast Radius Generator")
    print("=" * 60)

    if "--install-hook" in sys.argv:
        install_git_hook()

    print("[1/3] Parsing Python AST across codebase...")
    analyzer = CodebaseAnalyzer(WORKSPACE)
    analyzer.analyze()
    print(f"      Parsed {len(analyzer.py_files)} files, {len(analyzer.symbols)} symbols, {len(analyzer.routes)} endpoints.")

    print("[2/3] Generating Master Wiring Markdown...")
    md_content = generate_markdown(analyzer)

    print(f"[3/3] Writing to {OUTPUT_FILE}...")
    OUTPUT_FILE.write_text(md_content, encoding="utf-8")
    print(f"[OK] Successfully generated {OUTPUT_FILE.name} ({len(md_content)} bytes).")
    print("=" * 60)


if __name__ == "__main__":
    main()
