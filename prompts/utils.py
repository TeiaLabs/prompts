import pyaml


def load_yaml(filename):
    with open(filename) as f:
        prompt = pyaml.yaml.load(f, Loader=pyaml.yaml.Loader)
    return prompt
