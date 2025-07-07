from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from .models import Post, PostTag


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "date", "get_tags", "is_archive", "suggested"]
    list_filter = ["date", "is_archive", "suggested"]
    search_fields = ["title", "slug", "tags__name"]
    prepopulated_fields = {"slug": ["title"]}
    autocomplete_fields = ["tags"]
    fieldsets = [
        (
            "Post Details",
            {
                "fields": [
                    "title",
                    "slug",
                    "date",
                ]
            },
        ),
        (
            "Category",
            {
                "fields": [
                    "is_archive",
                    "suggested",
                ]
            },
        ),
        ("Tags", {"fields": ["tags"]}),
    ]

    @admin.display(description="Tags")
    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())


class PostTagAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "get_post_count"]
    fieldsets = [
        ("Tags", {"fields": ["name", "used_in"]}),
    ]
    readonly_fields = ["used_in"]

    @admin.display(description="Used In Posts")
    def used_in(self, obj):
        posts = obj.posts.all()
        if not posts.exists():
            return "—"
        links = [
            f'<a href="/admin/postapp/post/{post.id}/change/">• {post.title}</a>'
            for post in posts
        ]
        return format_html("<br>".join(links))

    @admin.display(description="Post Count")
    def get_post_count(self, obj):
        return getattr(obj, "post_count", obj.posts.count())

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(post_count=Count("posts"))
            .order_by("-post_count")
        )


admin.site.register(Post, PostAdmin)
admin.site.register(PostTag, PostTagAdmin)
