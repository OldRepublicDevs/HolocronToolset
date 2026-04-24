from __future__ import annotations

from typing import TYPE_CHECKING, Union

from pykotor.resource.type import ResourceType

try:
    from pykotor.resource.type import ToolsetFormat
except ImportError:
    # Older PyKotor releases exposed toolset serialization variants on ResourceType.
    if not TYPE_CHECKING:
        ToolsetFormat = ResourceType  # type: ignore[misc,assignment]

try:
    from pykotor.resource.type import RESOURCE_FORMAT
except ImportError:
    RESOURCE_FORMAT = Union[ResourceType, ToolsetFormat]

try:
    from pykotor.resource.type import get_toolset_formats_for_type
except ImportError:
    def get_toolset_formats_for_type(restype: ResourceType) -> tuple[ToolsetFormat, ...]:
        _ = restype
        return ()

__all__ = [
    "RESOURCE_FORMAT",
    "ResourceType",
    "ToolsetFormat",
    "get_toolset_formats_for_type",
]