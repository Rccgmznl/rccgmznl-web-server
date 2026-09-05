from drf_spectacular.utils import extend_schema_view, extend_schema, inline_serializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from apps.basic_events.models import BasicEvent, BibleReference, HeroImage, About
from apps.basic_events.serializers import BasicEventSerializer, BibleReferenceSerializer, HeroImageSerializer, AboutSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Retrieve a list of basic events",
        description="Endpoint to retrieve all basic events",
    
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
        tags = ["Events"],
    ),

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
        tags = ["Events"],
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
        tags = ["Events"],
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
        tags = ["Events"],
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
        tags = ["Events"],
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
        tags = ["Events"],
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

    @extend_schema(
        summary="Retrieve the most recent basic event",
        description="Endpoint to retrieve the basic event with the latest start date",
        responses={
            200: BasicEventSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
            404: inline_serializer(
                name="BasicEventNotFound",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Events"],
    )
    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        event = self.get_queryset().order_by("-start_date").first()
        if event is None:
            return Response({"detail": "No basic events found."}, status=404)

        return Response(self.get_serializer(event).data)
    
@extend_schema_view(
    list=extend_schema(
        summary="List all Bible verses",
        description="Endpoint to list all Bible verses",
        responses={
            200: BibleReferenceSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Hero Bible verses"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a Bible verse",
        description="Endpoint to retrieve a Bible verse by its ID",
        responses={
            200: BibleReferenceSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Hero Bible verses"], 
    ),
    create=extend_schema(
        summary="Create a new Bible verse",
        description="Endpoint to create a new Bible verse",
        responses={
            201: BibleReferenceSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Hero Bible verses"],
    ),
    update=extend_schema(
        summary="Update an existing Bible verse",
        description="Endpoint to update an existing Bible verse by its ID",
        responses={
            200: BibleReferenceSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Hero Bible verses"],
    ),
    partial_update=extend_schema(
        summary="Partially update an existing Bible verse",
        description="Endpoint to partially update an existing Bible verse by its ID",
        responses={
            200: BibleReferenceSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Hero Bible verses"],
    ),
    destroy=extend_schema(
        summary="Delete a Bible verse",
        description="Endpoint to delete a Bible verse by its ID",
        responses={
            204: None,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Hero Bible verses"], 
    ),
)
class BibleReferenceViewSet(viewsets.ModelViewSet):
    queryset = BibleReference.objects.all()
    serializer_class = BibleReferenceSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = PageNumberPagination

@extend_schema_view(
    list=extend_schema(
        summary="List all hero images",
        description="Endpoint to list all hero images",
        responses={
            200: HeroImageSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Hero-Images"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a hero image",
        description="Endpoint to retrieve a hero image by its ID",
        responses={
            200: HeroImageSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Hero-Images"],
    ),
    create=extend_schema(
        summary="Create a new hero image",
        description="Endpoint to create a new hero image",
        responses={
            201: HeroImageSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Hero-Images"],
    ),
    update=extend_schema(
        summary="Update an existing hero image",
        description="Endpoint to update an existing hero image by its ID",
        responses={
            200: HeroImageSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Hero-Images"],
    ),
    partial_update=extend_schema(
        summary="Partially update an existing hero image",
        description="Endpoint to partially update an existing hero image by its ID",
        responses={
            200: HeroImageSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Hero-Images"],
    ),
    destroy=extend_schema(
        summary="Delete a hero image",
        description="Endpoint to delete a hero image by its ID",
        responses={
            204: None,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Hero-Images"],   
    ),
)
class HeroImageViewSet(viewsets.ModelViewSet):
    queryset = HeroImage.objects.all()
    serializer_class = HeroImageSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = PageNumberPagination

@extend_schema_view(
    list=extend_schema(
        summary="Retrieve a list of about sections",
        description="Endpoint to retrieve a list of about sections",
        responses={200: AboutSerializer},
        tags=["About"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific about section",
        description="Endpoint to retrieve a specific about section by its ID",
        responses={200: AboutSerializer},
        tags=["About"],
    ),
    create=extend_schema(
        summary="Create a new about section",
        description="Endpoint to create a new about section",
        responses={
            201: AboutSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["About"],
    ),
    update=extend_schema(
        summary="Update an existing about section",
        description="Endpoint to update an existing about section by its ID",
        responses={
            200: AboutSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["About"],
    ),
    partial_update=extend_schema(
        summary="Partially update an existing about section",
        description="Endpoint to partially update an existing about section by its ID",
        responses={
            200: AboutSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["About"],
    ),
    destroy=extend_schema(
        summary="Delete an about section",
        description="Endpoint to delete an about section by its ID",
        responses={
            204: None,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["About"],   
    ),
)
class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = PageNumberPagination