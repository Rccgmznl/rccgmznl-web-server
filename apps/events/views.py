from drf_spectacular.utils import OpenApiExample, extend_schema, extend_schema_view, inline_serializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.events.models import Event
from apps.events.serializers import EventSerializer, GalleryImageUploadSerializer
from apps.events.services import upload_gallery_image_file


@extend_schema_view(
    create=extend_schema(
        summary="Create Event",
        description=(
            "Create an event with nested schedules and galleries. "
            "Gallery images must be uploaded first using the gallery upload endpoint, "
            "then the returned image_url should be sent in the event payload."
        ),
        request=EventSerializer,
        responses={201: EventSerializer},
        examples=[
            OpenApiExample(
                "Create Event With Image URL",
                value={
                    "title": "Monthly Thanksgiving Service",
                    "description": "A special monthly thanksgiving service.",
                    "is_recurring": True,
                    "schedules": [
                        {
                            "recurrence_type": "monthly",
                            "day_of_month": 1,
                            "start_time": "10:00:00",
                            "end_time": "12:00:00",
                        }
                    ],
                    "galleries": [
                        {
                            "image_url": "http://localhost:8000/media/gallery/2026/06/sample.jpg",
                            "caption": "Main banner",
                            "display_order": 1,
                        }
                    ],
                },
                request_only=True,
            ),
        ],
        tags=["Events"],
    ),
    update=extend_schema(
        summary="Update Event",
        description=(
            "Replace an event and nested schedules or galleries. "
            "Gallery rows should reference image_url values returned from the upload endpoint."
        ),
        request=EventSerializer,
        responses={200: EventSerializer},
        tags=["Events"],
    ),
    partial_update=extend_schema(
        summary="Partially Update Event",
        description=(
            "Partially update an event. If galleries is included, gallery rows are replaced "
            "with the provided list. Upload image files first and send the resulting image_url values."
        ),
        request=EventSerializer,
        responses={200: EventSerializer},
        tags=["Events"],
    ),
)
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.prefetch_related("schedules", "galleries").all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_recurring"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at", "title"]
    ordering = ["-created_at"]


class GalleryImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        summary="Upload Gallery Image",
        description=(
            "Upload a single gallery image and return generated image URL and storage path."
        ),
        request=GalleryImageUploadSerializer,
        responses={
            201: inline_serializer(
                name="GalleryImageUploadResponse",
                fields={
                    "url": serializers.URLField(),
                    "path": serializers.CharField(),
                },
            ),
        },
        examples=[
            OpenApiExample(
                "Upload File",
                value={"file": "<binary file>"},
                request_only=True,
            ),
            OpenApiExample(
                "Upload Response",
                value={
                    "url": "http://localhost:8000/media/gallery/2026/06/abc123.jpg",
                    "path": "gallery/2026/06/abc123.jpg",
                },
                response_only=True,
            ),
        ],
        tags=["Events"],
    )

    def post(self, request, *args, **kwargs):
        serializer = GalleryImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_file = serializer.validated_data["file"]
        upload_result = upload_gallery_image_file(
            uploaded_file,
            request=request,
        )

        return Response(
            {
                "url": upload_result["url"],
                "path": upload_result["path"],
            },
            status=201,
        )
