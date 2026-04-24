from __future__ import annotations

from pathlib import Path

import pytest
from pptx import Presentation


@pytest.fixture
def tmp_yaml(tmp_path: Path):
    """Helper to create a temp YAML file with given content."""

    def _make(content: str, name: str = "test.yaml") -> Path:
        p = tmp_path / name
        p.write_text(content, encoding="utf-8")
        return p

    return _make


@pytest.fixture
def default_template(tmp_path: Path) -> Path:
    """Create a minimal default template for testing."""
    p = tmp_path / "template.pptx"
    prs = Presentation()
    prs.save(str(p))
    return p
