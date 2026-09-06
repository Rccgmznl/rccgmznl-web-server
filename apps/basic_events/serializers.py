from rest_framework import serializers
from apps.events.services import upload_gallery_image_file, validate_gallery_image_file
from apps.basic_events.models import (
    BasicEvent,
    BibleReference,
    HeroImage,
    WelcomeContent,
    Sermon,
    HeroGallery,
    About,
)

class BasicEventSerializer(serializers.ModelSerializer):
    cover_image = serializers.FileField(write_only=True, required=False)
    cover_image_url = serializers.URLField(read_only=True)
    external_url = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = BasicEvent
        fields = "__all__"

    def validate_cover_image(self, value):
        validate_gallery_image_file(value)
        return value

    def create(self, validated_data):
        cover_image = validated_data.pop("cover_image", None)
        if cover_image is None:
            raise serializers.ValidationError({"cover_image": "This field is required."})

        upload_result = upload_gallery_image_file(
            cover_image,
            request=self.context.get("request"),
        )
        validated_data["cover_image_url"] = upload_result["url"]
        return super().create(validated_data)

    def update(self, instance, validated_data):
        cover_image = validated_data.pop("cover_image", None)
        if cover_image is not None:
            upload_result = upload_gallery_image_file(
                cover_image,
                request=self.context.get("request"),
            )
            validated_data["cover_image_url"] = upload_result["url"]

        return super().update(instance, validated_data)

class BibleReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BibleReference
        fields = "__all__"

class HeroImageSerializer(serializers.ModelSerializer):
    image = serializers.FileField(write_only=True, required=False)
    url = serializers.URLField(read_only=True)
    order = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = HeroImage
        fields = "__all__"

    def validate_image(self, value):
        validate_gallery_image_file(value)
        return value

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        if image is None:
            raise serializers.ValidationError({"image": "This field is required."})

        upload_result = upload_gallery_image_file(
            image,
            request=self.context.get("request"),
        )
        validated_data["url"] = upload_result["url"]
        return super().create(validated_data)

    def update(self, instance, validated_data):
        image = validated_data.pop("image", None)
        if image is not None:
            upload_result = upload_gallery_image_file(
                image,
                request=self.context.get("request"),
            )
            validated_data["url"] = upload_result["url"]

        return super().update(instance, validated_data)

    def validate_order(self, value):
        if (
            self.instance
            and HeroImage.objects.exclude(pk=self.instance.pk).filter(order=value).exists()
        ):
            raise serializers.ValidationError(
                "That order is already in use. Use the order endpoint to reorder images."
            )
        return value


class HeroImageOrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    order = serializers.IntegerField(min_value=1, max_value=10)


class HeroImageOrderSerializer(serializers.Serializer):
    images = HeroImageOrderItemSerializer(many=True)

    def validate_images(self, images):
        image_ids = [image["id"] for image in images]
        orders = [image["order"] for image in images]

        if len(image_ids) != len(set(image_ids)):
            raise serializers.ValidationError("Each hero image ID must be included only once.")
        if len(orders) != len(set(orders)):
            raise serializers.ValidationError("Each hero image order must be unique.")

        return images

class WelcomeContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WelcomeContent
        fields = "__all__"

class SermonSerializer(serializers.ModelSerializer):
    cover_image = serializers.FileField(write_only=True, required=False)
    cover_image_url = serializers.URLField(read_only=True)

    class Meta:
        model = Sermon
        fields = "__all__"

    def validate_cover_image(self, value):
        validate_gallery_image_file(value)
        return value

    def create(self, validated_data):
        cover_image = validated_data.pop("cover_image", None)
        if cover_image is None:
            raise serializers.ValidationError({"cover_image": "This field is required."})

        upload_result = upload_gallery_image_file(
            cover_image,
            request=self.context.get("request"),
        )
        validated_data["cover_image_url"] = upload_result["url"]
        return super().create(validated_data)

    def update(self, instance, validated_data):
        cover_image = validated_data.pop("cover_image", None)
        if cover_image is not None:
            upload_result = upload_gallery_image_file(
                cover_image,
                request=self.context.get("request"),
            )
            validated_data["cover_image_url"] = upload_result["url"]

        return super().update(instance, validated_data)


class SermonUploadRequestSerializer(serializers.ModelSerializer):
    cover_image = serializers.FileField(required=False)
    external_url = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Sermon
        fields = [
            "title",
            "description",
            "date",
            "cover_image",
            "cover_image_alt_text",
            "preacher",
            "tags",
            "external_url",
        ]

class HeroGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroGallery
        fields = "__all__"

class AboutSerializer(serializers.ModelSerializer):
    image = serializers.FileField(write_only=True, required=False)
    image_url = serializers.URLField(read_only=True)

    class Meta:
        model = About
        fields = "__all__"

    def validate_image(self, value):
        validate_gallery_image_file(value)
        return value

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        if image is None:
            raise serializers.ValidationError({"image": "This field is required."})

        upload_result = upload_gallery_image_file(
            image,
            request=self.context.get("request"),
        )
        validated_data["image_url"] = upload_result["url"]
        validated_data["id"] = 1
        return super().create(validated_data)

    def update(self, instance, validated_data):
        image = validated_data.pop("image", None)
        if image is not None:
            upload_result = upload_gallery_image_file(
                image,
                request=self.context.get("request"),
            )
            validated_data["image_url"] = upload_result["url"]

        return super().update(instance, validated_data)

