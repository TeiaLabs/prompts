import pytest

from prompts import DynamicPrompt, exceptions
from prompts.ensemble import PromptEnsemble


def test_ensemble():
    templates = ['<label>', 'a photo of <label>', 'picture of <label>']
    template_vars = ['label']
    
    prompt = PromptEnsemble(templates, template_vars)

    prompted_list = prompt.build(label='dog')    

    assert len(prompted_list) == 3
    assert prompted_list[0] == 'dog'
    assert prompted_list[1] == 'a photo of dog'
    assert prompted_list[2] == 'picture of dog'

    with pytest.raises(exceptions.UndefinedVariableError):
        _ = prompt.build(img_class='cat')

    assert len(prompt) == 3


def test_build_missing_args_valid():
    templates = ['<label>/<superclass>', 'a photo of <label>']
    template_vars = ['label', 'superclass']

    prompt = PromptEnsemble(templates, template_vars)

    prompted_list = prompt.build(
        label='dog',
        superclass='animal',
        strict=False,
    )
    expected = ['dog/animal', 'a photo of dog']

    assert len(prompted_list) == 2
    assert prompted_list == expected


def test_build_missing_args():
    templates = ['<label>/<superclass>', 'a photo of <label>']    

    with pytest.raises(exceptions.ExpectedVarsArgumentError):
        PromptEnsemble(templates, expected_vars=None)


def test_build_missing_args_invalid():
    templates = ['<label>', 'test']
    template_vars = ['label']

    with pytest.raises(exceptions.VariableNotInPromptError):
        _ = PromptEnsemble(templates, template_vars)


def test_build_many():
    templates = ['<label>', 'a photo of <label>']
    template_vars = ['label']
    classes = ['dog', 'cat', 'horse']
    
    prompt = PromptEnsemble(templates, template_vars)

    prompted_list = prompt.build_many(label=classes)    

    assert len(prompted_list) == 6
    assert prompted_list[0] == 'dog'
    assert prompted_list[1] == 'a photo of dog'
    assert prompted_list[2] == 'cat'
    assert prompted_list[3] == 'a photo of cat'
    assert prompted_list[4] == 'horse'
    assert prompted_list[5] == 'a photo of horse'

    with pytest.raises(exceptions.UndefinedVariableError):
        _ = prompt.build(labels=['cat'])


def test_build_many_multiple_args():
    templates = ['<label>/<superclass>', 'a photo of <label>/<superclass>']
    template_vars = ['label', 'superclass']
    labels = ['dog', 'cat', 't-shirt']
    superclasses = ['animal', 'animal', 'clothes']
    
    prompt = PromptEnsemble(templates, template_vars)

    prompted_list = prompt.build_many(
        label=labels,
        superclass=superclasses,
    )
    expected = [
        'dog/animal', 
        'a photo of dog/animal', 
        'cat/animal', 
        'a photo of cat/animal', 
        't-shirt/clothes', 
        'a photo of t-shirt/clothes',
    ]

    assert prompted_list == expected

    # Test error 
    with pytest.raises(exceptions.ArgumentNumberOfElementsError):
        prompted_list = prompt.build_many(
            label=labels,
            superclass=superclasses[:-1],
        )


def test_build_many_missing_args_valid():
    templates = ['<label>/<superclass>', 'a photo of <label>']
    template_vars = ['label', 'superclass']
    labels = ['dog', 'cat', 't-shirt']
    superclasses = ['animal', 'animal', 'clothes']

    prompt = PromptEnsemble(templates, template_vars)

    prompted_list = prompt.build_many(
        label=labels,
        superclass=superclasses,
        strict=False,
    )
    expected = [
        'dog/animal',
        'a photo of dog',
        'cat/animal',
        'a photo of cat',
        't-shirt/clothes',
        'a photo of t-shirt',
    ]

    assert len(prompted_list) == 6
    assert prompted_list == expected


def test_invalid_ensemble_template():
    templates = ['<label>', 'a photo of <img_class>', 'picture of <label>']
    template_vars = ['label']

   # expect exception
    with pytest.raises(exceptions.VariableNotInPromptError):
        _ = PromptEnsemble(templates, template_vars)


def test_prompt_ensemble_from_file():
    prompts = []
    for i in range(3):
        prompt_file = 'samples/sample.prompt.yaml'
        prompt = DynamicPrompt.from_file(prompt_file)
        prompts.append(prompt)
    
    prompt_ens = PromptEnsemble(prompts)
    prompt_str = prompt_ens.build(
        input_sentence='lets go'
    )
    assert len(prompt_str) == 3

    prompt_ens_ff = PromptEnsemble.from_paths(
        [prompt_file, prompt_file, prompt_file]
    )

    prompt_ff = prompt_ens_ff.build(
        input_sentence='lets go'
    )

    assert prompt_ff == prompt_str    