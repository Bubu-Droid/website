from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page


@cache_page(60 * 30)
def home_page(request):
    return render(request, "main/home.html")


@cache_page(60 * 30)
def calculus_page(request):
    return render(request, "main/calculus.html")


@cache_page(60 * 30)
def olympiads_page(request):
    return render(request, "main/olympiads.html")


@cache_page(60 * 30)
def pet_peeves_page(request):
    return render(request, "main/pet_peeves.html")


@cache_page(60 * 30)
def contact_page(request):
    return render(request, "main/contact.html")


def trigger_error(request):
    1 / 0  # This will raise ZeroDivisionError
    return HttpResponse("This will never be reached.")


def robots_txt(request):
    content = [
        "User-agent: *",
        "Disallow: /super-secret-admin-path-69420/",
        "Allow: /",
        "Sitemap: https://bubudroid.me/sitemap.xml",
    ]
    return HttpResponse("\n".join(content), content_type="text/plain")
