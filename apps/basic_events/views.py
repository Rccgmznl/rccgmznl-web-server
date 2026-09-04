from drf_spectacular.utils import extend_schema_view, extend_schema, inline_serializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from apps.basic_events.models import BasicEvent, BibleReference
from apps.basic_events.serializers import BasicEventSerializer, BibleReferenceSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Retrieve a list of basic events",
        description="Endpoint to retrieve all basic events",
    ),
    responses={
        200: BasicEventSerializer,
        201: BasicEventSerializer,
        401: inline_serializer(
            name="Unauthorized",
            fields={
                "detail": "string",
            },
        ),
    },
    tags = ["Basic Events"],
    retrieve=extend_schema(
        summary="Retrieve a single basic event",
        description="Endpoint to retrieve a single basic event by its ID",
        responses={
            200: BasicEventSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
    ),
    create=extend_schema(
        summary="Create a new basic event",
        description="Endpoint to create a new basic event",
        responses={
            201: BasicEventSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
    ),
    update=extend_schema(
        summary="Update an existing basic event",
        description="Endpoint to update an existing basic event by its ID",
        responses={
            200: BasicEventSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Partially update an existing basic event",
        description="Endpoint to partially update an existing basic event by its ID",
        responses={
            200: BasicEventSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
    ),
    destroy=extend_schema(
        summary="Delete a basic event",
        description="Endpoint to delete a basic event by its ID",
        responses={
            204: None,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
    ),
)
class BasicEventViewSet(viewsets.ModelViewSet):
    queryset = BasicEvent.objects.all()
    serializer_class = BasicEventSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["title", "start_date"]
    search_fields = ["title", "description"]
    ordering_fields = ["start_date", "title"]
    ordering = ["start_date", "title"]
    pagination_class = PageNumberPagination
    
@extend_schema_view(
    list=extend_schema(
        summary="List all Bible references",
        description="Endpoint to list all Bible references",
        responses={
            200: BibleReferenceSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve a Bible reference",
        description="Endpoint to retrieve a Bible reference by its ID",
        responses={
            200: BibleReferenceSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
    ),
    create=extend_schema(
        summary="Create a new Bible reference",
        description="Endpoint to create a new Bible reference",
        responses={
            201: BibleReferenceSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
    ),
    update=extend_schema(
        summary="Update an existing Bible reference",
        description="Endpoint to update an existing Bible reference by its ID",
        responses={
            200: BibleReferenceSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Partially update an existing Bible reference",
        description="Endpoint to partially update an existing Bible reference by its ID",
        responses={
            200: BibleReferenceSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
    ),
    destroy=extend_schema(
        summary="Delete a Bible reference",
        description="Endpoint to delete a Bible reference by its ID",
        responses={
            204: None,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
    ),
)
class BibleReferenceViewSet(viewsets.ModelViewSet):
    queryset = BibleReference.objects.all()
    serializer_class = BibleReferenceSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = PageNumberPagination