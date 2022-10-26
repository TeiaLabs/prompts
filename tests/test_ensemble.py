import pytest 
from prompts.ensemble import PromptEnsemble
from prompts import DynamicPrompt


def test_ensemble():
    templates = ['<label>', 'a photo of <label>', 'picture of <label>']
    vars = ['label']
    
    prompt = PromptEnsemble(templates, vars)

    prompted_list = prompt.build(label='dog')    

    assert len(prompted_list) == 3
    assert prompted_list[0] == 'dog'
    assert prompted_list[1] == 'a photo of dog'
    assert prompted_list[2] == 'picture of dog'

    with pytest.raises(ValueError):
        _ = prompt.build(img_class='cat')


def test_build_many():
    templates = ['<label>', 'a photo of <label>']
    im_vars = ['label']
    classes = ['dog', 'cat', 'horse']
    
    prompt = PromptEnsemble(templates, im_vars)

    prompted_list = prompt.build_many(label=classes)

    print(prompted_list)

    assert len(prompted_list) == 6
    assert prompted_list[0] == 'dog'
    assert prompted_list[1] == 'a photo of dog'
    assert prompted_list[2] == 'cat'
    assert prompted_list[3] == 'a photo of cat'
    assert prompted_list[4] == 'horse'
    assert prompted_list[5] == 'a photo of horse'

    with pytest.raises(ValueError):
        _ = prompt.build(labels=['cat'])


def test_build_many_multiple_args():
    templates = ['<label>/<superclass>', 'a photo of <label>/<superclass>']
    im_vars = ['label', 'superclass']
    labels = ['dog', 'cat', 't-shirt']
    superclasses = ['animal', 'animal', 'clothes']
    
    prompt = PromptEnsemble(templates, im_vars)

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
    with pytest.raises(ValueError):
        prompted_list = prompt.build_many(
            label=labels,
            superclass=superclasses[:-1],
        )


def test_invalid_ensemble_template():
    templates = ['<label>', 'a photo of <img_class>', 'picture of <label>']
    vars = ['label']

   # expect exception
    with pytest.raises(ValueError):
        _ = PromptEnsemble(templates, vars)


def test_prompt_ensemble_from_file():
    prompts = []
    for i in range(3):
        prompt_file = 'samples/sample.prompt'
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