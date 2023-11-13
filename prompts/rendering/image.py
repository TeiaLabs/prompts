from ..artifact.image import ImageArtifact

# TODO: for base64-encoded images, we should handle "data:image/jpeg;base64,".

def image_to_placeholder(artifact: ImageArtifact) -> str:
     return f"<artifact_img_start>{artifact.name}<artifact_img_end>"


def image_to_metadata(artifact: ImageArtifact) -> str:
    image_size = "Not available."
    if artifact.content_encoding == "base64":
        image_size = base64_size_bytes(artifact.content)
    elif artifact.content_encoding == "bytes":
        image_size = len(artifact.content)

    message = "".join(
        [
            "Image Metadata - ",
            f"Name: {artifact.name!r}, ",
            f"Content Encoding: {artifact.content_encoding!r}, ",
            f"Size (bytes): {image_size}" if image_size else "",
        ]
    )
    return message


def image_to_pillow_image(artifact: ImageArtifact) -> "PIL.Image":  # type: ignore
    import base64
    from io import BytesIO
    from PIL import Image

    img_content = artifact.content
    if artifact.content_encoding == "base64":
            img_content = base64.b64decode(img_content)
    image = Image.open(BytesIO(img_content))
    return image


def image_to_caption(artifact: ImageArtifact) -> str:
    from transformers import pipeline
    pil_image = image_to_pillow_image(artifact)
    image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
    caption = image_to_text(pil_image)[0]["generated_text"]
    return f"Caption for {artifact.name!r}: {caption}"


def base64_size_bytes(b64string: str) -> int:
    """Calculate the approximate size in bytes of a base64 encoded string."""
    if isinstance(b64string, bytes):
        b64string = b64string.decode("utf-8")
    return (len(b64string) * 3 // 4) - b64string.count("=", -2)
