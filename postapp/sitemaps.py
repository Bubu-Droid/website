import json
from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from website.settings import BASE_DIR

BLOG_DB = BASE_DIR / "db_blog.json"
ARCHIVE_DB = BASE_DIR / "db_archive.json"


class PostSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        with BLOG_DB.open(mode="r", encoding="utf-8") as f:
            blog_posts = json.load(f)["posts"]
        with ARCHIVE_DB.open(mode="r", encoding="utf-8") as f:
            archive_posts = json.load(f)["posts"]

        all_posts = []
        for post in blog_posts:
            all_posts.append([post, "blog"])
        for post in archive_posts:
            all_posts.append([post, "archive"])

        return all_posts

    def location(self, item):
        if item[1] == "blog":
            return reverse("blog:post_detail", kwargs={"slug": item[0]["slug"]})

        return reverse("archive:post_detail", kwargs={"slug": item[0]["slug"]})

    def priority(self, item):
        return 0.7 if item[0]["suggested"] == "yes" else 0.6

    def lastmod(self, item):
        date_string = f"{item[0]['date']['month']} {item[0]['date']['year']}"
        parsed_date = datetime.strptime(date_string, "%B %Y")
        return parsed_date.date()


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return [
            "main:home_page",
            "main:calculus_page",
            "main:olympiads_page",
            "main:pet_peeves_page",
            "main:contact_page",
            "blog:post_index",
            "archive:post_index",
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return {
            "main:home_page": 1.0,
            "main:calculus_page": 0.9,
            "main:olympiads_page": 0.9,
            "main:pet_peeves_page": 0.9,
            "main:contact_page": 0.9,
            "blog:post_index": 0.8,
            "archive:post_index": 0.8,
        }.get(item, 0.5)
