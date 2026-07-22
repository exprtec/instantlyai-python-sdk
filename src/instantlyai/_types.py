"""Shared JSON typing helpers for resource methods."""

from __future__ import annotations

from typing import TypeAlias

JSONValue: TypeAlias = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]
JSONObject: TypeAlias = dict[str, JSONValue]

__all__ = ["JSONObject", "JSONValue"]
