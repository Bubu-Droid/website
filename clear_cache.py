import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()

from django.core.cache import cache

cache.clear()
print("All cache cleared.")
