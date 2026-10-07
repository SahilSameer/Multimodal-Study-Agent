"""Validation and preparation of uploaded images."""
from io import BytesIO
from PIL import Image, UnidentifiedImageError

MAX_BYTES = 8 * 1024 * 1024      # 8 MB
MAX_SIDE = 1568                  # resize large photos to this longest side
MIN_SIDE = 200                   # reject images that are too small to read
ALLOWED_FORMATS = {"PNG", "JPEG", "WEBP"}


class ImageError(Exception):
    """Raised with a user-friendly message when an image cannot be used."""


def prepare_image(data: bytes):
    """Validate an uploaded image and return (jpeg_bytes, mime_type, PIL image)."""
    if len(data) > MAX_BYTES:
        raise ImageError("The image is larger than 8 MB. Please upload a smaller photo.")
    try:
        img = Image.open(BytesIO(data))
        fmt = img.format
        img.load()
    except (UnidentifiedImageError, OSError):
        raise ImageError("This file could not be read as an image.")
    if fmt not in ALLOWED_FORMATS:
        raise ImageError("Please upload a PNG, JPG or WEBP image.")
    if min(img.size) < MIN_SIDE:
        raise ImageError("The image is too small to read. Please upload a clearer photo.")
    img = img.convert("RGB")
    if max(img.size) > MAX_SIDE:
        img.thumbnail((MAX_SIDE, MAX_SIDE))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue(), "image/jpeg", img
