from pathlib import Path
from uuid import uuid4

from django.core.files.storage import default_storage
from django.utils import timezone
from rest_framework.exceptions import ValidationError

ALLOWED_GALLERY_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}
MAX_GALLERY_IMAGE_SIZE = 10 * 1024 * 1024
CONTENT_TYPE_TO_EXTENSION = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def validate_gallery_image_file(uploaded_file):
    content_type = getattr(uploaded_file, "content_type", None)
    if content_type not in ALLOWED_GALLERY_IMAGE_CONTENT_TYPES:
        raise ValidationError("Only JPEG, PNG, and WEBP files are allowed.")

    if uploaded_file.size > MAX_GALLERY_IMAGE_SIZE:
        raise ValidationError("File size must not exceed 10MB.")


def upload_gallery_image_file(uploaded_file, request=None):
    validate_gallery_image_file(uploaded_file)

    extension = Path(uploaded_file.name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        extension = CONTENT_TYPE_TO_EXTENSION.get(
            getattr(uploaded_file, "content_type", None),
            ".jpg",
        )

    subdir = timezone.now().strftime("gallery/%Y/%m")
    filename = f"{subdir}/{uuid4().hex}{extension}"
    stored_path = default_storage.save(filename, uploaded_file)
    file_url = default_storage.url(stored_path)

    if request is not None:
        file_url = request.build_absolute_uri(file_url)

    return {
        "url": file_url,
        "path": stored_path,
    }
