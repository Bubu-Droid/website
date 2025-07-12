from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("calculus/", views.calculus_page, name="calculus_page"),
    path("olympiads/", views.olympiads_page, name="olympiads_page"),
    path("pet-peeves/", views.pet_peeves_page, name="pet_peeves_page"),
    path("contact/", views.contact_page, name="contact_page"),
    path("error-test/", views.trigger_error),
]
