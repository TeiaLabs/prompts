# AIPrompts Documentation

AIPrompts is a package that provides powerful and flexible abstractions to **create and render prompts** for Large Language Models (LLMs).
The library provides a prompt object abstraction/interface that is used to represent prompts in a generic fashion.
Then, these prompts can be rendered to become compatible with multiple LLM provider/model configurations with minimal code changes.
Additionally, the library can be easily extended to support custom use cases.

To begin using AIPrompts, please refer to the Getting Started guides.

## Core Features

* **Flexibility:** create and compose prompt objects via a unified interface
* **Templating:** model dynamic behaviors via templating engines ([Jinja2](<https://jinja.palletsprojects.com/en/>))
* **Multi-format:** switch between different prompt formats/standards
* **Multimodal:** use multimodal prompt inputs (e.g., texts, images, etc.)
* **Generic:** use prompt templates for several applications and tasks
* **Extensibility:** add support for your custom use cases and data types
* **Serialization:** serialize and deserialize prompts and their components
* **Examples:** library of examples for common and specific use cases

## Why Choose AIPrompts

Unlike many other LLM-related libraries and frameworks---that frequently become bloated, opinionated, and monolithic---, AIPrompts is not meant to be a full-fledged LLM execution framework.
This was a deliberate design decision that allows this library to focus solely on one step of the LLM execution pipeline: *prompts*.

With that in mind, AIPrompts does **NOT** provide support for:

* Calling model providers and parsing their outputs
* Managing model configurations and execution parameters
* Database connection and querying
* Execution chaining
* Token counting, text chunking, asynchronous execution, agent plugins, API key handling, ...

If you are looking for a library that provides all of the above, then AIPrompts is probably not for you.

However, if you are looking for a library that:

* [Aims to solve a single problem](<https://en.wikipedia.org/wiki/Unix_philosophy>)
* Is minimally intrusive to your workflow
* Can be adapted to your needs
* Can be used alongside other libraries

Then AIPrompts is probably a good fit.

## Quick Links

* Getting Started: installation and quickstart demo.
* Modules Overview : understand the purpose of the core modules.
* API Reference: complete API reference.
* [GitHub Repository](<https://github.com/TeiaLabs/prompts>): source code, issue tracker, and other resources.
* [PyPI](<https://pypi.org/project/AIPrompts/>): official PyPI page of AIPrompts for Python.
