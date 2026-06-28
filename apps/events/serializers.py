from django.db import transaction
from rest_framework import serializers

from apps.events.models import Event, EventGallery, EventSchedule


class EventScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSchedule
        fields = [
            "id",
            "created_by",
            "recurrence_type",
            "day_of_week",
            "day_of_month",
            "start_time",
            "end_time",
            "start_at",
            "end_at",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]


class EventGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventGallery
        fields = [
            "id",
            "created_by",
            "image_url",
            "caption",
            "display_order",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]


class EventSerializer(serializers.ModelSerializer):
    schedules = EventScheduleSerializer(many=True, required=False)
    galleries = EventGallerySerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = [
            "id",
            "created_by",
            "title",
            "description",
            "is_recurring",
            "schedules",
            "galleries",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def _get_request_user(self):
        request = self.context.get("request")
        if request and getattr(request, "user", None) and request.user.is_authenticated:
            return request.user
        return None

    def _validate_nested_rows(self, event, schedules_data, galleries_data, created_by):
        for schedule_data in schedules_data:
            schedule = EventSchedule(
                event=event,
                created_by=created_by,
                **schedule_data,
            )
            try:
                schedule.full_clean()
            except Exception as exc:
                raise serializers.ValidationError({"schedules": exc.message_dict})

        for gallery_data in galleries_data:
            gallery = EventGallery(
                event=event,
                created_by=created_by,
                **gallery_data,
            )
            try:
                gallery.full_clean()
            except Exception as exc:
                raise serializers.ValidationError({"galleries": exc.message_dict})

    def validate(self, attrs):
        schedules = attrs.get("schedules")
        is_recurring = attrs.get("is_recurring")
        if self.instance is not None and is_recurring is None:
            is_recurring = self.instance.is_recurring

        if schedules is not None and is_recurring is False:
            for schedule in schedules:
                if schedule.get("recurrence_type") is not None:
                    raise serializers.ValidationError(
                        {
                            "schedules": (
                                "Non-recurring events must not include recurrence_type in schedules."
                            )
                        }
                    )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        schedules_data = validated_data.pop("schedules", [])
        galleries_data = validated_data.pop("galleries", [])
        created_by = self._get_request_user()

        event = Event.objects.create(created_by=created_by, **validated_data)

        self._validate_nested_rows(
            event,
            schedules_data,
            galleries_data,
            created_by,
        )

        for schedule_data in schedules_data:
            EventSchedule.objects.create(
                event=event,
                created_by=created_by,
                **schedule_data,
            )

        for gallery_data in galleries_data:
            EventGallery.objects.create(
                event=event,
                created_by=created_by,
                **gallery_data,
            )

        return event

    @transaction.atomic
    def update(self, instance, validated_data):
        schedules_data = validated_data.pop("schedules", None)
        galleries_data = validated_data.pop("galleries", None)
        created_by = self._get_request_user()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if schedules_data is not None:
            self._validate_nested_rows(instance, schedules_data, [], created_by)
        if galleries_data is not None:
            self._validate_nested_rows(instance, [], galleries_data, created_by)

        # Replace nested schedules only when provided on request.
        if schedules_data is not None:
            instance.schedules.all().delete()
            for schedule_data in schedules_data:
                EventSchedule.objects.create(
                    event=instance,
                    created_by=created_by,
                    **schedule_data,
                )

        # Replace nested galleries only when provided on request.
        if galleries_data is not None:
            instance.galleries.all().delete()
            for gallery_data in galleries_data:
                EventGallery.objects.create(
                    event=instance,
                    created_by=created_by,
                    **gallery_data,
                )

        return instance
