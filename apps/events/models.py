from django.core.exceptions import ValidationError
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title", "-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["is_recurring"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.title


class EventSchedule(models.Model):
    RECURRENCE_WEEKLY = "weekly"
    RECURRENCE_MONTHLY = "monthly"
    RECURRENCE_TYPE_CHOICES = [
        (RECURRENCE_WEEKLY, "Weekly"),
        (RECURRENCE_MONTHLY, "Monthly"),
    ]

    DAY_OF_WEEK_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="schedules",
    )
    recurrence_type = models.CharField(
        max_length=20,
        choices=RECURRENCE_TYPE_CHOICES,
        null=True,
        blank=True,
    )
    day_of_week = models.PositiveSmallIntegerField(
        choices=DAY_OF_WEEK_CHOICES,
        null=True,
        blank=True,
    )
    day_of_month = models.PositiveSmallIntegerField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["recurrence_type", "day_of_week", "day_of_month", "start_time", "start_at"]

    def clean(self):
        is_time_range_provided = self.start_time is not None or self.end_time is not None

        if self.event and self.event.is_recurring:
            if self.recurrence_type not in {
                self.RECURRENCE_WEEKLY,
                self.RECURRENCE_MONTHLY,
            }:
                raise ValidationError(
                    "Recurring events require recurrence_type of weekly or monthly."
                )

            if self.start_time is None or self.end_time is None:
                raise ValidationError(
                    "Recurring events require start_time and end_time."
                )

            if self.recurrence_type == self.RECURRENCE_WEEKLY:
                if self.day_of_week is None:
                    raise ValidationError(
                        "Weekly recurring events require day_of_week."
                    )
                if self.day_of_month is not None:
                    raise ValidationError(
                        "Weekly recurring events should not define day_of_month."
                    )

            if self.recurrence_type == self.RECURRENCE_MONTHLY:
                if self.day_of_month is None:
                    raise ValidationError(
                        "Monthly recurring events require day_of_month."
                    )
                if not 1 <= self.day_of_month <= 31:
                    raise ValidationError(
                        "day_of_month must be between 1 and 31."
                    )
                if self.day_of_week is not None:
                    raise ValidationError(
                        "Monthly recurring events should not define day_of_week."
                    )

            if self.start_at is not None or self.end_at is not None:
                raise ValidationError(
                    "Recurring event schedules should not define start_at/end_at."
                )
        else:
            if self.recurrence_type is not None:
                raise ValidationError(
                    "Non-recurring event schedules should not define recurrence_type."
                )
            if self.day_of_week is not None or self.day_of_month is not None:
                raise ValidationError(
                    "Non-recurring event schedules should not define day_of_week/day_of_month."
                )

        if is_time_range_provided and (self.start_time is None or self.end_time is None):
            raise ValidationError("Both start_time and end_time must be set together.")

        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError("end_time must be later than start_time.")

        is_datetime_range_provided = self.start_at is not None or self.end_at is not None
        if is_datetime_range_provided and (self.start_at is None or self.end_at is None):
            raise ValidationError("Both start_at and end_at must be set together.")

        if self.start_at and self.end_at and self.end_at <= self.start_at:
            raise ValidationError("end_at must be later than start_at.")

    def __str__(self):
        if (
            self.recurrence_type == self.RECURRENCE_WEEKLY
            and self.day_of_week is not None
            and self.start_time
        ):
            return f"{self.get_day_of_week_display()} {self.start_time}"
        if (
            self.recurrence_type == self.RECURRENCE_MONTHLY
            and self.day_of_month is not None
            and self.start_time
        ):
            return f"Day {self.day_of_month} {self.start_time}"
        if self.start_at:
            return self.start_at.isoformat()
        return f"Schedule {self.pk}"


class EventGallery(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="galleries",
    )
    image_url = models.URLField(max_length=500)
    caption = models.CharField(max_length=255, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.event.title} - Gallery {self.id}"
