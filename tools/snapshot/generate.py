#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


# ============================================================
# Project Snapshot Generator
# ============================================================

"""
Generate a single-file, developer-oriented project snapshot in Markdown.

Default behavior:
- Output file: `tools/snapshot/docs/PROJECT_SNAP.md`
- Include full repository structure
- Include full file contents for eligible files
- Exclude sensitive/local runtime artifacts

Security & hygiene guarantees:
- Local `.env*` files are excluded (except `.env.example`)
- Runtime/cache artifacts are excluded (`__pycache__`, `.pyc`, `.pyo`)
- Venv trees are excluded (`.venv`, `venv`, `ENV`)
- Git internals are excluded (`.git`)

This module is intended for maintainers and advanced users who want an
offline, auditable "project snapshot" artifact.
"""


# ============================================================
# Configuration Constants
# ============================================================

# File extensions excluded from full-content dumps by default.
DEFAULT_EXCLUDED_EXTENSIONS = {".md", ".png"}

# Directory names that should never be traversed during snapshot generation.
IGNORED_DIR_NAMES = {".git", "__pycache__", ".venv", "venv", "ENV"}

# Runtime-generated file suffixes that should never be included.
IGNORED_FILE_SUFFIXES = {".pyc", ".pyo"}

# Markdown syntax-highlighting hints for fenced code blocks.
LANGUAGE_BY_SUFFIX = {
    ".py": "python",
    ".txt": "text",
    ".json": "json",
    ".toml": "toml",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".sh": "bash",
}


# ============================================================
# Discovery Helpers
# ============================================================


def iter_project_files(root: Path) -> Iterable[Path]:
    """
    Yield repository files while filtering infrastructure/runtime artifacts.

    Filtering rules:
    - Skip non-file paths
    - Skip files inside ignored directories
    - Skip files with ignored suffixes
    """

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        if any(part in IGNORED_DIR_NAMES for part in path.parts):
            continue

        if path.suffix.lower() in IGNORED_FILE_SUFFIXES:
            continue

        yield path


def is_sensitive_env_file(path: Path) -> bool:
    """
    Return True for local secret env files.

    Included exception:
    - `.env.example` is explicitly allowed as a safe template reference.
    """

    return path.name.startswith(".env") and path.name != ".env.example"


# ============================================================
# Formatting Helpers
# ============================================================


def detect_lang(path: Path) -> str:
    """
    Detect Markdown code-fence language for readability.

    Notes:
    - `LICENSE` is presented as plain text.
    - `.env.example` is presented as `dotenv`.
    - Unknown extensions default to `text`.
    """

    if path.name == "LICENSE":
        return "text"

    if path.name == ".env.example":
        return "dotenv"

    return LANGUAGE_BY_SUFFIX.get(path.suffix.lower(), "text")


def normalize_extension(value: str) -> str:
    """
    Normalize user-provided extension values to `.ext` format.

    Examples:
    - `md` -> `.md`
    - `.png` -> `.png`
    """

    extension = value.strip().lower()
    if not extension:
        return extension

    if not extension.startswith("."):
        extension = f".{extension}"

    return extension


def anchor_for_path(path_text: str) -> str:
    """
    Convert a path string into a Markdown-anchor-friendly token.

    Used by the generated "File Index" section for quick navigation.
    """

    normalized = path_text.lower().replace("`", "")
    safe: list[str] = []

    for char in normalized:
        if char.isalnum() or char in {"-", "_", "."}:
            safe.append(char)
        elif char in {"/", " ", "\\"}:
            safe.append("-")

    return "".join(safe).strip("-")


# ============================================================
# Snapshot Builder
# ============================================================


