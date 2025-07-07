from django.urls import path

from . import views

app_name = "postapp"
urlpatterns = [
    path("", views.post_index, name="post_index"),
    path("search/", views.post_search, name="post_search"),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
    path("tag/<str:tag>/", views.post_tag, name="post_tag"),
]
