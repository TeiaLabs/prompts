import inspect
from typing import Any

from pydantic import (
    SerializeAsAny,
    ValidationError,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    WrapValidator,
)
from pydantic.error_wrappers import ErrorWrapper
from typing_extensions import Annotated

from ..artifact.base import BaseArtifact


def get_all_subclasses[T](base_class: type[T]) -> tuple[type[T]]:
    """
    Get all subclasses of a given base class.

    Args:
        base_class: The base class to get subclasses of.

    Returns:
        A tuple of all subclasses of the given base class.
    """
    subclasses = set()

    def recurse(cls: type[T]):
        for subclass in cls.__subclasses__():
            if not inspect.isabstract(subclass):
                subclasses.add(subclass)
            recurse(subclass)

    recurse(base_class)
    out = tuple(subclasses)
    return out


def artifact_subtype_converter(
    v: Any,
    handler: ValidatorFunctionWrapHandler,
    info: ValidationInfo,
) -> Any:
    """
    Converts a dict to a valid subclass of BaseArtifact.

    Args:
        v: The value to convert.
        handler: The handler to use.
        info: The validation info to use.

    Raises:
        ValidationError: If no subclass matches.

    Returns:
        The converted value.
    """
    if not isinstance(v, dict):
        return handler(v)

    # TODO: see if we can substitute this for a Discriminator
    # https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions
    for subclass in get_all_subclasses(BaseArtifact):
        if type := subclass.model_fields.get("type"):
            if type.default == v.get("type", None):
                return subclass.model_validate(v)

    raise ValidationError(
        [
            ErrorWrapper(
                ValueError(
                    f"Invalid artifact type: {v.get('type', None)}. "
                    f"Expected one of: {[subclass.model_fields['type'].default for subclass in get_all_subclasses(BaseArtifact)]}"
                ),
            )
        ],
        model=BaseArtifact,
    )


AnyArtifact = Annotated[
    SerializeAsAny[BaseArtifact],
    WrapValidator(artifact_subtype_converter),
]
