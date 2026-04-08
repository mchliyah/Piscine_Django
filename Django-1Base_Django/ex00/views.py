from django.shortcuts import render


def markdown_cheatsheet(request):
    return render(request, "index.html")
