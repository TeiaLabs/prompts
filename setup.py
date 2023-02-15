from __future__ import annotations

import subprocess
from pathlib import Path

import setuptools


def read_multiline_as_list(file_path: Path | str) -> list[str]:
    with open(file_path) as req_file:
        contents = req_file.read().split("\n")
        if contents[-1] == "":
            contents.pop()
        return contents


version = (
    subprocess.check_output(["git", "describe", "--tags"])
    .decode()
    .strip()
)
requirements = read_multiline_as_list("requirements.txt")

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="AIPrompts",
    version=version,
    author="Teialabs",
    author_email="jonatas@teialabs.com",
    description="Create and parse prompts for OpenAI models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TeiaLabs/prompts",
    packages=setuptools.find_packages(),
    keywords="prompt openai teialabs gpt3",
    python_requires=">=3.10",
    install_requires=requirements,
)
