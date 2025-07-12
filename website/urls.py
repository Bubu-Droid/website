"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.decorators.cache import cache_page

from main.views import robots_txt
from postapp.sitemaps import PostSitemap, StaticViewSitemap

sitemaps = {
    "posts": PostSitemap,
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("super-secret-admin-path-69420/", admin.site.urls),
    path("", include("main.urls")),
    path("blog/", include(("postapp.urls", "postapp"), namespace="blog")),
    path("archive/", include(("postapp.urls", "postapp"), namespace="archive")),
    path(
        "sitemap.xml",
        cache_page(60 * 60)(sitemap),
        {"sitemaps": sitemaps},
        name="sitemap",
    ),
    path("robots.txt", robots_txt, name="robots_txt"),
]

# TODO: Remove this while deploying

# if not settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
