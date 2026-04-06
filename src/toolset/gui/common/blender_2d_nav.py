from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Any

from qtpy.QtCore import Qt

from toolset.gui.common.interaction.camera import calculate_zoom_strength

if TYPE_CHECKING:
    from utility.common.geometry import Vector2


AABB2D = tuple[float, float, float, float]


def aabb_from_points(points: Iterable[tuple[float, float]]) -> AABB2D | None:
    point_list = list(points)
    if not point_list:
        return None
    xs = [point[0] for point in point_list]
    ys = [point[1] for point in point_list]
    return min(xs), min(ys), max(xs), max(ys)


def zoom_to_fit_aabb(renderer: Any, aabb: AABB2D, *, padding: float = 0.15) -> None:
    min_x, min_y, max_x, max_y = aabb
    center_x = (min_x + max_x) / 2.0
    center_y = (min_y + max_y) / 2.0
    world_width = max(max_x - min_x, 1.0) * (1.0 + padding * 2.0)
    world_height = max(max_y - min_y, 1.0) * (1.0 + padding * 2.0)
    screen_width = renderer.width() or 520
    screen_height = renderer.height() or 507
    zoom = min(screen_width / world_width, screen_height / world_height)
    renderer.camera.set_position(center_x, center_y)
    renderer.camera.set_zoom(zoom)
    renderer.mark_dirty()


class Blender2DNavigationHelper:
    def __init__(
        self,
        renderer: Any,
        *,
        get_content_bounds: Callable[[], AABB2D | None],
        get_selection_bounds: Callable[[], AABB2D | None] | None = None,
        settings: object | None = None,
    ) -> None:
        self.renderer = renderer
        self._get_content_bounds = get_content_bounds
        self._get_selection_bounds = get_selection_bounds
        self._settings = settings

    def _is_blender_scheme(self) -> bool:
        return getattr(self._settings, "controlScheme", "blender") != "classic"

    def frame_all(self) -> bool:
        bounds = self._get_content_bounds()
        if bounds is None:
            return False
        zoom_to_fit_aabb(self.renderer, bounds)
        return True

    def frame_selected(self) -> bool:
        if self._get_selection_bounds is None:
            return self.frame_all()
        bounds = self._get_selection_bounds()
        if bounds is None:
            return self.frame_all()
        zoom_to_fit_aabb(self.renderer, bounds)
        return True

    def reset_view(self) -> bool:
        return self.frame_all()

    def handle_mouse_scroll(self, delta: Vector2, keys: set[int], *, zoom_sensitivity: int) -> bool:
        if not delta.y:
            return False
        if not self._is_blender_scheme() and Qt.Key.Key_Control not in keys:
            return False
        self.renderer.zoom_at_screen(calculate_zoom_strength(delta.y, zoom_sensitivity))
        return True

    def handle_key_pressed(self, keys: set[int], *, pan_step: float, zoom_in_factor: float = 1.25, zoom_out_factor: float = 0.8) -> bool:
        if Qt.Key.Key_Home in keys:
            return self.frame_all()
        if Qt.Key.Key_Period in keys:
            return self.frame_selected()
        if Qt.Key.Key_0 in keys and Qt.Key.Key_Control in keys:
            return self.reset_view()
        if Qt.Key.Key_Equal in keys or Qt.Key.Key_Plus in keys:
            self.renderer.zoom_at_screen(zoom_in_factor)
            return True
        if Qt.Key.Key_Minus in keys:
            self.renderer.zoom_at_screen(zoom_out_factor)
            return True

        effective_pan_step = pan_step * 0.2 if Qt.Key.Key_Shift in keys else pan_step
        if Qt.Key.Key_Left in keys:
            self.renderer.camera.nudge_position(-effective_pan_step, 0.0)
            self.renderer.mark_dirty()
            return True
        if Qt.Key.Key_Right in keys:
            self.renderer.camera.nudge_position(effective_pan_step, 0.0)
            self.renderer.mark_dirty()
            return True
        if Qt.Key.Key_Up in keys:
            self.renderer.camera.nudge_position(0.0, effective_pan_step)
            self.renderer.mark_dirty()
            return True
        if Qt.Key.Key_Down in keys:
            self.renderer.camera.nudge_position(0.0, -effective_pan_step)
            self.renderer.mark_dirty()
            return True
        return False