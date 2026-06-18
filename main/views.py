from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    return render(request, "main/home.html")


def calculus_page(request):
    return render(request, "main/calculus.html")


def olympiads_page(request):
    return render(request, "main/olympiads.html")


def pet_peeves_page(request):
    return render(request, "main/pet_peeves.html")


def contact_page(request):
    return render(request, "main/contact.html")


def robots_txt(request):
    content = [
        "User-agent: *",
        "Disallow: /super-secret-admin-path-69420/",
        "Allow: /",
        "Sitemap: https://bubudroid.me/sitemap.xml",
    ]
    return HttpResponse("\n".join(content), content_type="text/plain")
