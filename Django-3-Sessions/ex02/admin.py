from django.contrib import admin

from .models import Tip


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "tip_date")
    search_fields = ("content", "author__username")
