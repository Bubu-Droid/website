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
