AIPrompts Documentation
=======================

AIPrompts is a package that provides powerful and flexible abstractions to **create and render prompts** for Large Language Models (LLMs).
The library provides a single prompt object abstraction/interface that is used to represent prompts in a generic fashion.
Then, these prompts can be rendered to become compatible with multiple LLM provider/model configurations with minimal code changes.
Additionally, the library can be easily extended to support custom use cases.

To begin using AIPrompts, please refer to the :doc:`getting_started/installation` and :doc:`getting_started/quickstart` guides.

Core Features
-------------

* Flexible prompt creation and composition
* Templating support (`Jinja2 <https://jinja.palletsprojects.com/en/>`_) to help model dynamic behaviors
* Support for different prompt formats/standards
* Multimodal prompt inputs (e.g., texts, images, audio, etc.)
* Prompt templates for several applications and tasks
* Extensible interfaces to support custom use cases and data types
* Serialization and deserialization capabilities
* Library of artifacts and prompts for common/specific use cases

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

* `GitHub Repository <https://github.com/TeiaLabs/prompts>`_: source code, issue tracker, and other resources.
* `PyPI <https://pypi.org/project/AIPrompts/>`_: official PyPI page of AIPrompts for Python.


.. page divider
.. raw:: html

   <hr>


.. toctree::
   :maxdepth: 1
   :caption: Getting Started
   :name: getting_started

   getting_started/installation
   getting_started/quickstart

.. toctree::
   :maxdepth: 1
   :caption: Modules
   :name: modules

   modules/index
   modules/artifacts
   modules/prompts
   modules/rendering

.. toctree::
   :glob:
   :caption: Examples
   :name: examples

   examples/*
   examples/text_completion/*

.. toctree::
   :maxdepth: 2
   :caption: API reference
   :name: api_reference

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
