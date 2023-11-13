import base64
from io import BytesIO
from pathlib import Path

from PIL import Image


def load_image_as_base64_string(img_path: Path) -> str:
    """Loads an image from a path and returns it as a base64 encoded string."""
    buffer = BytesIO()
    img_pil = Image.open(img_path)
    img_pil.save(buffer, format=img_pil.format)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
