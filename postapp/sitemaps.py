from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from .models import Post


class PostSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return Post.objects.order_by("-date")

    def lastmod(self, obj):
        return obj.date

    def priority(self, obj):
        return 0.7 if obj.suggested else 0.6


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
