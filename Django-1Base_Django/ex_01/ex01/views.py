from django.shortcuts import render


def django_page(request):
    return render(request, "ex01-django.html")


def display_page(request):
    return render(request, "ex01-display.html")


def template_engine_page(request):
    context = {
        "features": ["Blocks", "for ... in loops", "if control structures", "Context variables"],
        "show_note": True,
        "engine_name": "Django Template Language (DTL)",
    }
    return render(request, "ex01-template.html", context)
