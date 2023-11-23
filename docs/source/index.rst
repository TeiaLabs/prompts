AIPrompts Documentation
=======================

AIPrompts is a package that provides powerful and flexible abstractions to **create and render prompts** for Large Language Models (LLMs).
The library provides a prompt object abstraction/interface that is used to represent prompts in a generic fashion.
Then, these prompts can be rendered to become compatible with multiple LLM provider/model configurations with minimal code changes.
Additionally, the library can be easily extended to support custom use cases.

To begin using AIPrompts, please refer to the :doc:`Getting Started <getting_started/index>` guides.

Core Features
-------------

* **Flexible:** create and compose prompt objects via a unified interface
* **Templating:** model dynamic behaviors via templating engines (`Jinja2 <https://jinja.palletsprojects.com/en/>`_)
* **Multi-format:** switch between different prompt formats/standards
* **Multimodal:** use multimodal prompt inputs (e.g., texts, images, etc.)
* **Generic:** use prompt templates for several applications and tasks
* **Extensible:** add support for your custom use cases and data types
* **Serializable:** serialize and deserialize prompts and their components
* **Examples:** library of examples for common and specific use cases

Why Choose AIPrompts
--------------------

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

* `Aims to solve a single problem <https://en.wikipedia.org/wiki/Unix_philosophy>`_
* Is minimally intrusive to your workflow
* Can be adapted to your needs
* Can be used alongside other libraries

Then AIPrompts is probably a good fit.

Quick Links
-----------

* :doc:`Getting Started<getting_started/index>`: installation and quickstart demo.
* :doc:`Modules Overview <modules/index>`: understand the purpose of the core modules.
* :doc:`API Reference <api_reference/index>`: complete API reference.
* `GitHub Repository <https://github.com/TeiaLabs/prompts>`_: source code, issue tracker, and other resources.
* `PyPI <https://pypi.org/project/AIPrompts/>`_: official PyPI page of AIPrompts for Python.

.. page divider
.. raw:: html

   <hr>


.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Getting Started
   :name: getting_started

   getting_started/index
   getting_started/installation
   getting_started/quickstart

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Modules
   :name: modules

   modules/index
   modules/artifacts
   modules/prompts
   modules/renderers

.. toctree::
   :hidden:
   :glob:
   :caption: Examples
   :name: examples

   examples/*
   examples/text_completion/*

.. toctree::
   :glob:
   :hidden:
   :maxdepth: 2
   :caption: API Reference
   :name: api_reference

   api_reference/index
   api_reference/*


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
