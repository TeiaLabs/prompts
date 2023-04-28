from typing import Any

import yaml


def load_yaml(filename: str) -> dict[str, Any]:
    with open(filename) as f:
        prompt = yaml.safe_load(f)
    return prompt
