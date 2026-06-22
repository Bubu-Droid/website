import json
import re

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.utils import encoding
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from markdown import markdown

from website.settings import BASE_DIR

BLOG_DB = BASE_DIR / "db_blog.json"
ARCHIVE_DB = BASE_DIR / "db_archive.json"


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


def get_markdown_content(is_archive: bool, slug: str) -> str:
    folder = "archive" if is_archive else "blog"
    path = BASE_DIR / "post-content" / folder / slug / "content.md"
    try:
        with path.open(mode="r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Markdown file not found for slug ‘{slug}’"


def get_posts(is_archive: bool):
    if is_archive:
        with ARCHIVE_DB.open(mode="r", encoding="utf-8") as f:
            posts = json.load(f)["posts"]
    else:
        with BLOG_DB.open(mode="r", encoding="utf-8") as f:
            posts = json.load(f)["posts"]
    return posts


def get_sidebar_data(is_archive: bool):
    posts = get_posts(is_archive)
    post_timeline = {}
    for post in posts:
        year = str(post["date"]["year"])
        month = str(post["date"]["month"])
        if year not in post_timeline:
            post_timeline[year] = {}
        if month not in post_timeline[year]:
            post_timeline[year][month] = []
        post_timeline[year][month].append(post)
    # post_timeline = dict(reversed(list(post_timeline.items())))

    tag_dict = {}
    suggested_posts = []

    for post in posts:
        for tag in post["tags"]:
            tag_dict[tag] = tag_dict.get(tag, 0) + 1

        if post["suggested"]:
            suggested_posts.append(post)

    tag_dict = {k: v for k, v in sorted(tag_dict.items(), key=lambda item: item[1])}
    tag_list = list(tag_dict.keys())

    return post_timeline, tag_list, suggested_posts


def post_index(request):
    is_archive = request.resolver_match.namespace == "archive"
    posts = get_posts(is_archive)
    rendered_content = ""

    for post in posts:
        md_content = get_markdown_content(is_archive, post["slug"])
        html_content = markdown(
            md_content, extensions=["fenced_code", "toc", "codehilite", "attr_list"]
        )
        bumped_content = bump_headings(html_content, levels=2)
        rendered_content = mark_safe(bumped_content)
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
            "rendered_content": rendered_content,
        },
    )


def post_detail(request, slug):
    is_archive = request.resolver_match.namespace == "archive"
    posts = get_posts(is_archive)
    for post in posts:
        if post["slug"] == slug:
            break
    else:
        raise Http404

    md_content = get_markdown_content(is_archive, post["slug"])
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


def highlight_text(html_content: str, word: str):
    def check_case(match):
        if match.group(1):
            return match.group(1)
        else:
            return f"<mark>{match.group(2)}</mark>"

    # this logic is so goated bruv. i could've never come up with this.
    pattern = rf"(<[^>]+>)|({re.escape(word)})"

    highlighted = re.sub(
        pattern,
        check_case,
        html_content,
        flags=re.IGNORECASE,
    )

    return highlighted


def post_search(request):
    is_archive = request.resolver_match.namespace == "archive"
    query = request.GET.get("q", "").strip().lower()
    posts = get_posts(is_archive)
    heading = "Search Results"
    title = "Search Results"
    rendered_content = ""

    if query:
        query_words = query.split()

        def matches(post):
            title = post["title"].lower()
            tags = [tag.lower() for tag in post["tags"]]
            content = get_markdown_content(is_archive, post["slug"]).lower()
            return any(
                word in title or any(word in tag for tag in tags) or word in content
                for word in query_words
            )

        posts = [post for post in posts if matches(post)]
    else:
        heading = "Archive Posts" if is_archive else "Blog Posts"
        title = "Archive" if is_archive else "Blog"

    for post in posts:
        md_content = get_markdown_content(is_archive, post["slug"])
        html_content = markdown(
            md_content, extensions=["fenced_code", "toc", "codehilite", "attr_list"]
        )
        bumped_content = bump_headings(html_content, levels=2)
        highlighted = bumped_content
        if query:
            for word in query_words:
                highlighted = highlight_text(highlighted, word)

        rendered_content = mark_safe(highlighted)

    post_timeline, tag_list, suggested_posts = get_sidebar_data(is_archive)
    if is_archive:
        desc = "Search results from the archive — including older academic posts, math materials, problem sets, and reference content."
    else:
        desc = "Search through the blog — a collection of less-serious thoughts, reflections, and whatever else has crossed my mind lately."

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
            "rendered_content": rendered_content,
        },
    )


def post_tag(request, tag):
    is_archive = request.resolver_match.namespace == "archive"
    posts = get_posts(is_archive)
    post_list = []
    tag_set = set()
    rendered_content = ""

    for post in posts:
        tag_set.update(set(post["tags"]))
        if tag in post["tags"]:
            post_list.append(post)

    if tag not in tag_set:
        raise Http404

    if is_archive:
        title = f"Archive Posts tagged with “{tag}”"
        desc = f"Browse archived content tagged with “{tag}” — including academic notes, math materials, and past resources."
    else:
        title = f"Blog Posts tagged with “{tag}”"
        desc = f"Explore blog posts tagged with “{tag}” — including casual thoughts, rants, ideas, and other informal posts."

    for post in post_list:
        md_content = get_markdown_content(is_archive, post["slug"])
        html_content = markdown(
            md_content, extensions=["fenced_code", "toc", "codehilite", "attr_list"]
        )
        bumped_content = bump_headings(html_content, levels=2)
        rendered_content = mark_safe(bumped_content)

    post_timeline, tag_list, suggested_posts = get_sidebar_data(is_archive)
    return render(
        request,
        "postapp/index.html",
        {
            "post_list": post_list,
            "tag_filter": tag,
            "post_timeline": post_timeline,
            "tag_list": tag_list,
            "suggested_posts": suggested_posts,
            "title": title,
            "description": desc,
            "rendered_content": rendered_content,
        },
    )
