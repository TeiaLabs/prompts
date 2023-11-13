from pathlib import Path

from prompts.artifact.image import ImageArtifact
from prompts.artifact.text import TextArtifact
from prompts.rendering import image as image_rendering
from prompts.utils.image import load_image_as_base64_string


def main():
    img_path = Path(__file__).parents[2] / "data" / "car.jpeg"
    img_base64 = load_image_as_base64_string(img_path)
    image = ImageArtifact(
        name="image",
        content=img_base64,
        content_encoding="base64",
    )

    rendered = image.render()
    print(rendered)

    text = TextArtifact(
        name="question",
        content="What is the color of the car in this image? {{ image }}",
    )

    context = {"image": image}
    rendered_text = text.render(
        image_renderer=image_rendering.image_to_caption,
        **context,
    )
    print(rendered_text)


if __name__ == "__main__":
    main()
