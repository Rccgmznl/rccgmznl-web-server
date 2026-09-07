from drf_spectacular.utils import extend_schema_view, extend_schema, inline_serializer
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from apps.basic_events.models import BasicEvent, BibleReference, HeroImage, About, Sermon, WelcomeContent
from apps.basic_events.serializers import AboutSerializer, BasicEventSerializer, BibleReferenceSerializer, HeroImageOrderSerializer, HeroImageSerializer, SermonSerializer, SermonUploadRequestSerializer, WelcomeContentSerializer

class BibleReferenceView(APIView):
    parser_classes = [JSONParser]

    def get_permissions(self):
        permission_class = AllowAny if self.request.method == "GET" else IsAuthenticated
        return [permission_class()]

    @extend_schema(
        summary="Retrieve the featured Bible verse",
        responses={200: BibleReferenceSerializer},
        tags=["Hero Bible verse"],
    )
    def get(self, request):
        verse = BibleReference.objects.filter(pk=1).first()
        if verse is None:
            return Response(
                {"detail": "The featured Bible verse has not been configured."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(BibleReferenceSerializer(verse).data)

    @extend_schema(
        summary="Update the featured Bible verse",
        request=BibleReferenceSerializer,
        responses={200: BibleReferenceSerializer, 201: BibleReferenceSerializer},
        tags=["Hero Bible verse"],
    )
    def patch(self, request):
        verse = BibleReference.objects.filter(pk=1).first()
        serializer = BibleReferenceSerializer(
            verse,
            data=request.data,
            partial=verse is not None,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_status = (
            status.HTTP_200_OK if verse is not None else status.HTTP_201_CREATED
        )
        return Response(serializer.data, status=response_status)


class WelcomeContentView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        permission_class = AllowAny if self.request.method == "GET" else IsAuthenticated
        return [permission_class()]

    @extend_schema(
        summary="Retrieve the welcome content",
        responses={
            200: WelcomeContentSerializer,
            404: inline_serializer(
                name="WelcomeContentNotFoundError",
                fields={"detail": serializers.CharField()},
            ),
        },
        tags=["Welcome"],
    )
    def get(self, request):
        welcome = WelcomeContent.objects.filter(pk=1).first()
        if welcome is None:
            return Response(
                {"detail": "Welcome content has not been configured."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            WelcomeContentSerializer(welcome, context={"request": request}).data
        )

    @extend_schema(
        summary="Update the welcome content",
        request=WelcomeContentSerializer,
        responses={200: WelcomeContentSerializer, 201: WelcomeContentSerializer},
        tags=["Welcome"],
    )
    def patch(self, request):
        welcome = WelcomeContent.objects.filter(pk=1).first()
        serializer = WelcomeContentSerializer(
            welcome,
            data=request.data,
            partial=welcome is not None,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_status = (
            status.HTTP_200_OK if welcome is not None else status.HTTP_201_CREATED
        )
        return Response(serializer.data, status=response_status)


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
            200: inline_serializer(
                name="BasicEventDeleteResponse",
                fields={"id": serializers.IntegerField()},
            ),
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
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["title", "start_date"]
    search_fields = ["title", "description"]
    ordering_fields = ["start_date", "title"]
    ordering = ["start_date", "title"]
    pagination_class = PageNumberPagination

    def get_permissions(self):
        permission_class = AllowAny if self.request.method == "GET" else IsAuthenticated
        return [permission_class()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.pk
        self.perform_destroy(instance)
        return Response({"id": instance_id}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Retrieve the next upcoming basic event",
        description="Endpoint to retrieve the earliest basic event scheduled for today or later",
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
        event = (
            self.get_queryset()
            .filter(start_date__gte=timezone.localdate())
            .order_by("start_date", "title")
            .first()
        )
        if event is None:
            return Response({"detail": "No basic events found."}, status=404)

        return Response(self.get_serializer(event).data)
    
@extend_schema_view(
    list=extend_schema(tags=["Hero-Images"]),
    retrieve=extend_schema(tags=["Hero-Images"]),
    create=extend_schema(tags=["Hero-Images"]),
    update=extend_schema(tags=["Hero-Images"]),
    partial_update=extend_schema(tags=["Hero-Images"]),
    destroy=extend_schema(
        responses=inline_serializer(
            name="HeroImageDeleteResponse",
            fields={"id": serializers.IntegerField()},
        ),
        tags=["Hero-Images"],
    ),
)
class HeroImageViewSet(viewsets.ModelViewSet):
    queryset = HeroImage.objects.order_by("order")
    serializer_class = HeroImageSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = PageNumberPagination

    def get_permissions(self):
        permission_class = AllowAny if self.request.method == "GET" else IsAuthenticated
        return [permission_class()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.pk
        self.perform_destroy(instance)
        return Response({"id": instance_id}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data["order"]

        with transaction.atomic():
            existing_image = HeroImage.objects.select_for_update().filter(order=order).first()
            if existing_image is None and HeroImage.objects.count() >= 10:
                existing_image = HeroImage.objects.select_for_update().order_by("-order", "-id").first()

            if existing_image is not None:
                serializer = self.get_serializer(existing_image, data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        summary="Order hero images",
        description="Update the order of every hero image with a list of image IDs and orders.",
        request=HeroImageOrderSerializer,
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
    )
    @action(detail=False, methods=["post"], url_path="order")
    def order(self, request):
        serializer = HeroImageOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        requested_orders = serializer.validated_data["images"]

        with transaction.atomic():
            hero_images = list(HeroImage.objects.select_for_update().order_by("id"))
            existing_ids = {hero_image.id for hero_image in hero_images}
            requested_ids = {image["id"] for image in requested_orders}

            if requested_ids != existing_ids:
                raise ValidationError(
                    {"images": "Include every existing hero image exactly once."}
                )

            temporary_order_start = max(
                [hero_image.order for hero_image in hero_images] + [10]
            ) + len(hero_images) + 1
            for index, hero_image in enumerate(hero_images):
                hero_image.order = temporary_order_start + index
            HeroImage.objects.bulk_update(hero_images, ["order"])

            order_by_id = {image["id"]: image["order"] for image in requested_orders}
            for hero_image in hero_images:
                hero_image.order = order_by_id[hero_image.id]
            HeroImage.objects.bulk_update(hero_images, ["order"])

        return Response(self.get_serializer(HeroImage.objects.order_by("order"), many=True).data)

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
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = PageNumberPagination


class AboutView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        permission_class = AllowAny if self.request.method == "GET" else IsAuthenticated
        return [permission_class()]

    @extend_schema(
        summary="Retrieve the About content",
        responses={
            200: AboutSerializer,
            404: inline_serializer(
                name="AboutNotFoundError",
                fields={"detail": "string"},
            ),
        },
        tags=["About"],
    )
    def get(self, request):
        about = About.objects.filter(pk=1).first()
        if about is None:
            return Response(
                {"detail": "About content has not been configured."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(AboutSerializer(about, context={"request": request}).data)

    @extend_schema(
        summary="Update the About content",
        description=(
            "Update the single About dataset using multipart form data. "
            "Include an image when configuring About for the first time."
        ),
        request=AboutSerializer,
        responses={200: AboutSerializer, 201: AboutSerializer},
        tags=["About"],
    )
    def patch(self, request):
        about = About.objects.filter(pk=1).first()
        serializer = AboutSerializer(
            about,
            data=request.data,
            partial=about is not None,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_status = (
            status.HTTP_200_OK if about is not None else status.HTTP_201_CREATED
        )
        return Response(serializer.data, status=response_status)

@extend_schema_view(
    list=extend_schema(
        summary="Retrieve a list of sermons",
        description="Endpoint to retrieve a list of sermons",
        request=None,
        responses={200: SermonSerializer},
        tags=["Sermon"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific sermon",
        description="Endpoint to retrieve a specific sermon by its ID",
        request=None,
        responses={200: SermonSerializer},
        tags=["Sermon"],
    ),
    create=extend_schema(
        summary="Create a new sermon",
        description="Endpoint to create a new sermon",
        request=SermonUploadRequestSerializer,
        responses={
            201: SermonSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Sermon"],
    ),
    update=extend_schema(
        summary="Update an existing sermon",
        description="Endpoint to update an existing sermon by its ID",
        request=SermonUploadRequestSerializer,
        responses={
            200: SermonSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Sermon"],
    ),
    partial_update=extend_schema(
        summary="Partially update an existing sermon",
        description="Endpoint to partially update an existing sermon by its ID",
        request=SermonUploadRequestSerializer,
        responses={
            200: SermonSerializer,
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Sermon"],
    ),
    destroy=extend_schema(
        summary="Delete a sermon",
        description="Endpoint to delete a sermon by its ID",
        responses={
            200: inline_serializer(
                name="SermonDeleteResponse",
                fields={"id": serializers.IntegerField()},
            ),
            401: inline_serializer(
                name="Unauthorized",
                fields={
                    "detail": "string",
                },
            ),
        },
        tags=["Sermon"],   
    ),
)
class SermonViewSet(viewsets.ModelViewSet):
    queryset = Sermon.objects.all()
    serializer_class = SermonSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = PageNumberPagination

    def get_permissions(self):
        permission_class = AllowAny if self.request.method == "GET" else IsAuthenticated
        return [permission_class()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.pk
        self.perform_destroy(instance)
        return Response({"id": instance_id}, status=status.HTTP_200_OK)