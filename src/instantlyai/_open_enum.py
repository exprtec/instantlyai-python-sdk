"""Enum base for generated models that tolerates values missing from the spec.

Instantly's API regularly returns enum values its published OpenAPI document
doesn't list (new ESP codes, statuses, ...). A closed enum turns every such
value into a ``ValidationError`` that fails the whole response -- often a whole
page of a paginated list. ``OpenEnum`` keeps the documented members for
comparison and autocompletion, and maps any other value of the right type to
an ``UNKNOWN_<value>`` pseudo-member instead of raising.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

__all__ = ["OpenEnum"]


class OpenEnum(Enum):
    """An ``Enum`` whose unknown values become pseudo-members instead of errors.

    Pseudo-members are cached, so ``Status(7) is Status(7)``; their ``value``
    is the raw API value and their ``name`` is ``UNKNOWN_<value>``. They are
    not included when iterating over the enum.
    """

    @classmethod
    def _missing_(cls, value: object) -> Any:
        if not _matches_member_types(cls, value):
            return None
        member_type = getattr(cls, "_member_type_", object)  # mixin type, e.g. int for IntEnum
        try:
            if member_type is object:
                member = object.__new__(cls)
            else:
                member = member_type.__new__(cls, value)
        except (TypeError, ValueError):
            return None
        member._name_ = f"UNKNOWN_{value}"
        member._value_ = value
        try:
            return cls._value2member_map_.setdefault(value, member)
        except TypeError:  # unhashable value: usable, just not cached
            return member

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        # Resolve values through the enum constructor (and so `_missing_`) before
        # pydantic's own enum validation, which rejects values it doesn't know
        # and doesn't call `_missing_` consistently between Python and JSON input.
        def to_member(value: Any) -> Any:
            if value is None or isinstance(value, cls):
                return value
            try:
                return cls(value)
            except (TypeError, ValueError):
                return value  # let pydantic report the type error

        return core_schema.no_info_before_validator_function(to_member, handler(source))


def _matches_member_types(cls: type[Enum], value: object) -> bool:
    # Only open the enum to values shaped like the documented ones: an unknown
    # ESP code is another int, while a string there is still a type error.
    member_types = {type(member.value) for member in cls}
    if isinstance(value, bool):
        return bool in member_types
    return type(value) in member_types or (float in member_types and type(value) is int)
