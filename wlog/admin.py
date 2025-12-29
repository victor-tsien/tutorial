# wlog/admin.py
from django.contrib import admin

from .models.title import Title
from .models.log import Log


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('title_text', 'created_at')
    search_fields = ('title_text',)
    list_filter = ('created_at',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'title')
    search_fields = ('log_text', 'title__title_text')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'