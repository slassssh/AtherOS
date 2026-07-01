from pathlib import Path

PROJECT_NAME = "AtherOS"
VERSION = "0.1.0"

ROOT_DIR = Path(__file__).resolve().parents[3]

BACKEND_DIR = ROOT_DIR / "backend"

APP_DIR = BACKEND_DIR / "app"

TESTS_DIR = BACKEND_DIR / "tests"

DOCS_DIR = ROOT_DIR / "docs"