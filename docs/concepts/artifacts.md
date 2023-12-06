# Artifacts

An **Artifact** is a data structure and interface used to represent different types of **prompt components** (i.e., the elements that make up a prompt).
The rationale behind this abstraction is to enable the creation of a **modular** and **extensible** prompt building system that also supports **multiple data types** (e.g., for multimodal prompting scenarios).
Artifacts can be serialized and deserialized using Pydantic 2 idioms.

Quick links:

* [`BaseArtifact`][prompts.artifact.base.BaseArtifact]: base interface that all artifacts must implement.
* [prompts.artifact][]: artifact API reference.

## `BaseArtifact` - The Artifact Interface

All artifacts must inherit from the [`BaseArtifact`][prompts.artifact.base.BaseArtifact] class.
Since artifacts can be nested and composed, the goal of this interface is to define a few important methods and attributes that help during artifact/prompt building and rendering.

Important attributes:

* [`name`][prompts.artifact.base.BaseArtifact.name]: unique identifier for an artifact.
* [`type`][prompts.artifact.base.BaseArtifact.type]: type of the artifact.
* [`content`][prompts.artifact.base.BaseArtifact.content]: data associated with an artifact.

Important methods:

* [`get_referenced_variables`][prompts.artifact.base.BaseArtifact.get_referenced_variables]: allows for the discoverability of referenced artifacts.
This method can also used to inform the user of an artifact's dependencies.
* [`render`][prompts.artifact.base.BaseArtifact.render]: allows the rendering of artifact data into a format suitable for prompts.
Depending on the data type that an artifact is abstracting, the implementation of this method can vary wildly.
When an artifact reference is encountered during rendering, the system will call the reference's `render` method to resolve the dependency.

## Text-based Artifacts

Most LLM use cases involve at least text as a data type.
We provide a few text-based artifacts to help build text-based prompts.
All base text artifacts provide Jinja templating support.

* [`TextArtifact`][prompts.artifact.text.TextArtifact]: represents raw text data.
* [`ChatMessageArtifact`][prompts.artifact.chat.ChatMessageArtifact] represents a chat message.

### `TextArtifact` - Examples

Jinja templating:

```py title="Basic Jinja Templating"
text_artifact = TextArtifact(
    name="text_artifact",
    content="This text artifact references a variable: {{ foo }}",
)

context = {"foo": "bar"}
rendered_text = text_artifact.render(**context)
print(rendered_text)
```

```txt title="Basic Jinja Templating - Output"
This text artifact references a variable: bar
```

Referencing other artifacts:

```py title="Referencing Another Text Artifact"
artifact1 = TextArtifact(
    name="artifact1",
    content="Foo.",
)

artifact2 = TextArtifact(
    name="artifact2",
    content="\n".join([
        "Referencing using Jinja variable: {{ artifact1 }}",
        "Referencing using Jinja include: {% include 'artifact1' %}",
    ])
)

context = {"artifact1": artifact1}
rendered_text = artifact2.render(**context)
print(rendered_text)
```

```txt title="Referencing Another Text Artifact - Output"
Referencing using Jinja variable: Foo.
Referencing using Jinja include: Foo.
```

Recursive resolution when rendering

```py title="Recursive Resolution"
artifact1 = TextArtifact(
    name="artifact1",
    content="Var1: {{ var1 }}.",
)

artifact2 = TextArtifact(
    name="artifact2",
    content="{{ artifact1 }}\nVar2: {{ var2 }}.",
)

context = {"artifact1": artifact1, "var1": "foo", "var2": "bar"}
rendered_text = artifact2.render(**context)
print(rendered_text)
```

```txt title="Recursive Resolution - Output"
Var1: foo.
Var2: bar.
```

### `ChatMessageArtifact` - Examples

Basic chat message with different renderers:

```py title="Chat Message And Renderers"
chat_message = ChatMessageArtifact(
    name="chat_message",
    content="Hello!",
    role="user",
    sender_name="John",
)

# Default renderer (OpenAI ChatML dict)
rendered_chatml = chat_message.render()
print(rendered_chatml)

# String renderer
from prompts.rendering.chat import chat_message_to_string
rendered_text = chat_message.render(chat_message_renderer=chat_message_to_string)
print(rendered_text)
```

```txt title="Chat Message And Renderers - Output"
{'content': 'Hello!', 'role': 'user', 'name': 'John'}
user (John): Hello!
```

## Multimodality

Text with image reference:

```py title="Text With Image Reference"
text_artifact = TextArtifact(
    name="text_artifact",
    content="This is an image: {{ image_artifact }}",
)

image1 = ImageArtifact(
    name="image1",
    content="data:image/jpeg;base64,[...]",
    content_encoding="base64",
)

context = {"image1": image1}
rendered_text = text_artifact.render(**context)
print(rendered_text)
```

```txt title="Text With Image Reference - Output"
This is an image: <artifact_img_start>image1<artifact_img_end>
```
