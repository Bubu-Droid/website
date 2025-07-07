import calendar

from django.test import TestCase
from django.urls import reverse

from .models import Post, PostTag


def create_post(title, slug, tags=None, is_archive=False, suggested=False):
    """Utility function to create a Post object with
    optional tags and archive flag."""
    post = Post.objects.create(
        title=title, slug=slug, is_archive=is_archive, suggested=suggested
    )
    if tags:
        post.tags.set(tags)
    return post


def create_tag(name):
    tag = PostTag.objects.create(name=name)
    return tag


class BlogIndexViewTests(TestCase):
    def test_blog_index_no_posts(self):
        response = self.client.get(reverse("blog:post_index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blog Posts")
        self.assertContains(response, "No posts yet!")
        self.assertQuerySetEqual(response.context["post_list"], [])

    def test_post_timeline_no_posts(self):
        response = self.client.get(reverse("blog:post_index"))
        self.assertNotContains(response, "Post Timeline")
        self.assertEqual(response.context["post_timeline"], {})

    def test_tag_list_no_posts(self):
        response = self.client.get(reverse("blog:post_index"))
        self.assertNotContains(response, "Tag List")
        self.assertQuerySetEqual(response.context["tag_list"], [])

    def test_suggested_reads_no_post(self):
        response = self.client.get(reverse("blog:post_index"))
        self.assertNotContains(response, "Suggested Reads")
        self.assertQuerySetEqual(response.context["suggested_posts"], [])

    def test_blog_index_multiple_posts(self):
        post1 = create_post("Post Title 1", "post-title-1")
        post2 = create_post("Post Title 2", "post-title-2")
        response = self.client.get(reverse("blog:post_index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["post_list"], [post1, post2])

    def test_tags_in_post(self):
        math_tag = create_tag("math")
        cs_tag = create_tag("cs")
        post = create_post("Post Title", "post-title", [math_tag])
        response = self.client.get(reverse("blog:post_index"))
        target_post = response.context["post_list"][0]
        self.assertIn(math_tag, target_post.tags.all())
        self.assertNotIn(cs_tag, target_post.tags.all())

    def test_post_timeline_with_post(self):
        post = create_post("Post Title", "post-title")
        response = self.client.get(reverse("blog:post_index"))
        timeline = response.context["post_timeline"]
        flattened_title = [
            p.title
            for year_val in timeline.values()
            for month_posts in year_val.values()
            for p in month_posts
        ]
        flattened_year = timeline.keys()
        flattened_month = [
            month for year_val in timeline.values() for month in year_val.keys()
        ]

        self.assertIn(post.title, flattened_title)
        year_const = str(post.date.year)
        month_const = str(calendar.month_name[post.date.month])
        self.assertIn(year_const, flattened_year)
        self.assertIn(month_const, flattened_month)

    def test_tag_list_with_post(self):
        math_tag = create_tag("math")
        cs_tag = create_tag("cs")
        post = create_post("Post Title", "post-title", tags=[math_tag])
        response = self.client.get(reverse("blog:post_index"))
        tag_list = response.context["tag_list"]
        self.assertIn(math_tag, tag_list)
        self.assertNotIn(cs_tag, tag_list)

    def test_suggested_reads_with_post(self):
        post1 = create_post("Post 1", "post-1", suggested=True)
        post2 = create_post("Post 2", "post-2", suggested=False)
        response = self.client.get(reverse("blog:post_index"))
        suggest_list = response.context["suggested_posts"]
        self.assertIn(post1, suggest_list)
        self.assertNotIn(post2, suggest_list)

    def test_tag_view_sidebar_counts(self):
        math_tag = create_tag("math")
        cs_tag = create_tag("cs")
        create_post("Tagged Once", "once", tags=[math_tag])
        create_post("Tagged Twice", "twice", tags=[math_tag, cs_tag])
        response = self.client.get(reverse("blog:post_index"))
        tags = response.context["tag_list"]
        math_tag = next(t for t in tags if t.name == math_tag.name)
        cs_tag = next(t for t in tags if t.name == "cs")
        self.assertEqual(math_tag.num_posts, 2)
        self.assertEqual(cs_tag.num_posts, 1)

    def test_tag_filter_sidebar_only_shows_namespace_tags(self):
        tag1 = create_tag("A")
        tag2 = create_tag("B")
        create_post("Post A", "a", tags=[tag1])
        create_post("Post B", "b", tags=[tag2], is_archive=True)
        response = self.client.get(reverse("blog:post_tag", args=["A"]))
        tag_names = {tag.name for tag in response.context["tag_list"]}
        self.assertIn("A", tag_names)
        self.assertNotIn("B", tag_names)

    def test_tag_name_uniqueness(self):
        create_tag("math")
        with self.assertRaises(Exception):
            create_tag("math")


class BlogTagViewTests(TestCase):
    def test_tag_view_with_multiple_posts(self):
        math_tag = create_tag("math")
        cs_tag = create_tag("cs")
        post1 = create_post("Post 1", "post-1", tags=[math_tag])
        post2 = create_post("Post 2", "post-2", tags=[math_tag, cs_tag])
        post3 = create_post("Post 3", "post-3", tags=[cs_tag])
        response = self.client.get(reverse("blog:post_tag", args=[math_tag]))
        self.assertEqual(response.status_code, 200)
        tgt_post_list = response.context["post_list"]
        self.assertIn(post1, tgt_post_list)
        self.assertIn(post2, tgt_post_list)
        self.assertNotIn(post3, tgt_post_list)

    def test_tag_view_with_wrong_tag(self):
        response = self.client.get(reverse("blog:post_tag", args=["incorrect_tag"]))
        self.assertEqual(response.status_code, 404)


class BlogDetailViewTests(TestCase):
    def test_detail_view_check_sidebar(self):
        cs_tag = create_tag("cs")
        post = create_post("Post Title", "post-title", tags=[cs_tag], suggested=True)
        response = self.client.get(reverse("blog:post_detail", args=[post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Tag List")
        self.assertNotContains(response, "Suggested Reads")
        self.assertNotContains(response, "Post Timeline")

    def test_detail_view_tags(self):
        math_tag = create_tag("math")
        cs_tag = create_tag("cs")
        post = create_post("Post Title", "post-title", tags=[cs_tag])
        post_new = create_post("New Post Title", "new-post-title", tags=[math_tag])
        response = self.client.get(reverse("blog:post_detail", args=[post.slug]))
        target_post = response.context["post"]
        self.assertIn(cs_tag, target_post.tags.all())
        self.assertNotIn(math_tag, target_post.tags.all())

    def test_detail_no_other_posts(self):
        math_tag = create_tag("math")
        cs_tag = create_tag("cs")
        post = create_post("Post Title", "post-title", tags=[cs_tag])
        post_new = create_post("New Post Title", "new-post-title", tags=[math_tag])
        response = self.client.get(reverse("blog:post_detail", args=[post.slug]))
        self.assertNotContains(response, post_new.title)

    def test_detail_wrong_slug(self):
        post = create_post("Post Title", "post-title")
        response = self.client.get(reverse("blog:post_detail", args=["incorrect-slug"]))
        self.assertEqual(response.status_code, 404)

    def test_detail_slug_edge_case(self):
        post = create_post("INMO 2025 Review", "inmo-2025-review")
        response = self.client.get(reverse("blog:post_detail", args=[post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "INMO 2025 Review")

    def test_slug_uniqueness(self):
        create_post("Post A", "same-slug")
        with self.assertRaises(Exception):
            create_post("Post B", "same-slug")


class NamespaceIndexViewTest(TestCase):
    def test_index_post_in_correct_namespace(self):
        blog_post = create_post("Blog Post", "blog-post")
        archive_post = create_post("Archive Post", "archive-post", is_archive=True)
        blog_response = self.client.get(reverse("blog:post_index"))
        archive_response = self.client.get(reverse("archive:post_index"))
        self.assertIn(blog_post, blog_response.context["post_list"])
        self.assertIn(archive_post, archive_response.context["post_list"])
        self.assertNotIn(blog_post, archive_response.context["post_list"])
        self.assertNotIn(archive_post, blog_response.context["post_list"])


class NamespaceDetailViewTest(TestCase):
    def test_detail_post_in_correct_namespace(self):
        blog_post = create_post("Blog Post", "blog-post")
        archive_post = create_post("Archive Post", "archive-post", is_archive=True)
        blog_response = self.client.get(
            reverse("blog:post_detail", args=[blog_post.slug])
        )
        archive_response = self.client.get(
            reverse("archive:post_detail", args=[archive_post.slug])
        )
        self.assertEqual(blog_response.context["post"], blog_post)
        self.assertEqual(archive_response.context["post"], archive_post)
        self.assertNotEqual(blog_response.context["post"], archive_post)
        self.assertNotEqual(archive_response.context["post"], blog_post)


class NamespaceTagViewTest(TestCase):
    def test_tag_post_in_correct_namespace(self):
        math_tag = create_tag("math")
        blog_post = create_post("Blog Post", "blog-post", tags=[math_tag])
        archive_post = create_post(
            "Archive Post", "archive-post", tags=[math_tag], is_archive=True
        )
        blog_response = self.client.get(reverse("blog:post_tag", args=[math_tag]))
        archive_response = self.client.get(reverse("archive:post_tag", args=[math_tag]))
        self.assertIn(blog_post, blog_response.context["post_list"])
        self.assertIn(archive_post, archive_response.context["post_list"])
        self.assertNotIn(blog_post, archive_response.context["post_list"])
        self.assertNotIn(archive_post, blog_response.context["post_list"])


class ArchiveIndexViewTests(TestCase):
    def test_archive_index_no_posts(self):
        response = self.client.get(reverse("archive:post_index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Archive Posts")
        self.assertContains(response, "No posts yet!")
        self.assertQuerySetEqual(response.context["post_list"], [])

    def test_post_timeline_no_posts(self):
        response = self.client.get(reverse("archive:post_index"))
        self.assertNotContains(response, "Post Timeline")
        self.assertEqual(response.context["post_timeline"], {})

    def test_tag_list_no_posts(self):
        response = self.client.get(reverse("archive:post_index"))
        self.assertNotContains(response, "Tag List")
        self.assertQuerySetEqual(response.context["tag_list"], [])

    def test_suggested_reads_no_post(self):
        response = self.client.get(reverse("archive:post_index"))
        self.assertNotContains(response, "Suggested Reads")
        self.assertQuerySetEqual(response.context["suggested_posts"], [])

    def test_archive_index_multiple_posts(self):
        post1 = create_post("Post Title 1", "post-title-1", is_archive=True)
        post2 = create_post("Post Title 2", "post-title-2", is_archive=True)
        response = self.client.get(reverse("archive:post_index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["post_list"], [post1, post2])

    def test_tags_in_post(self):
        math_tag = create_tag("math")
        cs_tag = create_tag("cs")
        post = create_post("Post Title", "post-title", [math_tag], is_archive=True)
        response = self.client.get(reverse("archive:post_index"))
        target_post = response.context["post_list"][0]
        self.assertIn(math_tag, target_post.tags.all())
        self.assertNotIn(cs_tag, target_post.tags.all())

    def test_post_timeline_with_post(self):
        post = create_post("Post Title", "post-title", is_archive=True)
        response = self.client.get(reverse("archive:post_index"))
        timeline = response.context["post_timeline"]
        flattened_title = [
            p.title
            for year_val in timeline.values()
            for month_posts in year_val.values()
            for p in month_posts
        ]
        flattened_year = timeline.keys()
        flattened_month = [
            month for year_val in timeline.values() for month in year_val.keys()
        ]

        self.assertIn(post.title, flattened_title)
        year_const = str(post.date.year)
        month_const = str(calendar.month_name[post.date.month])
        self.assertIn(year_const, flattened_year)
        self.assertIn(month_const, flattened_month)

    def test_tag_list_with_post(self):
        math_tag = create_tag("math")
        cs_tag = create_tag("cs")
        post = create_post("Post Title", "post-title", tags=[math_tag], is_archive=True)
        response = self.client.get(reverse("archive:post_index"))
        tag_list = response.context["tag_list"]
        self.assertIn(math_tag, tag_list)
        self.assertNotIn(cs_tag, tag_list)

    def test_suggested_reads_with_post(self):
        post1 = create_post("Post 1", "post-1", suggested=True, is_archive=True)
        post2 = create_post("Post 2", "post-2", suggested=False, is_archive=True)
        response = self.client.get(reverse("archive:post_index"))
        suggest_list = response.context["suggested_posts"]
        self.assertIn(post1, suggest_list)
        self.assertNotIn(post2, suggest_list)

    def test_tag_view_sidebar_counts(self):
        math_tag = create_tag("math")
        cs_tag = create_tag("cs")
        create_post("Tagged Once", "once", tags=[math_tag], is_archive=True)
        create_post("Tagged Twice", "twice", tags=[math_tag, cs_tag], is_archive=True)
        response = self.client.get(reverse("archive:post_index"))
        tags = response.context["tag_list"]
        math_tag = next(t for t in tags if t.name == math_tag.name)
        cs_tag = next(t for t in tags if t.name == "cs")
        self.assertEqual(math_tag.num_posts, 2)
        self.assertEqual(cs_tag.num_posts, 1)

    def test_tag_filter_sidebar_only_shows_namespace_tags(self):
        tag1 = create_tag("A")
        tag2 = create_tag("B")
        create_post("Post A", "a", tags=[tag1], is_archive=True)
        create_post("Post B", "b", tags=[tag2], is_archive=False)
        response = self.client.get(reverse("archive:post_tag", args=["A"]))
        tag_names = {tag.name for tag in response.context["tag_list"]}
        self.assertIn("A", tag_names)
        self.assertNotIn("B", tag_names)

    def test_tag_name_uniqueness(self):
        create_tag("math")
        with self.assertRaises(Exception):
            create_tag("math")


class ArchiveTagViewTests(TestCase):
    def test_tag_view_with_multiple_posts(self):
        math_tag = create_tag("math")
        cs_tag = create_tag("cs")
        post1 = create_post("Post 1", "post-1", tags=[math_tag], is_archive=True)
        post2 = create_post(
            "Post 2", "post-2", tags=[math_tag, cs_tag], is_archive=True
        )
        post3 = create_post("Post 3", "post-3", tags=[cs_tag], is_archive=True)
        response = self.client.get(reverse("archive:post_tag", args=[math_tag]))
        self.assertEqual(response.status_code, 200)
        tgt_post_list = response.context["post_list"]
        self.assertIn(post1, tgt_post_list)
        self.assertIn(post2, tgt_post_list)
        self.assertNotIn(post3, tgt_post_list)

    def test_tag_view_with_wrong_tag(self):
        response = self.client.get(reverse("archive:post_tag", args=["incorrect_tag"]))
        self.assertEqual(response.status_code, 404)


class ArchiveDetailViewTests(TestCase):
    def test_detail_view_check_sidebar(self):
        cs_tag = create_tag("cs")
        post = create_post(
            "Post Title", "post-title", tags=[cs_tag], suggested=True, is_archive=True
        )
        response = self.client.get(reverse("archive:post_detail", args=[post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Tag List")
        self.assertNotContains(response, "Suggested Reads")
        self.assertNotContains(response, "Post Timeline")

    def test_detail_view_tags(self):
        math_tag = create_tag("math")
        cs_tag = create_tag("cs")
        post = create_post("Post Title", "post-title", tags=[cs_tag], is_archive=True)
        post_new = create_post("New Post Title", "new-post-title", tags=[math_tag])
        response = self.client.get(reverse("archive:post_detail", args=[post.slug]))
        target_post = response.context["post"]
        self.assertIn(cs_tag, target_post.tags.all())
        self.assertNotIn(math_tag, target_post.tags.all())

    def test_detail_no_other_posts(self):
        math_tag = create_tag("math")
        cs_tag = create_tag("cs")
        post = create_post("Post Title", "post-title", tags=[cs_tag], is_archive=True)
        post_new = create_post("New Post Title", "new-post-title", tags=[math_tag])
        response = self.client.get(reverse("archive:post_detail", args=[post.slug]))
        self.assertNotContains(response, post_new.title)

    def test_detail_wrong_slug(self):
        post = create_post("Post Title", "post-title", is_archive=True)
        response = self.client.get(
            reverse("archive:post_detail", args=["incorrect-slug"])
        )
        self.assertEqual(response.status_code, 404)

    def test_detail_slug_edge_case(self):
        post = create_post("INMO 2025 Review", "inmo-2025-review", is_archive=True)
        response = self.client.get(reverse("archive:post_detail", args=[post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "INMO 2025 Review")

    def test_slug_uniqueness(self):
        create_post("Post A", "same-slug", is_archive=True)
        with self.assertRaises(Exception):
            create_post("Post B", "same-slug", is_archive=True)


class BlogSearchViewTests(TestCase):
    def test_show_only_relevant_posts(self):
        post1 = create_post("Geometry", "geometry")
        post2 = create_post("Algebra", "algebra")
        response = self.client.get(reverse("blog:post_search") + "?q=geometry")
        self.assertEqual(response.status_code, 200)
        tgt_post_list = response.context["post_list"]
        self.assertContains(response, "Search Results")
        self.assertIn(post1, tgt_post_list)
        self.assertNotIn(post2, tgt_post_list)

    def test_check_default_view_when_empty(self):
        post1 = create_post("Post 1", "post-1")
        post2 = create_post("Post 2", "post-2")
        response = self.client.get(reverse("blog:post_search") + "?q=")
        tgt_post_list = response.context["post_list"]
        self.assertContains(response, "Blog Posts")
        self.assertIn(post1, tgt_post_list)
        self.assertIn(post2, tgt_post_list)

    def test_check_order_of_posts(self):
        post1 = create_post("Post 1", "post-1")
        post2 = create_post("Post 2", "post-2")
        response = self.client.get(reverse("blog:post_search") + "?q=post")
        self.assertQuerySetEqual(response.context["post_list"], [post1, post2])

    def test_search_using_title(self):
        post = create_post("Post Neow", "post-1")
        response = self.client.get(reverse("blog:post_search") + "?q=neow")
        tgt_post_list = response.context["post_list"]
        self.assertIn(post, tgt_post_list)

    def test_search_using_content(self):
        post = create_post("Post Neow", "post-1")
        response = self.client.get(reverse("blog:post_search") + "?q=slug")
        tgt_post_list = response.context["post_list"]
        self.assertIn(post, tgt_post_list)

    def test_search_using_tags(self):
        mathneow = create_tag("mathneow")
        post = create_post("Post Neow", "post-1", [mathneow])
        response = self.client.get(reverse("blog:post_search") + "?q=mathneow")
        tgt_post_list = response.context["post_list"]
        self.assertIn(post, tgt_post_list)

    def test_no_search_results(self):
        post = create_post("Post Neow", "post-1")
        response = self.client.get(reverse("blog:post_search") + "?q=mathneow")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No results found for your search query.")


class ArchiveSearchViewTests(TestCase):
    def test_show_only_relevant_posts(self):
        post1 = create_post("Geometry", "geometry", is_archive=True)
        post2 = create_post("Algebra", "algebra", is_archive=True)
        response = self.client.get(reverse("archive:post_search") + "?q=geometry")
        self.assertEqual(response.status_code, 200)
        tgt_post_list = response.context["post_list"]
        self.assertContains(response, "Search Results")
        self.assertIn(post1, tgt_post_list)
        self.assertNotIn(post2, tgt_post_list)

    def test_check_default_view_when_empty(self):
        post1 = create_post("Post 1", "post-1", is_archive=True)
        post2 = create_post("Post 2", "post-2", is_archive=True)
        response = self.client.get(reverse("archive:post_search") + "?q=")
        tgt_post_list = response.context["post_list"]
        self.assertContains(response, "Archive Posts")
        self.assertIn(post1, tgt_post_list)
        self.assertIn(post2, tgt_post_list)

    def test_check_order_of_posts(self):
        post1 = create_post("Post 1", "post-1", is_archive=True)
        post2 = create_post("Post 2", "post-2", is_archive=True)
        response = self.client.get(reverse("archive:post_search") + "?q=post")
        self.assertQuerySetEqual(response.context["post_list"], [post1, post2])

    def test_search_using_title(self):
        post = create_post("Post Neow", "post-1", is_archive=True)
        response = self.client.get(reverse("archive:post_search") + "?q=neow")
        tgt_post_list = response.context["post_list"]
        self.assertIn(post, tgt_post_list)

    def test_search_using_content(self):
        post = create_post("Post Neow", "post-1", is_archive=True)
        response = self.client.get(reverse("archive:post_search") + "?q=slug")
        tgt_post_list = response.context["post_list"]
        self.assertIn(post, tgt_post_list)

    def test_search_using_tags(self):
        mathneow = create_tag("mathneow")
        post = create_post("Post Neow", "post-1", [mathneow], is_archive=True)
        response = self.client.get(reverse("archive:post_search") + "?q=mathneow")
        tgt_post_list = response.context["post_list"]
        self.assertIn(post, tgt_post_list)

    def test_no_search_results(self):
        post = create_post("Post Neow", "post-1", is_archive=True)
        response = self.client.get(reverse("archive:post_search") + "?q=mathneow")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No results found for your search query.")
