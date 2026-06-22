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
        "Allow: /",
        "Sitemap: https://www.bubudroid.me/sitemap.xml",
    ]

    return HttpResponse(
        "\n".join(content).encode("utf-8"),
        content_type="text/plain",
    )
