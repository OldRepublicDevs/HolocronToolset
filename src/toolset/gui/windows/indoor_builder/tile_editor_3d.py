"""Optional 3D tile-grid preview for Indoor Map Builder (PyQt + OpenGL).

When ``INDOOR_BUILDER_DISABLE_3D`` is set, or PyOpenGL is unavailable, the UI keeps the
fallback label from ``indoor_builder.ui``.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QLabel, QVBoxLayout, QWidget

if TYPE_CHECKING:
    from qtpy.QtWidgets import QSplitter


def indoor_builder_3d_enabled() -> bool:
    return os.environ.get("INDOOR_BUILDER_DISABLE_3D", "").strip().lower() not in (
        "1",
        "true",
        "yes",
    )


class _MinimalTileGridGL(QWidget):
    """Clears a color buffer; placeholder for a full tile-mesh + grid renderer."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        from qtpy.QtWidgets import QOpenGLWidget  # noqa: PLC0415

        self._gl: object | None = None
        try:
            from OpenGL.GL import (  # noqa: PLC0415
                GL_COLOR_BUFFER_BIT,
                GL_DEPTH_BUFFER_BIT,
                glClear,
                glClearColor,
            )

            class _V(QOpenGLWidget):
                def initializeGL(self) -> None:
                    glClearColor(0.12, 0.12, 0.14, 1.0)

                def paintGL(self) -> None:
                    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self._gl = _V(self)
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self._gl)
        except Exception:
            lab = QLabel(self)
            lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lab.setText(
                "3D view: PyOpenGL not available. Use 2D map or install PyOpenGL.",
            )
            layout = QVBoxLayout(self)
            layout.addWidget(lab)


def setup_indoor_builder_tile_3d(
    *,
    main_splitter: QSplitter,
    host: QWidget,
    host_layout: QVBoxLayout,
    fallback_label: QLabel,
) -> None:
    """Replace the fallback label with a minimal GL widget when 3D is allowed."""
    if not indoor_builder_3d_enabled():
        fallback_label.setText("3D tile view disabled (INDOOR_BUILDER_DISABLE_3D).")
        try:
            main_splitter.setSizes([480, 0])
        except Exception:
            pass
        return
    host_layout.removeWidget(fallback_label)
    fallback_label.hide()
    host_layout.addWidget(_MinimalTileGridGL(host))
    try:
        main_splitter.setSizes([400, 200])
    except Exception:
        pass
