from django.contrib import admin
from .models import SiteContent, StoryCategory, StoryItem, SplashLink

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key', 'value')

class StoryItemInline(admin.TabularInline):
    model = StoryItem
    extra = 3

@admin.register(StoryCategory)
class StoryCategoryAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'order')
    inlines = [StoryItemInline]

@admin.register(SplashLink)
class SplashLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'icon_type', 'order')
