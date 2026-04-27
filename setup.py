"""Custom setup.py to handle wiki directory inclusion for PyPI distribution.

This file extends setuptools to copy the wiki directory from the repo root
into the packaged help tree during the build process, ensuring it's included in PyPI distributions.

Note: When using setuptools.build_meta (pyproject.toml), this file is automatically
detected and used for custom build commands.
"""

from __future__ import annotations

import os
import shutil
import stat

from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist


def _handle_remove_readonly(func, path, exc_info):
    """Retry read-only deletions on Windows worktrees."""
    del exc_info
    os.chmod(path, stat.S_IWRITE)
    func(path)


def _refresh_wiki_tree(setup_dir: Path) -> None:
    """Copy the root wiki into the packaged help tree without VCS metadata."""
    repo_root = setup_dir.parent.parent
    wiki_src = repo_root / "wiki"
    wiki_dest = setup_dir / "src" / "toolset" / "help" / "wiki"

    if not wiki_src.exists() or not wiki_src.is_dir():
        return

    if wiki_dest.exists():
        shutil.rmtree(wiki_dest, onerror=_handle_remove_readonly)

    shutil.copytree(
        wiki_src,
        wiki_dest,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(".git", ".gitignore", "__pycache__"),
    )
    print(f"Copied wiki directory from {wiki_src} to {wiki_dest}")


class BuildPyWithWiki(build_py):
    """Custom build_py that copies wiki directory before building."""

    def run(self):
        """Copy wiki directory to src/toolset/help/wiki before building (idempotent)."""
        setup_dir = Path(__file__).parent
        _refresh_wiki_tree(setup_dir)
        super().run()


class SDistWithWiki(sdist):
    """Custom sdist that ensures wiki is included in source distribution."""

    def run(self):
        """Copy wiki directory before processing MANIFEST.in (which happens in super().run())."""
        setup_dir = Path(__file__).parent
        _refresh_wiki_tree(setup_dir)

        # Run standard sdist (processes MANIFEST.in, which will now find src/toolset/help/wiki)
        # NOTE: make_release_tree() is NOT overridden because wiki is already included
        # via MANIFEST.in from src/toolset/help/wiki. Overriding it would cause duplication
        # (wiki would appear both in src/toolset/help/wiki/ and wiki/ in the distribution).
        super().run()


# Setup configuration is read from pyproject.toml
# This file provides custom build commands
if __name__ == "__main__":
    setup(
        cmdclass={
            "build_py": BuildPyWithWiki,
            "sdist": SDistWithWiki,
        }
    )
