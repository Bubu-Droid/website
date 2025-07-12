import calendar
import re

from django.core.cache import cache
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.views.decorators.cache import cache_page
from markdown import markdown

from .models import Post, PostTag


def bump_headings(html: str, levels: int) -> str:
    def replace_heading(match):
        level = int(match.group(1))
        attrs = match.group(2) or ""
        content = match.group(3)
        new_level = min(level + levels, 6)
        return f"<h{new_level}{attrs}>{content}</h{new_level}>"

    return re.sub(
        r"<h([1-6])(\s[^>]*)?>(.*?)</h\1>",
        replace_heading,
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )


@cache_page(60 * 30)
def post_index(request):
    is_archive = request.resolver_match.namespace == "archive"
    posts = Post.objects.filter(is_archive=is_archive).order_by("-date")
    for post in posts:
        md_content = post.get_markdown_content()
        html_content = markdown(
            md_content, extensions=["fenced_code", "toc", "codehilite", "attr_list"]
        )
        bumped_content = bump_headings(html_content, levels=2)
        post.rendered_content = mark_safe(bumped_content)
    post_timeline, tag_list, suggested_posts = get_sidebar_data(is_archive)

    if is_archive:
        heading = "Archive Posts"
        title = "Archive"
        desc = "A curated archive of academic and math-related posts, storage notes, linked materials, and more from past updates."
    else:
        heading = "Blog Posts"
        title = "Blog"
        desc = "A space for my less-serious thoughts — reflections on life, rants, ideas, and whatever else I feel like sharing."

    return render(
        request,
        "postapp/index.html",
        {
            "post_list": posts,
            "post_timeline": post_timeline,
            "tag_list": tag_list,
            "suggested_posts": suggested_posts,
            "title": title,
            "description": desc,
            "heading": heading,
        },
    )


@cache_page(60 * 10)
def post_detail(request, slug):
    is_archive = request.resolver_match.namespace == "archive"
    post = get_object_or_404(Post, slug=slug, is_archive=is_archive)
    md_content = post.get_markdown_content()
    html_content = markdown(
        md_content, extensions=["fenced_code", "toc", "codehilite", "attr_list"]
    )
    bumped_content = bump_headings(html_content, levels=1)
    desc = " ".join(strip_tags(bumped_content).strip().split())[:150]
    html_content = mark_safe(bumped_content)
    return render(
        request,
        "postapp/detail.html",
        {
            "post": post,
            "description": desc,
            "content": html_content,
        },
    )


def post_search(request):
    is_archive = request.resolver_match.namespace == "archive"
    query = request.GET.get("q", "").strip().lower()
    posts = Post.objects.filter(is_archive=is_archive).order_by("-date")
    heading = "Search Results"
    title = "Search Results"

    if query:
        query_words = query.split()

        def matches(post):
            title = post.title.lower()
            tags = [tag.name.lower() for tag in post.tags.all()]
            content = post.get_markdown_content().lower()
            return any(
                word in title or any(word in tag for tag in tags) or word in content
                for word in query_words
            )

        posts = [post for post in posts if matches(post)]
    else:
        heading = "Archive Posts" if is_archive else "Blog Posts"
        title = "Archive" if is_archive else "Blog"
    for post in posts:
        md_content = post.get_markdown_content()
        html_content = markdown(
            md_content, extensions=["fenced_code", "toc", "codehilite", "attr_list"]
        )
        bumped_content = bump_headings(html_content, levels=2)
        highlighted = bumped_content
        if query:
            for word in query_words:
                highlighted = re.sub(
                    rf"(?i)\b({re.escape(word)})\b",
                    r"<mark>\1</mark>",
                    highlighted,
                    flags=re.IGNORECASE,
                )

        post.rendered_content = mark_safe(highlighted)

    post_timeline, tag_list, suggested_posts = get_sidebar_data(is_archive)
    if is_archive:
        desc = "Search results from the archive — including older academic posts, math materials, problem sets, and reference content."
    else:
        desc = "Browse search results from the blog — covering thoughts on math, programming, introspection, and everyday musings."

    return render(
        request,
        "postapp/index.html",
        {
            "post_list": posts,
            "post_timeline": post_timeline,
            "tag_list": tag_list,
            "suggested_posts": suggested_posts,
            "title": title,
            "description": desc,
            "heading": heading,
        },
    )


def get_sidebar_data(is_archive):
    posts = Post.objects.filter(is_archive=is_archive)
    post_timeline = {}
    for post in posts:
        year = str(post.date.year)
        month = str(calendar.month_name[post.date.month])
        if year not in post_timeline:
            post_timeline[year] = {}
        if month not in post_timeline[year]:
            post_timeline[year][month] = []
        post_timeline[year][month].append(post)
    post_timeline = dict(reversed(list(post_timeline.items())))
    tag_list = (
        PostTag.objects.filter(posts__is_archive=is_archive)
        .annotate(num_posts=Count("posts", filter=Q(posts__is_archive=is_archive)))
        .filter(num_posts__gt=0)
        .order_by("-num_posts")
    )
    suggested_posts = Post.objects.filter(
        is_archive=is_archive, suggested=True
    ).order_by("-date")

    result = (post_timeline, tag_list, suggested_posts)
    return result


def post_tag(request, tag):
    is_archive = request.resolver_match.namespace == "archive"
    tag_obj = get_object_or_404(PostTag, name=tag)
    if is_archive:
        title = f"Archive Posts tagged with “{tag_obj.name}”"
        desc = f"Browse archived content tagged with “{tag_obj.name}” — including academic notes, math materials, and past resources."
    else:
        title = f"Blog Posts tagged with “{tag_obj.name}”"
        desc = f"Explore blog posts tagged with “{tag_obj.name}” — covering ideas, math discussions, programming thoughts, and more."

    post_list = Post.objects.filter(tags=tag_obj, is_archive=is_archive).order_by(
        "-date"
    )
    for post in post_list:
        md_content = post.get_markdown_content()
        html_content = markdown(
            md_content, extensions=["fenced_code", "toc", "codehilite", "attr_list"]
        )
        bumped_content = bump_headings(html_content, levels=2)
        post.rendered_content = mark_safe(bumped_content)

    post_timeline, tag_list, suggested_posts = get_sidebar_data(is_archive)
    return render(
        request,
        "postapp/index.html",
        {
            "post_list": post_list,
            "tag_filter": tag_obj,
            "post_timeline": post_timeline,
            "tag_list": tag_list,
            "suggested_posts": suggested_posts,
            "title": title,
            "description": desc,
        },
    )
