from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from .models import Banner, StoryCategory, StoryItem, SiteContent, CourseFeature, SplashLink, SocialLink

@admin.register(Banner)
class BannerAdmin(ModelAdmin):
    list_display = ["title", "display_image_1", "display_image_2"]
    
    @admin.display(description="Превью 1")
    def display_image_1(self, obj):
        if obj.image_1:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.image_1.url)
        return "-"

    @admin.display(description="Превью 2")
    def display_image_2(self, obj):
        if obj.image_2:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.image_2.url)
        return "-"

class StoryItemInline(TabularInline):
    model = StoryItem
    extra = 1
    tab = True
    fields = ["image", "display_preview", "order"]
    readonly_fields = ["display_preview"]

    def display_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 80px; height: 120px; object-fit: cover; border-radius: 8px;" />', obj.image.url)
        return "-"
    display_preview.short_description = "Превью"

@admin.register(StoryCategory)
class StoryCategoryAdmin(ModelAdmin):
    list_display = ["label", "display_thumb", "order"]
    inlines = [StoryItemInline]
    
    @admin.display(description="Обложка")
    def display_thumb(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%;" />', obj.thumbnail.url)
        return "-"

@admin.register(SiteContent)
class SiteContentAdmin(ModelAdmin):
    list_display = ["key", "value"]
    list_editable = ["value"]
    search_fields = ["key", "value"]

@admin.register(CourseFeature)
class CourseFeatureAdmin(ModelAdmin):
    list_display = ["title", "order", "display_icon"]
    list_editable = ["order"]
    
    @admin.display(description="Иконка")
    def display_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="width: 40px; height: 40px;" />', obj.icon.url)
        return "-"

@admin.register(SplashLink)
class SplashLinkAdmin(ModelAdmin):
    list_display = ["title", "icon_type", "order"]
    list_editable = ["icon_type", "order"]

@admin.register(SocialLink)
class SocialLinkAdmin(ModelAdmin):
    list_display = ["icon_type", "order"]
    list_editable = ["order"]
