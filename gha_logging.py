import logging
import os
import sys
from contextlib import contextmanager

__all__ = [
    "setup_logging",
    "gha_group",
    "gha_mask_env",
]


class GitHubActionsFormatter(logging.Formatter):
    """Format logs using GitHub Actions workflow commands."""

    def format(self, record):
        msg = super().format(record)
        if record.levelno >= logging.ERROR:
            return f"::error file={record.pathname},line={record.lineno}::{msg}"
        elif record.levelno >= logging.WARNING:
            return f"::warning::{msg}"
        elif record.levelno >= logging.INFO:
            return f"::notice::{msg}"
        return msg


def _setup_gha_formatter(level: int):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(GitHubActionsFormatter("%(levelname)s: %(message)s"))
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)


def _setup_plain_formatter(level: int):
    # Nice local console format
    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    datefmt = "%H:%M:%S"
    logging.basicConfig(
        level=level,
        format=fmt,
        datefmt=datefmt,
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def setup_logging(level=logging.INFO, force_gha: bool | None = None):
    """
    Initialize logging. If running in GitHub Actions (GITHUB_ACTIONS=true)
    use GH-A annotations; otherwise use a plain console formatter.

    force_gha=True/False overrides auto-detection.
    """
    in_gha = os.getenv("GITHUB_ACTIONS", "").lower() == "true"
    use_gha = force_gha if force_gha is not None else in_gha
    if use_gha:
        _setup_gha_formatter(level)
    else:
        _setup_plain_formatter(level)


@contextmanager
def gha_group(title: str):
    """
    Create a collapsible group in GitHub Actions logs.
    No-op grouping locally (still prints a header line).
    """
    in_gha = os.getenv("GITHUB_ACTIONS", "").lower() == "true"
    if in_gha:
        print(f"::group::{title}")
    else:
        print(f"\n=== {title} ===")
    try:
        yield
    finally:
        if in_gha:
            print("::endgroup::")


def gha_mask_env(*names: str):
    """Mask sensitive env vars so they appear as *** in GitHub Actions logs."""
    if os.getenv("GITHUB_ACTIONS", "").lower() != "true":
        return
    for name in names:
        val = os.getenv(name)
        if val:
            print(f"::add-mask::{val}")
