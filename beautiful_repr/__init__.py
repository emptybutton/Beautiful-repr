from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass, field
from typing import Callable, Iterable


def _get_all_parents_by(class_: type) -> set[type, ]:
    parents = set(class_.__bases__)

    for parent in class_.__bases__:
        parents.update(_get_all_parents_by(parent))

    return parents


class _AdvancingCounter:
    """
    Counter whose life goal, when called, is to return a larger number than the
    previous one.

    The first number returned is counted from the "start_number" input argument.
    All subsequent return values are greater than the previous one by the "step"
    input argument.
    """

    def __init__(self, start_number: int | float = 0, step: int | float = 1):
        self.__counted = start_number
        self.step = step

    def __call__(self) -> int | float:
        self.__counted += self.step

        return self.__counted

    @property
    def counted(self) -> int | float:
        return self.__counted


@dataclass(frozen=True)
class Field:
    """
    Field model for containing the parser and formatter and organizing their
    collaboration to format the real field for subsequent exploitation by FieldRepr
    descendants.
    """

    name: str | None = None
    importance_index: int = field(default_factory=_AdvancingCounter())
    value_getter: Callable[[object, str], any] = lambda object_, field_name: getattr(object_, field_name)
    formatter: Callable[[any, str], str] = lambda value, field_name: f"{field_name}={value}"

    def get_formated_by(self, object_with_field: object) -> str:
        return self.formatter(self.value_getter(object_with_field, self.name), self.name)


class BaseRepr(ABC):
    """
    Base class for getting the string version of the input object when called.

    Contains (specifically it does not) a template for formatting an object and
    receives arguments for formatting it using the get_arguments_for_format_by
    method.
    """

    template: str

    def __call__(self, object_to_format: object) -> str:
        args_for_formating, kwargs_for_formating = self.get_arguments_for_format_by(object_to_format)

        return self.template.format(*args_for_formating, **kwargs_for_formating)

    @abstractmethod
    def get_arguments_for_format_by(self, object_: object) -> tuple[tuple, dict]:
        pass


class FieldRepr(BaseRepr, ABC):
    """Stores field models for formatting."""

    def __init__(self, fields: Iterable[Field,]):
        self.fields = tuple(fields)


class BeautifulRepr(FieldRepr):
    """
    Really great object formatter.

    Contains a great template, an implementation of getting attributes for it
    using field models and a delimiter string for their formatting results.
    """

    template = "{class_name}({formatted_fields})"
    field_delimiter = ", "

    def get_arguments_for_format_by(self, object_: object) -> tuple[tuple, dict]:
        return (
            tuple(),
            {
                "class_name": object_.__class__.__name__,
                "formatted_fields": self.field_delimiter.join(
                    (
                        field.get_formated_by(object_)
                        for field in sorted(self.fields, key=lambda field: field.importance_index)
                    )
                )
            }
        )


class FieldFormatter(ABC):
    """Formatters for the field model."""

    @abstractmethod
    def __call__(self, value: any, field_name: str) -> str:
        pass


class TemplateFormatter(FieldFormatter):
    def __init__(self, template: str):
        self.template = template

    def __call__(self, value: any, field_name: str) -> str:
        return self.template.format(value=value)


class StylizedMeta(ABCMeta):
    """
    Abstarct meta class.
    With the creation of the class, it also creates a repr for it.
    """

    def __new__(cls, class_name: str, super_classes: tuple, attributes: dict):
        class_ = super().__new__(cls, class_name, super_classes, attributes)
        class_.__init_repr__()

        return class_

    def __init_repr__(cls) -> BaseRepr:
        raise NotImplementedError


class FieldStylizedMeta(StylizedMeta):
    """
    Initializes the field repr. To work correctly, the class must be similar to
    StylizedMixin or contain the _repr_factory and _repr_fields attributes.
    """

    def __init_repr__(cls) -> BaseRepr:
        cls._repr = cls._repr_factory(frozenset(sum(
            (
                tuple(class_._repr_fields)
                for class_ in (cls, *_get_all_parents_by(cls))
                if hasattr(class_, '_repr_fields')
            ),
            tuple()
        )))


class StylizedMixin(metaclass=FieldStylizedMeta):
    """
    Class for replacing the default repr with an external one, stored in the
    "repr" attribute.
    """

    _repr_factory: Callable[[Field, ], BaseRepr] = BeautifulRepr
    _repr_fields: Iterable[Field, ]

    def __repr__(self) -> str:
        return self._repr(self)


def parse_length(object_: object, attribute_name: str):
    """
    Simple getter function for the Field model that returns the length of an
    attribute by its name.
    """

    return len(getattr(object_, attribute_name))
