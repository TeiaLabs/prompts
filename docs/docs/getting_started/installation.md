# Installation

## Requirements

To use AIPrompts, you need to have Python 3.11 or higher installed.
We also recommend using a virtual environment to install the package's dependencies.

## Installing using `pip`

AIPrompts is [hosted on PyPI](https://pypi.org/project/AIPrompts/>) and can be installed using `pip`:

```bash
pip install aiprompts
```

This will install the latest release version of the package.

## Installing from Source

To install AIPrompts directly from its [GitHub repository](<https://github.com/TeiaLabs/prompts>), run the following command:

```bash
pip install git+https://github.com/TeiaLabs/prompts.git
```

## Installing from Source (Development)

If you are interested in contributing to AIPrompts or want to use the latest development versions, you can:

1. Clone the repository
2. Navigate to the repository folder
3. Check which dependencies you will require to run the package according to your needs (`requirements-<name>.txt` files in root folder)
4. Install the package in development mode (providing optional dependencies as needed)

To install AIPrompts in development mode without any optional dependencies, run the following command:

```bash
pip install -e .
```

If you want to contribute to the documentation and also run the tests, the following command would be needed:

```bash
pip install -e .[docs,test]
```

## Now What?

Now that you have AIPrompts installed, you can check out:

* [Quickstart Guide](./quickstart.md): getting started with the package.
* [Concepts Overview](../concepts/index.md): detailed explanation of the package's modules.
