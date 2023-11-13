from prompts.artifact.chat import ChatMessageArtifact
from prompts.artifact.text import TextArtifact
from prompts.rendering import chat as chat_rendering


def main():
    artifact_template_with_var = TextArtifact(
        name="artifact_template_with_var",
        content="Artifact Template with subvar: {{ foo.bar }}",
    )
    message_content = TextArtifact(
        name="message_content",
        content="Variable: {{ foo.bar }}. Artifact as template: {% include 'artifact_template_with_var' %}",
    )
    chat_message = ChatMessageArtifact(
        name="chat_message",
        content="{{ message_content }}",
        role="user",
        sender_name="John",
    )

    context = {
        "foo": {"bar": "baz"},
        "artifact_template_with_var": artifact_template_with_var,
        "message_content": message_content,
    }

    referenced_vars = chat_message.get_referenced_variables(
        recursive=True,
        **context,
    )
    print(f"Referenced variables ({len(referenced_vars)}): {referenced_vars}")

    rendered = chat_message.render(
        strict=True,
        # chat_message_renderer=chat_rendering.chat_message_to_string,
        **context,
    )
    print(rendered)


if __name__ == "__main__":
    main()
