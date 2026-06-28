from django.contrib import admin

from apps.events.models import Event, EventGallery, EventSchedule


class EventScheduleInline(admin.TabularInline):
    model = EventSchedule
    extra = 1


class EventGalleryInline(admin.TabularInline):
    model = EventGallery
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_recurring", "created_at")
    list_filter = ("is_recurring", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    inlines = (EventScheduleInline, EventGalleryInline)


@admin.register(EventSchedule)
class EventScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "recurrence_type",
        "day_of_week",
        "day_of_month",
        "start_time",
        "end_time",
        "start_at",
        "end_at",
    )
    list_filter = ("recurrence_type", "day_of_week")
    search_fields = ("event__title",)


@admin.register(EventGallery)
class EventGalleryAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "display_order", "created_at")
    list_filter = ("created_at",)
    search_fields = ("event__title", "caption")
    ordering = ("event", "display_order")
