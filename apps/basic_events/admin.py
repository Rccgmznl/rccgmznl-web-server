from django.contrib import admin

from apps.basic_events.models import (
    BasicEvent,
    BibleReference,
    HeroImage,
    WelcomeContent,
    LastestSermon,
    HeroGallery,
)

@admin.register(BasicEvent)
class BasicEventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "start_date")
    search_fields = ("title", "description")

@admin.register(BibleReference)
class BibleReferenceAdmin(admin.ModelAdmin):
    list_display = ("id", "reference")
    search_fields = ("reference", "text")

@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ("id", "alt_text", "order")
    search_fields = ("alt_text",)
    ordering = ("order",)

@admin.register(WelcomeContent)
class WelcomeContentAdmin(admin.ModelAdmin):
    list_display = ("id", "text")
    search_fields = ("text",)

@admin.register(LastestSermon)
class LastestSermonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "preacher")
    search_fields = ("title", "description", "preacher", "tags")
    ordering = ("-date",)

@admin.register(HeroGallery)
class HeroGalleryAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "alt_text", "order")
    search_fields = ("alt_text",)
    ordering = ("order",)


