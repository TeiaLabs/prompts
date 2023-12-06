# Prompts

A **Prompt** is a data structure that contain [Artifact](./artifacts.md) references alongside other useful metadata (e.g., description, tags, tested model configurations, among others).
These objects serve as the final object that the user creates to define the prompt for a certain usage type or task.
Artifacts can be serialized and deserialized using Pydantic 2 idioms.

Quick links:

* [`BasePrompt`][prompts.prompt.base.BasePrompt]: base interface that all artifacts must implement.
* [prompts.prompt][]: prompt API reference.

## `BasePrompt` - The Prompt Interface

Similarly to artifacts, prompts also have a base interface that they must implement, the [`BasePrompt`][prompts.prompt.base.BasePrompt].
The `BasePrompt` interface also inherits from the [`BaseArtifact`][prompts.artifact.base.BaseArtifact] interface.
The goal of this interface is to standardize the way that prompts are defined to future-proof for the support of advanced features.

Important attributes:

* [`artifacts`][prompts.prompt.base.BasePrompt.artifacts]: list of artifacts referenced by the prompt.
* [`description`][prompts.prompt.base.BasePrompt.description]: what the prompt does.
* [`metadata`][prompts.prompt.base.BasePrompt.metadata]: additional metadata associated with the prompt.

Important methods:

* [`get_referenced_variables`][prompts.prompt.base.BasePrompt.get_referenced_variables]: allows for the discoverability of referenced artifacts.
This method can also used to inform the user of an artifact's dependencies.
* [`render`][prompts.prompt.base.BasePrompt.render]: allows the rendering of artifacts contained within the prompt.

## Common Prompt Types

Prompts can be used for a variety of tasks, such as chat completion, text classification, image classification, among others.
The prompts module providesa few prompt types for common text-based tasks:

* [`TextCompletionPrompt`][prompts.prompt.text_completion.TextCompletionPrompt]: text completion task.
* [`ChatCompletionPrompt`][prompts.prompt.chat_completion.ChatCompletionPrompt]: chat completion task.