def build_project_snap_content(
    root: Path,
    excluded_exts: set[str],
    output_relative_path: Path | None = None,
) -> str:
    """
    Build the complete Markdown body for the project snapshot artifact.

    The resulting document includes:
    - metadata and summary,
    - repository structure,
    - file index with anchors,
    - full file contents for included files,
    - skipped files list.
    """

    all_files = list(iter_project_files(root))

    # --------------------------------------------------------
    # Self-inclusion guard
    # --------------------------------------------------------
    # Ensure the generated output file does not become an input
    # to itself during the same generation pass.
    if output_relative_path is not None:
        output_rel = output_relative_path.as_posix()
        all_files = [
            path for path in all_files if path.relative_to(root).as_posix() != output_rel
        ]

    # --------------------------------------------------------
    # Inclusion / exclusion split
    # --------------------------------------------------------

    included = [
        path
        for path in all_files
        if path.suffix.lower() not in excluded_exts and not is_sensitive_env_file(path)
    ]

    skipped = [
        path
        for path in all_files
        if path.suffix.lower() in excluded_exts or is_sensitive_env_file(path)
    ]

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # --------------------------------------------------------
    # Markdown assembly
    # --------------------------------------------------------

    out: list[str] = []

    out.append("# PROJECT SNAP – Full Project Snapshot")
    out.append("")
    out.append(f"> Generated at: **{generated_at}**")
    out.append("")
    out.append(
        "This snapshot includes project content 1:1 except excluded extensions: "
        f"**{', '.join(sorted(excluded_exts))}**. "
        "Additionally, local secrets `.env*` are skipped "
        "(except `.env.example`)."
    )
    out.append("")

    out.append("## Summary")
    out.append("")
    out.append(f"- Total files in repository scope: **{len(all_files)}**")
    out.append(f"- Files with full content included: **{len(included)}**")
    out.append(f"- Skipped files: **{len(skipped)}**")
    out.append("")

    out.append("## Repository Structure")
    out.append("")
    for path in all_files:
        out.append(f"- `{path.relative_to(root).as_posix()}`")
    out.append("")

    out.append("## File Index (included content)")
    out.append("")
    for path in included:
        relative = path.relative_to(root).as_posix()
        out.append(f"- [`{relative}`](#{anchor_for_path(relative)})")
    out.append("")

    out.append("## File Contents")
    out.append("")
    for path in included:
        relative = path.relative_to(root).as_posix()
        lang = detect_lang(path)
        out.append(f"### `{relative}`")
        out.append("")

        try:
            content = path.read_text(encoding="utf-8")
            out.append(f"```{lang}")
            if content:
                out.append(content.rstrip("\n"))
            out.append("```")
        except UnicodeDecodeError:
            out.append("```text")
            out.append("[binary file omitted: cannot decode as UTF-8]")
            out.append("```")

        out.append("")

    out.append("## Skipped Files")
    out.append("")
    for path in skipped:
        out.append(f"- `{path.relative_to(root).as_posix()}`")

    return "\n".join(out) + "\n"


# ============================================================
# CLI Entry Point
# ============================================================


def main() -> None:
    """Parse CLI arguments and generate the project snapshot file."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="tools/snapshot/docs/PROJECT_SNAP.md",
        help=(
            "Output markdown path relative to project root "
            "(default: tools/snapshot/docs/PROJECT_SNAP.md)"
        ),
    )
    parser.add_argument(
        "--exclude-ext",
        action="append",
        default=None,
        help=(
            "File extension to exclude (repeatable), "
            "e.g. --exclude-ext .md or --exclude-ext md"
        ),
    )
    args = parser.parse_args()

    # Current file is: tools/snapshot/generate.py
    # Repository root is therefore three levels up.
    root = Path(__file__).resolve().parent.parent.parent

    raw_exts = args.exclude_ext or list(DEFAULT_EXCLUDED_EXTENSIONS)
    excluded_exts = {
        normalize_extension(ext) for ext in raw_exts if normalize_extension(ext)
    }

    output_relative_path = Path(args.output)

    content = build_project_snap_content(
        root=root,
        excluded_exts=excluded_exts,
        output_relative_path=output_relative_path,
    )

    output_path = (root / output_relative_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(
        f"Project snapshot generated: {output_path} "
        f"(excluded extensions: {', '.join(sorted(excluded_exts))})"
    )


if __name__ == "__main__":
    main()