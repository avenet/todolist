from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ['status', 'created', 'updated', 'owner']
    search_fields = ['name', 'description', 'owner']
    list_display = ['status', 'owner']
