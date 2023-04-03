"""Type hints for the passwordgen package."""

__all__ = ["JsonType"]

JsonType = int | float | str | bool | None | list["JsonType"] | dict[str, "JsonType"]
