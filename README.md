# AIPrompts

This is a simple prompt builder for OpenAI models. Easy to use and to modify.

## Install

`pip install AIPrompts`

`pip install AIPrompts@git+https://github.com/TeiaLabs/prompts.git@master`

## Dynamic prompts

```python
template = 'a photo of a <img_label>'
prompt = DynamicPrompt(template)
filled_prompt = prompt.build(img_label='dog')
print(filled_prompt)
# out: "a photo of a dog"
```

## Dynamic prompts from file templates

Build your own prompt by creating a file following a sample.prompt file (yaml format), and use the DynamicPrompt class to parse it:

```python
prompt = DynamicPrompt.from_file('samples/sample.prompt')
str_prompt = prompt.build(
    input_sentence="lets go",
)
```

You can also access recommended model settings (engine, temperature) that can be fed to the model input (e.g., openai.Completion.create()):

```python
prompt.get_model_settings()
```

## Improve Autocomplete with custom prompts

Alternatively, to get more control and better autocomplete suggestions, you can inherit from the `BasePrompt` class and override the build method with explicit arguments:

```python
class MyPrompt(BasePrompt):

    def build(self, input_sentence):
        return self.set_prompt_values(
            input_sentence=input_sentence,
        )
```

## Ensembling prompts

To ensemble multiple prompts, you can use the `EnsemblePrompt` class:

```python
templates = [
    '<label>', 
    'a photo of <label>', 
    'picture of <label>',
]
exp_vars = ['label']
prompt = PromptEnsemble(templates, exp_vars)
prompt.build(label='dog')
# out: ['dog', 'a photo of dog', 'picture of dog']
prompt.build(label='cat')
# out: ['cat', 'a photo of cat', 'picture of cat']
```

The output is a flattened list with all filled in templates.
Note: all templates must be filled with the same expected variables, and all variables must be provided.

You can also build multiple promtps at the same time (useful for classification):

```python
templates = [
    '<label>',
    'a photo of <label>'
]
template_vars = [
    'label'
]
labels = ['dog', 'cat', 't-shirt']
prompt = PromptEnsemble(templates, template_vars)
prompt.build_many(
    label=labels
)
# out: ['dog', 'a photo of dog', 'cat', 'a photo of cat', 't-shirt', 'a photo of t-shirt']
```
