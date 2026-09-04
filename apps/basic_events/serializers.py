from rest_framework import serializers
from apps.basic_events.models import (
    BasicEvent,
    BibleReference,
    HeroImage,
    WelcomeContent,
    LastestSermon,
    HeroGallery,
)

class BasicEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicEvent
        fields = "__all__"

class BibleReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BibleReference
        fields = "__all__"

class HeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroImage
        fields = "__all__"

class WelcomeContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WelcomeContent
        fields = "__all__"

class LastestSermonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastestSermon
        fields = "__all__"

class HeroGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroGallery
        fields = "__all__"