"""3D tile / area preview for Indoor Map Builder (PyQt + PyKotor GL).

Uses `OpenGLSceneRenderer` (`QOpenGLWidget`) and mirrors Kotor.NET AreaDesigner mesh draws
(`AreaEntity.GetMeshDescriptors` / `AreaExporter`): floors, walls, doorframes, corners, room objects.

When ``INDOOR_BUILDER_DISABLE_3D`` is set, or PyOpenGL is unavailable, the UI keeps the fallback
label from ``indoor_builder.ui``.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

from qtpy.QtCore import Qt, QTimer
from qtpy.QtGui import QCloseEvent, QMouseEvent, QOpenGLContext, QWheelEvent
from qtpy.QtWidgets import QLabel, QVBoxLayout, QWidget

from loggerplus import RobustLogger
from pykotor.common.indoormap import IndoorMap
from pykotor.common.tilekit import TileKit
from pykotor.gl.scene.scene import Scene
from pykotor.tools.tilekit_preview import (
    populate_scene_from_area_designer_v01,
    populate_scene_tile_grid_floor_preview,
    upload_tile_kit_assets,
)
from pykotor.tools.tilemap_compile import TileLayout
from toolset.gui.widgets.renderer.base import OpenGLSceneRenderer
from toolset.gui.widgets.settings.widgets.module_designer import get_renderer_loop_interval_ms
from utility.common.geometry import Vector2

if TYPE_CHECKING:
    from toolset.data.installation import HTInstallation


def _mouse_xy(event: QMouseEvent) -> tuple[float, float]:
    if hasattr(event, "position"):
        p = event.position()
        return (float(p.x()), float(p.y()))
    return (float(event.x()), float(event.y()))


def indoor_builder_3d_enabled() -> bool:
    return os.environ.get("INDOOR_BUILDER_DISABLE_3D", "").strip().lower() not in (
        "1",
        "true",
        "yes",
    )


class IndoorTileGridRenderer(OpenGLSceneRenderer):
    """OpenGL preview: Kotor.NET Area Designer JSON and/or PyKotor ``tile_layout``."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent, loop_interval_ms=get_renderer_loop_interval_ms())
        self._installation: HTInstallation | None = None
        self._last_map_id: int | None = None
        self._kits_signature: tuple[str, ...] = ()
        self._uploaded_for_kits: set[str] = set()
        self._map_ref: IndoorMap | None = None
        self._tile_kits_ref: list[TileKit] = []
        # Layer toggles (parity with .NET view options / export categories).
        self._show_walls: bool = True
        self._show_doors: bool = True
        self._show_corners: bool = True
        self._show_ceilings: bool = False
        self._show_objects: bool = True
        self._respect_adjacency_visibility: bool = True
        self._orbit_drag: bool = False
        self._orbit_last: Vector2 = Vector2(0.0, 0.0)

        self.loop_timer.timeout.disconnect()
        self.loop_timer.timeout.connect(self._on_loop_timer_timeout)

    def _on_loop_timer_timeout(self) -> None:
        if self.isVisible():
            self.update()

    def set_installation(self, installation: HTInstallation | None) -> None:
        self._installation = installation
        self._uploaded_for_kits.clear()
        if self.scene is not None and installation is not None:
            try:
                self.scene.set_installation(installation)
            except (OSError, ValueError, TypeError, RuntimeError):
                RobustLogger().exception("IndoorTileGridRenderer.set_installation failed.")

    def set_preview_layers(
        self,
        *,
        show_walls: bool | None = None,
        show_doors: bool | None = None,
        show_corners: bool | None = None,
        show_ceilings: bool | None = None,
        show_objects: bool | None = None,
    ) -> None:
        if show_walls is not None:
            self._show_walls = show_walls
        if show_doors is not None:
            self._show_doors = show_doors
        if show_corners is not None:
            self._show_corners = show_corners
        if show_ceilings is not None:
            self._show_ceilings = show_ceilings
        if show_objects is not None:
            self._show_objects = show_objects
        self.update()

    def set_respect_adjacency_visibility(self, enabled: bool) -> None:
        """Match Kotor.NET ``Room.FixWalls`` / ``Wall.Visible`` when True; show all kit hooks when False."""
        self._respect_adjacency_visibility = enabled
        self.update()

    def shutdown_renderer(self) -> None:
        super().shutdown_renderer()
        self._uploaded_for_kits.clear()

    def closeEvent(self, event: QCloseEvent) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        self.shutdown_renderer()
        super().closeEvent(event)

    def initializeGL(self) -> None:
        self.makeCurrent()
        try:
            from pykotor.gl.compat import HAS_PYOPENGL  # noqa: PLC0415
        except ImportError:
            HAS_PYOPENGL = False  # noqa: N806
        if not HAS_PYOPENGL:
            RobustLogger().warning("IndoorTileGridRenderer: PyOpenGL missing; 3D preview disabled.")
            return

        self.scene = Scene(installation=self._installation)
        self.scene.enable_frustum_culling = False
        self.scene.camera.distance = 25.0
        self.scene.camera.x = 0.0
        self.scene.camera.y = 0.0
        self.scene.camera.z = 12.0
        self.scene.show_focus_point_gizmo = False
        self.scene.show_cursor = False
        self._sync_camera_drawable_size()
        self.loop_timer.start()

    def resizeGL(self, width: int, height: int) -> None:  # noqa: ARG002
        self._sync_camera_drawable_size()

    def refresh_from_map(self, indoor_map: IndoorMap, tile_kits: list[TileKit]) -> None:
        """Rebuild GPU scene from map state (call after map / kits change)."""
        self._map_ref = indoor_map
        self._tile_kits_ref = tile_kits
        self.update()

    def paintGL(self) -> None:
        if self.scene is None:
            return
        ctx: QOpenGLContext | None = self.context()
        if ctx is None or not ctx.isValid():
            return
        self.makeCurrent()
        self._sync_camera_drawable_size()

        indoor_map = self._map_ref
        tile_kits = self._tile_kits_ref
        if indoor_map is None:
            try:
                self.scene.render()
            except Exception:  # noqa: BLE001
                RobustLogger().exception("IndoorTileGridRenderer.render failed.")
            return

        kits_by_id: dict[str, TileKit] = {tk.kit_id: tk for tk in tile_kits}
        sig = tuple(sorted(kits_by_id.keys()))
        mid = id(indoor_map)
        if sig != self._kits_signature or mid != self._last_map_id:
            self._uploaded_for_kits.clear()
            self._kits_signature = sig
            self._last_map_id = mid

        for kid, tk in kits_by_id.items():
            if kid not in self._uploaded_for_kits:
                upload_tile_kit_assets(self.scene, tk)
                self._uploaded_for_kits.add(kid)

        area_payload = getattr(indoor_map, "area_designer_v01", None)
        if isinstance(area_payload, dict) and area_payload.get("format") == "0.1":
            populate_scene_from_area_designer_v01(
                self.scene,
                area_payload,
                kits_by_id,
                show_walls=self._show_walls,
                show_doors=self._show_doors,
                show_corners=self._show_corners,
                show_ceilings=self._show_ceilings,
                show_objects=self._show_objects,
                respect_adjacency_visibility=self._respect_adjacency_visibility,
            )
        else:
            tl = getattr(indoor_map, "tile_layout", None)
            if isinstance(tl, dict) and tl.get("kit_id"):
                kit_id = str(tl["kit_id"])
                tk = kits_by_id.get(kit_id)
                if tk is not None:
                    layout = TileLayout(
                        format_version=int(tl.get("format_version", 1)),
                        kit_id=kit_id,
                        cell_size=float(tl.get("cell_size", 4.0)),
                        grid_w=int(tl.get("grid_w", 0)),
                        grid_h=int(tl.get("grid_h", 0)),
                        floor_cells=list(tl.get("floor_cells") or []),
                    )
                    populate_scene_tile_grid_floor_preview(self.scene, tk, layout)
                else:
                    self.scene.objects.clear()
                    self.scene.invalidate_render_cache()
            else:
                self.scene.objects.clear()
                self.scene.invalidate_render_cache()

        try:
            self.scene.render()
        except Exception:  # noqa: BLE001
            RobustLogger().exception("IndoorTileGridRenderer.render failed.")

    def wheelEvent(self, event: QWheelEvent) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        if self.scene is None:
            return
        delta = float(event.angleDelta().y())
        self.zoom_camera(delta * 0.0025)
        event.accept()
        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        if event.button() == Qt.MouseButton.MiddleButton:
            self._orbit_drag = True
            mx, my = _mouse_xy(event)
            self._orbit_last = Vector2(mx, my)
            self.setFocus(Qt.FocusReason.MouseFocusReason)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        if event.button() == Qt.MouseButton.MiddleButton:
            self._orbit_drag = False
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        if self._orbit_drag and self.scene is not None:
            mx, my = _mouse_xy(event)
            pos = Vector2(mx, my)
            dx = pos.x - self._orbit_last.x
            dy = pos.y - self._orbit_last.y
            self._orbit_last = pos
            self.rotate_camera(dx * 0.012, -dy * 0.012)
            self.update()
        super().mouseMoveEvent(event)


