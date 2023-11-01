# Prompts

## Prompt Types

- LLM prompts (OpenAI, HuggingFace, Meta)
  - Chat prompt
- Text-to-image prompts (Midjourney, DALL-E, StableDiffusion)

## Prompt Formats

- LLM prompts
  - OpenAI (ChatML, <https://github.com/openai/openai-python/blob/main/chatml.md>)
  - HuggingFace (OpenChat, <https://huggingface.co/openchat/openchat>)
  - Meta (LLaMA, <https://huggingface.co/blog/llama2#how-to-prompt-llama-2>)
  - Anthropic (Claude, <https://docs.anthropic.com/claude/docs/constructing-a-prompt#use-the-correct-format>)
  - Other LLM providers

- Midjourney prompts (<https://docs.midjourney.com/docs/prompts>)
  - Text description prompt
  - Image prompt
  - Parameters prompt
  - Weights

- Prompt payload metadata
  - Images (embedded? URL?) for multimodal models

- Custom export formats
  - Serialization?
  - Web UI?
  - Improved readability?

## Ideas

- Templating engine (jinja)
- Model LLM prompts at the message level
- Prompt graph to create complex prompts from simple ones
- Predefined messages/prompts for common NLP tasks
- Prompt Drivers for each model (handles model/execution configuration)
- Concatenate text messages to form a single message

- TextMessage
  - Templated string
  - Metadata (?)
  - Additional message data (image URLs? maybe model as XMessage type?)

- ChatMessage
  - TextMessage
  - ChatMessageRole

- ChatPrompt
  - ChatMessage[]
  - Prompt metadata

## Libraries

- <https://github.com/promptslab/Awesome-Prompt-Engineering>
- <https://github.com/griptape-ai/griptape>
- <https://github.com/langchain-ai/langchain>
- <https://github.com/promptslab/Promptify>
- <https://github.com/jerryjliu/llama_index>
