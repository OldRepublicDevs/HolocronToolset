"""Shared resource navigation controls for editor windows."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Sequence

from qtpy.QtCore import Signal  # pyright: ignore[reportPrivateImportUsage]
from qtpy.QtWidgets import QComboBox, QHBoxLayout, QLabel, QSizePolicy, QWidget

from pykotor.extract.file import FileResource
from toolset.utils.resource_type_compat import ResourceType

if TYPE_CHECKING:
    from toolset.data.installation import HTInstallation


_CAPSULE_TYPES: frozenset[ResourceType] = frozenset(
    {
        ResourceType.BIF,
        ResourceType.ERF,
        ResourceType.MOD,
        ResourceType.RIM,
        ResourceType.SAV,
    }
)


@dataclass(frozen=True)
class ResourceContainerSpec:
    key: str
    label: str
    kind: str
    value: str | None = None


class ResourceNavigationWidget(QWidget):
    """Container and resource selector row shared by editor windows."""

    resource_selected = Signal(object)  # FileResource | None

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._installation: HTInstallation | None = None
        self._resource_types: list[ResourceType] = []
        self._container_specs: list[ResourceContainerSpec] = []
        self._container_populating: bool = False
        self._resource_populating: bool = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.containerLabel = QLabel("  Container Location:  ", self)
        layout.addWidget(self.containerLabel)

        self.containerCombo = QComboBox(self)
        self.containerCombo.setMinimumWidth(260)
        self.containerCombo.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )
        layout.addWidget(self.containerCombo, 1)

        self.resourceLabel = QLabel("  Navigate:  ", self)
        layout.addWidget(self.resourceLabel)

        self.resourceCombo = QComboBox(self)
        self.resourceCombo.setMinimumWidth(320)
        self.resourceCombo.setMaxVisibleItems(30)
        self.resourceCombo.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )
        layout.addWidget(self.resourceCombo, 2)

        self.containerCombo.currentIndexChanged.connect(self._on_container_selection_changed)
        self.resourceCombo.currentIndexChanged.connect(self._on_resource_selection_changed)
        self._update_enabled_state()

    def set_navigation_context(
        self,
        installation: HTInstallation | None,
        resource_types: Sequence[ResourceType],
    ) -> None:
        self._installation = installation
        self._resource_types = list(dict.fromkeys(resource_types))
        preserve_key = self.containerCombo.currentData()
        self._refresh_containers(preserve_key)

    def sync_to_resource(
        self,
        filepath: str | Path,
        resname: str,
        restype: ResourceType,
    ) -> None:
        target_path = Path(filepath)
        target_name = resname.lower()
        self._resource_populating = True
        try:
            for index in range(self.resourceCombo.count()):
                resource: FileResource | None = self.resourceCombo.itemData(index)
                if resource is None:
                    continue
                if resource.resname().lower() != target_name:
                    continue
                if resource.restype() != restype:
                    continue
                if Path(resource.filepath()) != target_path:
                    continue
                self.resourceCombo.setCurrentIndex(index)
                return
            for index in range(self.resourceCombo.count()):
                resource = self.resourceCombo.itemData(index)
                if resource is None:
                    continue
                if resource.resname().lower() == target_name and resource.restype() == restype:
                    self.resourceCombo.setCurrentIndex(index)
                    return
            self.resourceCombo.setCurrentIndex(-1)
        finally:
            self._resource_populating = False

    def _update_enabled_state(self) -> None:
        has_installation = self._installation is not None and bool(self._resource_types)
        self.containerLabel.setEnabled(has_installation)
        self.resourceLabel.setEnabled(has_installation)
        self.containerCombo.setEnabled(has_installation and self.containerCombo.count() > 0)
        self.resourceCombo.setEnabled(has_installation and self.resourceCombo.count() > 0)

    def _refresh_containers(self, preserve_key: str | None = None) -> None:
        self._container_specs = self._build_container_specs()
        self._container_populating = True
        try:
            self.containerCombo.clear()
            for spec in self._container_specs:
                self.containerCombo.addItem(spec.label, spec.key)
            if preserve_key is not None:
                preserve_index = self.containerCombo.findData(preserve_key)
                if preserve_index >= 0:
                    self.containerCombo.setCurrentIndex(preserve_index)
                elif self.containerCombo.count() > 0:
                    self.containerCombo.setCurrentIndex(0)
                else:
                    self.containerCombo.setCurrentIndex(-1)
            elif self.containerCombo.count() > 0:
                self.containerCombo.setCurrentIndex(0)
            else:
                self.containerCombo.setCurrentIndex(-1)
        finally:
            self._container_populating = False
        self._refresh_resources()

    def _refresh_resources(self) -> None:
        spec = self._current_container_spec()
        resources = self._load_resources(spec)
        self._resource_populating = True
        try:
            self.resourceCombo.clear()
            if spec is None:
                self.resourceCombo.setCurrentIndex(-1)
                return
            filtered = self._filter_supported_resources(resources)
            labels = [self._base_resource_label(resource) for resource in filtered]
            duplicate_counts = Counter(labels)
            for resource in filtered:
                label = self._base_resource_label(resource)
                if duplicate_counts[label] > 1:
                    label = f"{label} - {self._describe_resource_path(resource)}"
                self.resourceCombo.addItem(label, resource)
            self.resourceCombo.setCurrentIndex(-1)
        finally:
            self._resource_populating = False
            self._update_enabled_state()

    def _current_container_spec(self) -> ResourceContainerSpec | None:
        container_key = self.containerCombo.currentData()
        if container_key is None:
            return None
        for spec in self._container_specs:
            if spec.key == container_key:
                return spec
        return None

    def _build_container_specs(self) -> list[ResourceContainerSpec]:
        installation = self._installation
        if installation is None or not self._resource_types:
            return []

        specs: list[ResourceContainerSpec] = [
            ResourceContainerSpec("default", "Default (data + override)", "default"),
            ResourceContainerSpec("core", "data (KEY/BIF + patch)", "core"),
            ResourceContainerSpec("override_all", "Override (all)", "override_all"),
        ]

        for directory in sorted(installation.override_list(), key=str.lower):
            label = "Override: root" if directory in {"", "."} else f"Override: {directory}"
            specs.append(
                ResourceContainerSpec(
                    f"override:{directory or '.'}",
                    label,
                    "override_dir",
                    None if directory in {"", "."} else directory,
                )
            )

        modules = sorted(installation.modules_list(), key=str.lower)
        if modules:
            specs.append(ResourceContainerSpec("modules_all", "Modules (all)", "modules_all"))
            for module_name in modules:
                specs.append(
                    ResourceContainerSpec(
                        f"module:{module_name}",
                        f"Module: {module_name}",
                        "module",
                        module_name,
                    )
                )

        texturepacks = sorted(installation.texturepacks_list(), key=str.lower)
        if texturepacks:
            specs.append(
                ResourceContainerSpec("texturepacks_all", "TexturePacks (all)", "texturepacks_all")
            )
            for texturepack_name in texturepacks:
                specs.append(
                    ResourceContainerSpec(
                        f"texturepack:{texturepack_name}",
                        f"TexturePack: {texturepack_name}",
                        "texturepack",
                        texturepack_name,
                    )
                )

        lips = sorted(installation.lips_list(), key=str.lower)
        if lips:
            specs.append(ResourceContainerSpec("lips_all", "Lips (all)", "lips_all"))
            for lip_name in lips:
                specs.append(
                    ResourceContainerSpec(
                        f"lip:{lip_name}",
                        f"Lips: {lip_name}",
                        "lip",
                        lip_name,
                    )
                )

        specs.extend(
            [
                ResourceContainerSpec("streammusic", "StreamMusic", "streammusic"),
                ResourceContainerSpec("streamsounds", "StreamSounds", "streamsounds"),
                ResourceContainerSpec("streamvoice", "StreamVoice / StreamWaves", "streamvoice"),
            ]
        )
        return specs

    def _load_resources(self, spec: ResourceContainerSpec | None) -> list[FileResource]:
        installation = self._installation
        if installation is None or spec is None:
            return []

        resources: list[FileResource] = []
        if spec.kind == "default":
            resources.extend(self._core_entry_resources(installation))
            resources.extend(installation.override_resources())
        elif spec.kind == "core":
            resources.extend(self._core_entry_resources(installation))
        elif spec.kind == "override_all":
            resources.extend(installation.override_resources())
        elif spec.kind == "override_dir":
            resources.extend(installation.override_resources(spec.value))
        elif spec.kind == "modules_all":
            resources.extend(self._module_entry_resources(installation, installation.modules_list()))
        elif spec.kind == "module" and spec.value is not None:
            resources.extend(self._module_entry_resources(installation, [spec.value]))
        elif spec.kind == "texturepacks_all":
            resources.extend(
                self._texturepack_entry_resources(installation, installation.texturepacks_list())
            )
        elif spec.kind == "texturepack" and spec.value is not None:
            resources.extend(self._texturepack_entry_resources(installation, [spec.value]))
        elif spec.kind == "lips_all":
            resources.extend(self._lip_entry_resources(installation, installation.lips_list()))
        elif spec.kind == "lip" and spec.value is not None:
            resources.extend(self._lip_entry_resources(installation, [spec.value]))
        elif spec.kind == "streammusic":
            resources.extend(installation._streammusic)  # noqa: SLF001
        elif spec.kind == "streamsounds":
            resources.extend(installation._streamsounds)  # noqa: SLF001
        elif spec.kind == "streamvoice":
            resources.extend(installation._streamwaves)  # noqa: SLF001
        return resources

    def _core_entry_resources(self, installation: HTInstallation) -> list[FileResource]:
        resources = installation.core_resources()
        resources.extend(
            self._container_file_resources(resource.filepath() for resource in resources)
        )
        return resources

    def _module_entry_resources(
        self,
        installation: HTInstallation,
        module_names: Sequence[str],
    ) -> list[FileResource]:
        resources: list[FileResource] = []
        module_paths = [installation.module_path() / module_name for module_name in module_names]
        resources.extend(self._container_file_resources(module_paths))
        for module_name in module_names:
            resources.extend(installation.module_resources(module_name))
        return resources

    def _texturepack_entry_resources(
        self,
        installation: HTInstallation,
        texturepack_names: Sequence[str],
    ) -> list[FileResource]:
        resources: list[FileResource] = []
        texturepack_paths = [
            installation.texturepacks_path() / texturepack_name
            for texturepack_name in texturepack_names
        ]
        resources.extend(self._container_file_resources(texturepack_paths))
        for texturepack_name in texturepack_names:
            resources.extend(installation.texturepack_resources(texturepack_name))
        return resources

    def _lip_entry_resources(
        self,
        installation: HTInstallation,
        lip_names: Sequence[str],
    ) -> list[FileResource]:
        resources: list[FileResource] = []
        lip_paths = [installation.lips_path() / lip_name for lip_name in lip_names]
        resources.extend(self._container_file_resources(lip_paths))
        for lip_name in lip_names:
            resources.extend(installation.lip_resources(lip_name))
        return resources

    def _container_file_resources(self, paths: Iterable[Path]) -> list[FileResource]:
        resources: list[FileResource] = []
        seen_paths: set[str] = set()
        for path in paths:
            path_key = str(path).lower()
            if path_key in seen_paths or not path.is_file():
                continue
            seen_paths.add(path_key)
            try:
                resources.append(FileResource.from_path(path))
            except Exception:
                continue
        return resources

    def _filter_supported_resources(self, resources: Sequence[FileResource]) -> list[FileResource]:
        allowed = set(self._resource_types)
        filtered = [resource for resource in resources if resource.restype() in allowed]
        filtered.sort(
            key=lambda resource: (
                resource.resname().lower(),
                resource.restype().extension.lower(),
                str(resource.filepath()).lower(),
                resource.offset(),
            )
        )
        return filtered

    def _base_resource_label(self, resource: FileResource) -> str:
        return f"{resource.resname()}.{resource.restype().extension}"

    def _describe_resource_path(self, resource: FileResource) -> str:
        path = resource.filepath()
        installation = self._installation
        if installation is not None:
            try:
                path = path.relative_to(installation.path())
            except ValueError:
                pass
        return path.as_posix()

    def _on_container_selection_changed(self, _index: int) -> None:
        if self._container_populating:
            return
        self._refresh_resources()

    def _on_resource_selection_changed(self, index: int) -> None:
        if self._resource_populating or index < 0:
            return
        resource: FileResource | None = self.resourceCombo.itemData(index)
        self.resource_selected.emit(resource)