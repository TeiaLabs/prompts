import pytest 
from prompts.ensemble import PromptEnsemble


def test_ensemble():
    templates = ['<label>', 'a photo of <label>', 'picture of <label>']
    vars = ['<label>']
    
    prompt = PromptEnsemble(templates, vars)

    prompted_list = prompt.build(label='dog')
    assert len(prompted_list) == 3
    assert prompted_list[0] == 'dog'
    assert prompted_list[1] == 'a photo of dog'
    assert prompted_list[2] == 'picture of dog'

    with pytest.raises(ValueError):
        _ = prompt.build(img_class='cat')


def test_invalid_ensemble_template():
    templates = ['<label>', 'a photo of <img_class>', 'piucture of <label>']
    vars = ['<label>']

   # expect exception
    with pytest.raises(ValueError):
        _ = PromptEnsemble(templates, vars)
