# Quickstart

!!! note
    This quickstart tutorial requires the library to be installed.
    If you haven't already, please follow the [installation guide](./installation.md).

In this quickstart, we'll walk through the basics of using the library to create an LLM text completion prompt.
We'll show you how to:

* [Create artifacts, which serve as the building blocks of your prompt](#creating-artifacts)
* [Show examples of Jinja templating features](#dynamic-artifacts-via-jinja-templating)
* [Create a prompt, which will reference a collection of artifacts](#creating-a-prompt)
* [Render a prompt based on its artifacts and custom variable inputs](#rendering-a-prompt)
* [Call a model provider to obtain a text completion answer based on our prompt](#calling-a-model-provider)
* [Serialize a prompt to a file for later use](#serializing-a-prompt)

## The Task At Hand

We are going to create a **text completion prompt** to model an assistant capable of **document question answering**.
Please note that one of the core features of the library is its flexibility; that means that there are several paths to achieve the same result and there is no "right" or "wrong" way to model a prompt.
You can break a prompt into several artifacts to increase reusability and clarity, or you can model the whole task in a single prompt.
Use your creativity and adapt the library to your needs.
Since the goal of this tutorial is to showcase the basics of the library, we'll model the task using artifacts, aiming for clarity instead of simplicity and efficiency.

## Creating Artifacts

One of the core concepts of the library is the [**Artifact**](../concepts/artifacts.md).
An artifact is used to model a data type that can be included in a prompt, such as texts, chat messages, images, among others.
The library also supports extending artifacts to support custom data types.
To use artifacts, you have to import them from the [artifact][prompts.artifact] module.
Since we only need to include texts in this tutorial, we'll import the [TextArtifact][prompts.artifact.text.TextArtifact] class:

```py
from prompts.artifact.text import TextArtifact
```

We'll begin by creating an artifact that models the instructions of the bot:

```py
qa_instructions = TextArtifact(
    name="qa_instructions",  # (1)
    content="\n".join([  # (2)
        "You are a helpful question answering bot.",
        "You will be provided with a CONTEXT (document) and a QUESTION.",
        "Your task is to ANSWER the QUESTION based on the CONTEXT.",
    ])
)
```

1. Every artifact MUST have a **unique** name when used in a prompt.
2. This represents the text of the text artifact.
In this example, we are concatenating several strings using the `join` method.

To check what the artifact will look like, we can call its [`render`][prompts.artifact.base.BaseArtifact.render] method:

```py
qa_instructions.render()
```

```txt title="Output"
You are a helpful question answering bot.
You will be provided with a CONTEXT (document) and a QUESTION.
Your task is to ANSWER the QUESTION based on the CONTEXT.
```

Next, we'll create an artifact that contains the Question-answering data placeholders:

```py
qa_data = TextArtifact(
    name="qa_data",
    content="\n".join([
        "CONTEXT:",
        "{{ document }}",  # (1)
        "QUESTION:",
        "{{ question }}",
        "ANSWER:"  # (2)
    ])
)
```

1. Text-based artifacts and prompts support **Jinja templating**.
When an artifact or a prompt is rendered, variables in its context can be used to replace these placeholders.
2. Here we are *prompting* the model so that it understands it should start with an answer.

This artifact contains template strings that need to be replaced when rendered.
To check which variables are needed, we can call the [`get_referenced_variables`][prompts.artifact.base.BaseArtifact.get_referenced_variables] method:

```py
qa_data.get_template_variables()
```

```txt title="Output"
{'document', 'question'}
```

We can also call its `render` method to check the output.
Note, however, that this artifact contains template strings, so it will not render correctly without a context.
Let's fix that by providing a context document and a question:

??? note "pytorch_wiki.md"
    This is the document that we will use as context for our prompt.

    ```md
    # PyTorch
    <!-- Extracted and adapted from  https://en.wikipedia.org/wiki/PyTorch (2023/12/04) -->

    **PyTorch** is a machine learning framework based on the Torch library, used for applications such as computer vision and natural language processing, originally developed by Meta AI and now part of the Linux Foundation umbrella.
    It is free and open-source software released under the modified BSD license.
    Although the Python interface is more polished and the primary focus of development, PyTorch also has a C++ interface.

    A number of pieces of deep learning software are built on top of PyTorch, including Tesla Autopilot, Uber's Pyro, Hugging Face's Transformers, PyTorch
    Lightning, and Catalyst.

    PyTorch provides two high-level features:

    - Tensor computing (like NumPy) with strong acceleration via graphics processing units (GPU)
    - Deep neural networks built on a tape-based automatic differentiation system

    ## History

    Meta (formerly known as Facebook) operates both *PyTorch* and *Convolutional Architecture for Fast Feature Embedding* (Caffe2), but models defined by the two frameworks were mutually incompatible.
    The Open Neural Network Exchange (ONNX) project was created by Meta and Microsoft in September 2017 for converting models between frameworks.
    Caffe2 was merged into PyTorch at the end of March 2018.
    In September 2022, Meta announced that *PyTorch* would be governed by PyTorch Foundation, a newly createdindependent organizationa subsidiary of Linux Foundation.

    PyTorch 2.0 was released on 15 March 2023.

    ## PyTorch tensors

    PyTorch defines a class called Tensor (`torch.Tensor`) to store and operate on homogeneous multidimensional rectangular arrays of numbers.
    PyTorch Tensors are similar to NumPy Arrays, but can also be operated on a CUDA-capable NVIDIA GPU.
    PyTorch has also been developing support for other GPU platforms, for example, AMD's ROCm and Apple's Metal Framework.

    PyTorch supports various sub-types of Tensors.

    Note that the term "tensor" here does not carry the same meaning as tensor in mathematics or physics.
    The meaning of the word in machine learning is only tangentially related to its original meaning as a certain kind of object in linear algebra.

    ## PyTorch neural networks

    PyTorch defines a class called nn (`torch.nn`) to describe neural networks and to support training.
    ```

```py
# Getting the context document
with open("pytorch_wiki.md", "r") as f:
    document = f.read()

# Creating rendering context
context = {
    "document": document,
    "question": "What is PyTorch?",
}

print(qa_data.render(**context))  # (1)
```

1. Here we are providing the additional context (as keyword arguments) to render the templated variables.

```txt title="Output"
CONTEXT:
# PyTorch
<!-- Extracted and adapted from  https://en.wikipedia.org/wiki/PyTorch (2023/12/04) -->

**PyTorch** is a machine learning framework based on the Torch library, used for applications [...]
QUESTION:
What is PyTorch?
ANSWER:
```

## Dynamic Artifacts Via Jinja Templating

So far, we have created two artifacts: one representing the instructions and another containing the question-answering inputs.
We will use them to create a prompt later on, but first, let's take a look at how to take advantage of Jinja templating in artifacts (and prompts).

!!! note
    If you want to know more about Jinja templating, you can check the [official Jinja documentation](https://jinja.palletsprojects.com/en/).

Let's say that we want to allow the user to provide additional instructions (i.e., rules) that the bot should follow when answering.
For instance, the user may want to instruct the model to answer in a specific format or to alter the bot's general behavior.
To do so, we will create another artifact that will deal with the user's ruleset:

```py
qa_ruleset = TextArtifact(
    name="qa_ruleset",
    content="\n".join([
        "You will also need to respect the following RULES:",
        "{% for rule in ruleset %}",  # (1)
        "- {{ rule }}",  # (2)
        "{% endfor %}",
    ])
)
```

1. We are using a Jinja `for` loop to iterate over the `ruleset` variable.
Jinja supports iterations, conditional statements, and many other features.
2. Here we are rendering each rule as a part of a bullet list.

Let's try rendering it with a context containing a ruleset:

```py
# Creating rendering context
context = {
    "ruleset": [
        "Answer like a pirate.",
        "If the answer is not contained within the document, you should return 'I don't know.'",
    ]
}

print(qa_ruleset.render(**context))
```

```txt title="Output"
You will also need to respect the following RULES:
- Answer like a pirate.
- If the answer is not contained within the document, you should return 'I don't know.'
```

To use this new artifact, we will include it in the `qa_instructions` artifact by recreating it:

```py hl_lines="7 8 9"
qa_instructions = TextArtifact(
    name="qa_instructions",
    content="\n".join([
        "You are a helpful question answering bot.",
        "You will be provided with a CONTEXT (document) and a QUESTION.",
        "Your task is to ANSWER the QUESTION based on the CONTEXT.",
        "{% if ruleset is defined %}",  # (1)
        "{% include 'qa_ruleset' %}",  # (2)
        "{% endif %}",
    ])
)
```

1. Here we are using a Jinja `if` statement to check if the `ruleset` variable is defined.
2. If the `ruleset` variable exists, we will include the `qa_ruleset` artifact by referencing its name.
There is also support for including artifacts as Jinja variables (e.g., `{{ qa_ruleset }}`).

Now, if the user provides a ruleset, it will be included in the `qa_instructions` artifact when rendered.

## Creating a Prompt

After declaring the artifacts, we can create a [`prompt`][prompts.prompt] that uses them.
There are many prompt types available; in this tutorial we will use a [`TextCompletionPrompt`][prompts.prompt.text_completion.TextCompletionPrompt]:

```py
from prompts.prompt.text_completion import TextCompletionPrompt
```

All prompt types inherit from a [`BasePrompt`][prompts.prompt.base.BasePrompt], which provides a few important attributes and methods.
For instance, we can use the `artifacts` attribute to provide a list of artifacts that the prompt can reference.
Let's create a prompt that uses our artifacts:

```py
completion_prompt = TextCompletionPrompt(
    name="document_qa_prompt",
    description="Provides answers based on a context document. Can be customized with additional rules.",
    content="\n".join([  # (1)
        "{{ qa_instructions }}",
        "{{ qa_data }}",
    ]),
    artifacts=[qa_instructions, qa_data, qa_ruleset],  # (2)
)
```

1. This is the *prompt* text.
A `TextCompletionPrompt` works very similarly to a `TextArtifact` and also supports Jinja templating.
2. We are providing the artifacts that the prompt can reference during rendering.
However, don't forget that we can still provide additional context as keyword arguments when rendering.

Notice that the `TextCompletionPrompt` object also has a `content` attribute that works similarly to a `TextArtifact` (it also supports Jinja templating).
We are using it here to combine the `qa_instructions` and `qa_data` artifacts, but since it supports Jinja, we could have modeled the entire prompt here (without using additional artifacts).
We chose to create separate artifacts for reusability and readability.
The library provides the means, but ultimately it is up to the user to decide how to model their prompts.
You can rely on Jinja templating for most cases, but you can also use a combination of artifacts and Jinja templating to create more complex prompts.

## Rendering a Prompt

In general, prompts work similarly to artifacts, in the sense that they can also be rendered to produce an output.
The following diagram depicts, at a high-level, the relationship between the context, artifacts, and prompt during the rendering phase:

``` mermaid
---
title: Quickstart Artifact, Context, and Prompt Diagram
---
graph LR
    subgraph context["Context"]
        direction LR
        document
        question
        ruleset

        document ~~~ question
        question ~~~ ruleset
    end

    subgraph completion_prompt["TextCompletionPrompt"]
        direction LR

        subgraph artifacts["artifacts"]
            direction LR
            qa_instructions
            qa_data
            qa_ruleset
        end

        qa_instructions ~~~ qa_data
        qa_data ~~~ qa_ruleset
    end

    context ~~~ completion_prompt

    document --> qa_data
    question --> qa_data
    ruleset --> qa_ruleset
    qa_ruleset --> qa_data
```

Let's call the `render` method of the `completion_prompt` object to render it:

```py
# Rendering the prompt
context = {
    "document": document,
    "question": "When was PyTorch 2.0 released?",
    "ruleset": [
        "Answer like a pirate.",
        "If the answer is not contained within the document, you should return 'I don't know.'",
    ],
}

completion_prompt_rendered = completion_prompt.render(**context)
print(completion_prompt_rendered)
```

```txt title="Output"
You are a helpful question answering bot.
You will be provided with a CONTEXT (document) and a QUESTION.
Your task is to ANSWER the QUESTION based on the CONTEXT.
You will also need to respect the following RULES:
- Answer in a single sentence.
- Answer like a pirate.
- If you use an abbreviation, explain it.
- If the answer is not contained within the document, you should return 'I don't know.'
CONTEXT:
# PyTorch
<!-- Extracted and adapted from  https://en.wikipedia.org/wiki/PyTorch (2023/12/04) -->

**PyTorch** is a machine learning framework based on the Torch library, used for applications [...]
QUESTION:
When was PyTorch 2.0 released?
ANSWER:
```

And that's it, we are ready to call a model provider!
Since this is a text-based task, the default renderers will suffice.
However, depending on the task or use case, we would have to provide different renderers for each artifact type.
For instance, for chatbot-based tasks, different model providers and model architectures may have incompatible formats.
Thus, we would have to provide renderers that can convert the artifacts into the appropriate format (e.g., OpenAI vs Anthropic chat API formats).
To read more about it, check out the [`Renderers`](../concepts/renderers.md) documentation.

## Calling a Model Provider

!!! note
    To run this part of the tutorial, you need to install the OpenAI Python library ([instructions here](https://platform.openai.com/docs/libraries/python-library)).

Now that we have a prompt, we can call a model provider to generate a response.
In this guide, we will use the OpenAI API, which provides access to the GPT model family.
After investigating the OpenAI documentation, we can see that the `completions.create` endpoint is the most appropriate for our use case:

```py
# OpenAI request
openai_api_key = "OPENAI_API_KEY"  # (1)
client = OpenAI(api_key=openai_api_key)

response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt=completion_prompt_rendered,  # (2)
    max_tokens=200,
    temperature=1.05,
)
print(response.choices[0].text)
```

1. You have to substitute this string for your own OpenAI API key.
2. We can provide the rendered version of the prompt directly.

```txt title="Output"
PyTorch be a machine learning framework based on the Torch library, used for plunderin' like computer vision and natural language processing, originally sailored by Meta AI and now part o' the Linux Foundation umbrella.
```

## Serializing a Prompt

The library uses [Pydantic 2](https://docs.pydantic.dev/latest/) to represent its core concepts, such as artifacts and prompts.
This allows us to serialize and deserialize our objects with ease, which can be useful for saving them to a database or sending them over a network.

!!! note
    If you want to know more about Pydantic, you can check the [official Pydantic 2 documentation](https://docs.pydantic.dev/latest/).

Let's first try to serialize an the `qa_instructions` artifact:

```py
print(qa_instructions.model_dump_json())
```

```json title="JSON Output"
{
    "name": "qa_instructions",
    "type": "text",
    "content": "You are a helpful question answering bot.\nYou will be provided with a CONTEXT (document) and a QUESTION.\nYour task is to ANSWER the QUESTION based on the CONTEXT.\n\n{% if ruleset is defined %}\n{% include 'qa_ruleset' %}\n{% endif %}",
    "content_encoding": "utf-8",
}
```

We can also serialize the `completion_prompt` object:

```py
print(completion_prompt.model_dump())
```

```json title="JSON Output"
{
    "name": "document_qa_prompt",
    "type": "prompt_text_completion",
    "content": "{{ qa_instructions }}\n{{ qa_data }}",
    "artifacts": [
        {
            "name": "qa_instructions",
            "type": "text",
            "content": "You are a helpful question answering bot.\nYou will be provided with a CONTEXT (document) and a QUESTION.\nYour task is to ANSWER the QUESTION based on the CONTEXT.\n\n{% if ruleset is defined %}\n{% include 'qa_ruleset' %}\n{% endif %}"
        },
        {
            "name": "qa_data",
            "type": "text",
            "content": "CONTEXT:\n{{ document }}\n\nQUESTION:\n{{ question }}\nANSWER:"
        },
        {
            "name": "qa_ruleset",
            "type": "text",
            "content": "You will also need to respect the following RULES:\n{% for rule in ruleset %}\n- {{ rule }}\n{% endfor %}\n"
        }
    ],
    "description": "Provides answers based on a context document. Can be customized with additional rules.",
    "metadata": null
}
```

## Next Steps

- [Concepts Overview](../concepts/index.md): Learn more about the core concepts of the library.
- [API Reference][prompts]: Get a detailed overview of the library's public API.
