"""Shared OpenGL widget infrastructure for toolset renderers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QOpenGLWidget  # pyright: ignore[reportPrivateImportUsage]

from loggerplus import RobustLogger
from utility.common.geometry import Vector2

if TYPE_CHECKING:
    from qtpy.QtGui import (
        QCloseEvent,
        QFocusEvent,
    )
    from qtpy.QtWidgets import QWidget

    from pykotor.gl.scene import Scene


class OpenGLSceneRenderer(QOpenGLWidget):
    """Shared OpenGL widget lifecycle helpers for scene-backed renderers."""

    def __init__(
        self,
        parent: QWidget,
        *,
        initial_mouse_prev: Vector2 | None = None,
        loop_interval_ms: int = 33,
    ) -> None:
        super().__init__(parent)
        self._scene: Scene | None = None
        self._keys_down: set[Any] = set()
        self._mouse_down: set[Any] = set()
        self._mouse_prev: Vector2 = initial_mouse_prev if initial_mouse_prev is not None else Vector2(0, 0)

        self._loop_timer: QTimer = QTimer(self)
        self._loop_timer.setInterval(loop_interval_ms)
        self._loop_timer.setSingleShot(False)
        self._loop_timer.timeout.connect(self._on_loop_timer_timeout)

    @property
    def loop_timer(self) -> QTimer:
        return self._loop_timer

    def _on_loop_timer_timeout(self) -> None:
        raise NotImplementedError

    def _drawable_size(self) -> tuple[int, int]:
        try:
            device_pixel_ratio = float(self.devicePixelRatioF())
        except AttributeError:
            device_pixel_ratio = float(self.devicePixelRatio())

        drawable_width: int = max(1, int(round(self.width() * device_pixel_ratio)))
        drawable_height: int = max(1, int(round(self.height() * device_pixel_ratio)))
        return drawable_width, drawable_height

    def _sync_camera_drawable_size(self) -> tuple[int, int]:
        drawable_width, drawable_height = self._drawable_size()
        if self._scene is not None:
            self._scene.camera.set_resolution(drawable_width, drawable_height)
        return drawable_width, drawable_height

    def _logical_to_drawable_coords(self, x: float, y: float) -> tuple[float, float]:
        drawable_width, drawable_height = self._drawable_size()
        logical_width = max(1, self.width())
        logical_height = max(1, self.height())
        return (
            x * drawable_width / logical_width,
            y * drawable_height / logical_height,
        )

    def focusOutEvent(self, event: QFocusEvent):  # pyright: ignore[reportIncompatibleMethodOverride]
        self._mouse_down.clear()
        self._keys_down.clear()
        super().focusOutEvent(event)
        RobustLogger().debug("%s.focusOutEvent: clearing all keys/buttons held down.", self.__class__.__name__)

    def closeEvent(self, event: QCloseEvent):  # pyright: ignore[reportIncompatibleMethodOverride]
        self.shutdown_renderer()
        super().closeEvent(event)

    def shutdown_renderer(self) -> None:
        if self._loop_timer.isActive():
            self._loop_timer.stop()
        self._scene = None
