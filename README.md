# Prompt builder

This is a simple prompt builder for OpenAI models. Easy to use and to modify. To install this backage, run:

```python
pip install git+https://github.com/TeiaLabs/prompts.git
```

Build your own prompt by creating a file following a sample.prompt file, and use the DynamicPrompt class to parse it:

```python
prompt = DynamicPrompt.from_file('samples/sample.prompt')
str_prompt = prompt.build(
    input_sentence="lets go",
)
```

Alternatively, to get more control and better auto-complete suggestions, you can inherit from the `BasePrompt` class and override the build method with explicit arguments:

```python
class MyPrompt(BasePrompt):

    def build(self, input_sentence):
        return self.set_prompt_values(
            input_sentence=input_sentence,
        )
```
