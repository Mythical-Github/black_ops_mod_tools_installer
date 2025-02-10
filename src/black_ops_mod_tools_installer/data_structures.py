from enum import Enum
from dataclasses import dataclass


class ExtractionType(Enum):
    """
    enum for when to extract files, before or after the converter is ran
    """
    PRE_CONVERTER = 'pre_converter'
    POST_CONVERTER = 'post_converter'


def get_enum_from_val(enum: Enum, value: str) -> Enum:
    for member in enum:
        if member.value == value:
            return member
    return None


def get_enum_strings_from_enum(enum: Enum) -> list[str]:
    strings = []
    for entry in enum:
        strings.append(entry.value)
    return strings


@dataclass
class ContentPackConfigStructure:
    executable: str
    executable_args: list[str]