def setup_indoor_builder_tile_3d(
    *,
    main_splitter: Any,
    host: QWidget,
    host_layout: QVBoxLayout,
    fallback_label: QLabel,
    installation: HTInstallation | None = None,
) -> IndoorTileGridRenderer | None:
    """Replace the fallback label with the GL renderer when 3D is allowed."""
    if not indoor_builder_3d_enabled():
        fallback_label.setText("3D tile view disabled (INDOOR_BUILDER_DISABLE_3D).")
        try:
            main_splitter.setSizes([480, 0])
        except Exception:
            pass
        return None

    try:
        from pykotor.gl.compat import HAS_PYOPENGL  # noqa: PLC0415
    except ImportError:
        HAS_PYOPENGL = False  # noqa: N806

    if not HAS_PYOPENGL:
        fallback_label.setText(
            "3D view: PyOpenGL not available. Use 2D map or install PyOpenGL.",
        )
        try:
            main_splitter.setSizes([480, 0])
        except Exception:
            pass
        return None

    host_layout.removeWidget(fallback_label)
    fallback_label.hide()
    gl_widget = IndoorTileGridRenderer(host)
    gl_widget.set_installation(installation)
    host_layout.addWidget(gl_widget)
    try:
        main_splitter.setSizes([400, 200])
    except Exception:
        pass
    QTimer.singleShot(0, gl_widget.update)
    return gl_widget
