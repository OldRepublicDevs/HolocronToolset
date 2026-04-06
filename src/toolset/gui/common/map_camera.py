"""Shared 2D map camera state for toolset renderers."""

from __future__ import annotations

from toolset.utils.misc import clamp
from utility.common.geometry import Vector2


class MapCamera:
    """Mutable camera state shared by 2D editor renderers."""

    def __init__(
        self,
        *,
        min_zoom: float = 0.1,
        max_zoom: float = 100.0,
        zoom: float = 1.0,
    ) -> None:
        self._position: Vector2 = Vector2.from_null()
        self._rotation: float = 0.0
        self._min_zoom: float = min_zoom
        self._max_zoom: float = max_zoom
        self._zoom: float = clamp(zoom, self._min_zoom, self._max_zoom)

    def position(self) -> Vector2:
        return self._position.copy()

    def rotation(self) -> float:
        return self._rotation

    def zoom(self) -> float:
        return self._zoom

    def min_zoom(self) -> float:
        return self._min_zoom

    def max_zoom(self) -> float:
        return self._max_zoom

    def set_position(self, x: float, y: float) -> None:
        self._position.x = x
        self._position.y = y

    def nudge_position(self, x: float, y: float) -> None:
        self._position.x += x
        self._position.y += y

    def set_rotation(self, rotation: float) -> None:
        self._rotation = rotation

    def nudge_rotation(self, rotation: float) -> None:
        self._rotation += rotation

    def set_zoom(self, zoom: float) -> None:
        self._zoom = clamp(zoom, self._min_zoom, self._max_zoom)

    def nudge_zoom(self, zoom_factor: float) -> None:
        self.set_zoom(self._zoom * zoom_factor)

    def zoom_to_point(self, zoom_factor: float, world_x: float, world_y: float) -> None:
        """Zoom while keeping the specified world point stationary on screen."""
        old_zoom = self._zoom
        old_pos = self._position.copy()
        self.set_zoom(old_zoom * zoom_factor)
        new_zoom = self._zoom
        if old_zoom <= 0 or new_zoom <= 0 or abs(new_zoom - old_zoom) < 1e-9:
            return
        zoom_ratio = old_zoom / new_zoom
        self._position.x = world_x - (world_x - old_pos.x) * zoom_ratio
        self._position.y = world_y - (world_y - old_pos.y) * zoom_ratio
