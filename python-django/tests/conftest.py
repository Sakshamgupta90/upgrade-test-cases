"""Minimal Django settings so the app's views and URLs can be tested on their own."""
import importlib.util
import sys
from pathlib import Path

import django
from django.conf import settings

APP_DIR = Path(__file__).resolve().parent.parent

# Load this folder as a package called "notes", so `from . import views` in urls.py works.
spec = importlib.util.spec_from_file_location("notes", APP_DIR / "__init__.py",
                                              submodule_search_locations=[str(APP_DIR)])
sys.modules["notes"] = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sys.modules["notes"])

settings.configure(
    DEBUG=True, SECRET_KEY="test", ROOT_URLCONF="notes.urls", ALLOWED_HOSTS=["*"], USE_TZ=True,
    MIDDLEWARE=[], INSTALLED_APPS=["django.contrib.contenttypes"], DATABASES={},
)
django.setup()
