from abc import ABC, abstractmethod


def parse_length(object_: object, attribute_name: str):
    """
    Simple getter function for the Field model that returns the length of an
    attribute by its name.
    """

    return len(getattr(object_, attribute_name))


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
