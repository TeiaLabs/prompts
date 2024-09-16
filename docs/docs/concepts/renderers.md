# Renderers

A **Renderer** is a callable that receives an [Artifact](./artifacts.md) as a parameter and returns a rendered version of the artifact.
When you call the `render` method of an artifact, you can specify which renderer to use.
If you don't provide one, the artifact's default renderer will be used.
Separating the artifact data structure from the rendering logic allows us to support multiple output formats and facilitates the creation of custom renderering logic.

Quick links:

* [prompts.rendering][]: rendering API reference.

## The Rendering Interface

Each artifact type defines its own rendering interface, and the general pattern is as follows:

```py
ArtifactRenderer = Callable[["ArtifactClass"], Any]
```

!!! note
    The return type of the renderer is not specified, as it can be anything from a string to a complex object.
    However, keep in mind that if you are rendering a text-based artifact, the renderers you use should probably return strings.
    It is up to the user to ensure that a renderer is compatible with the set of artifact types they are using.

## Using Renderers

To use a renderer, you must provide it to the `render` method of the artifact.
For instance, for the [`ChatMessageArtifact`][prompts.artifact.chat.ChatMessageArtifact], you can use the renderers defined in [prompts.rendering.chat][prompts.rendering.chat] or create your own:

```py title="Chat Message And Renderers"
from prompts.artifact.chat import ChatMessageArtifact
from prompts.rendering.chat import chat_message_to_string


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

# Custom renderer that returns only the message content
def custom_renderer(chat_message: ChatMessageArtifact) -> str:
    return chat_message.content

rendered_custom = chat_message.render(chat_message_renderer=custom_renderer)
print(rendered_custom)
```

```txt title="Chat Message And Renderers - Output"
{'content': 'Hello!', 'role': 'user', 'name': 'John'}
user (John): Hello!
Hello!
```
