import os

from django.conf import settings
from django.db import models
from django.utils import timezone


class PostTag(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, unique=True)


class Post(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=False, blank=False, max_length=200)
    is_archive = models.BooleanField(default=False)
    suggested = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    tags = models.ManyToManyField(PostTag, related_name="posts")

    def get_markdown_path(self):
        folder = "archive" if self.is_archive else "blog"
        return os.path.join(
            settings.BASE_DIR, "post-content", folder, f"{self.slug}/", "content.md"
        )

    def get_markdown_content(self):
        path = self.get_markdown_path()
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return f"Markdown file not found for slug ‘{self.slug}’"
