from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


# TODO: check if this works properly
class PostSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        with open("db_blog.json", "r") as f:
            all_posts = json.load(f)["posts"]
        with open("db_archive.json", "r") as f:
            all_posts.append(json.load(f))

        return all_posts

    def lastmod(self, post):
        return post.date

    def priority(self, post):
        return 0.7 if post.suggested else 0.6


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
