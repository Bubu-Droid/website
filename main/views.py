from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

from scripts.bdaywisher import bdaywisher_mailer
from scripts.github_file_monitor import gfm_checker_and_mailer
from website.settings import CRON_SECRET


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


def github_file_monitor(request):
    if "authorization" not in request.headers:
        return HttpResponse(status=401)
    auth_header = request.headers["authorization"]
    if auth_header != f"Bearer ${CRON_SECRET}":
        return HttpResponse(status=401)

    gfm_checker_and_mailer()

    return JsonResponse({"success": "true"})


def bday_wisher(request):
    if "authorization" not in request.headers:
        return HttpResponse(status=401)
    auth_header = request.headers["authorization"]
    if auth_header != f"Bearer {CRON_SECRET}":
        return HttpResponse(status=401)

    bdaywisher_mailer()

    return JsonResponse({"success": "true"})


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
