# Concepts

AIPrompts provides several abstractions and extensible interfaces for working with LLM prompts.
To better understand how concepts related to prompts are represented in AIPrompts, please take a look at the following topics:

* [Artifacts:](./artifacts.md) representation of data types used in prompts.
* [Prompts:](./prompts.md) representation of a prompt for a specific task.
* [Renderers:](./renderers.md) deal with artifact rendering to support different output formats.

``` mermaid
---
title: Relationship Between Library Concepts
---
graph LR
    renderers["Renderers"]
    artifacts["Artifacts"]
    prompts["Prompts"]
    renderers --->|Used by| artifacts
    artifacts --->|Contained in| prompts
```
