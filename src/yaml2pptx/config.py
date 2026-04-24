from pathlib import Path

PACKAGE_DIR = Path(__file__).parent
TEMPLATES_DIR = PACKAGE_DIR.parent.parent / "templates"
DEFAULT_TEMPLATE = TEMPLATES_DIR / "default.pptx"
