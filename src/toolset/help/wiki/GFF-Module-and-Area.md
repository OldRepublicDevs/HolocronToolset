# GFF Types: Module and Area

ARE, GIT, and IFO are not separate binary dialects; they are three typed GFF resources that the Odyssey-family runtime consumes at different scopes. PyKotor models them as distinct generic readers, and the recovered GFF access layer in KotOR I, KotOR II, and Aurora follows the same label-driven pattern: resolve a field label, resolve the referenced field record, then decode typed payloads such as `ResRef` and `CExoLocString`. [[`ARE`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L21), [`GIT`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L57), [`IFO`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L16)] `GetFieldByLabel @ (/K1/k1_win_gog_swkotor.exe @ 0x00411630, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00623a40, /Other BioWare Engines/Aurora/nwmain.exe @ 0x14019fcc0)` `GetField @ (/K1/k1_win_gog_swkotor.exe @ 0x00410990, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x006238d0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x14019fc20)` `ReadFieldCResRef @ (/K1/k1_win_gog_swkotor.exe @ 0x00411e10, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00624fa0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a12d0)` `ReadFieldCExoLocString @ (/K1/k1_win_gog_swkotor.exe @ 0x00411fd0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00625240, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a0f80)`

For KotOR specifically, the practical split is narrower and safer to document than older one-file summaries suggest: ARE carries static area metadata, GIT carries per-area placed instances plus root audio integers, and IFO carries module-level entry configuration, area membership, and module script state. That scope split is explicit in the local schemas below; where retail loader visibility differs across binaries, the prose calls that out instead of pretending every label is equally recovered everywhere. [[`are.py` fields](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L31-L123), [`git.py` sections](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L80-L147), [`ifo.py` fields](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L25-L84)]

## Contents

- [ARE — Area](#are)
- [GIT — Game Instance (Dynamic Area Data)](#git)
- [IFO — Module Info](#ifo)

---

<a id="are"></a>

# ARE (Area)

Part of the [GFF File Format Documentation](GFF-File-Format).

ARE is the static-area half of the KotOR area package. PyKotor's schema exposes lighting, fog, grass, weather, map, room, and script-hook fields, and the recovered retail `CSWSArea::LoadAreaHeader` routines in KotOR I and KotOR II visibly read scalar metadata first, then an `Expansion_List`, and then ARE script-hook labels through the shared GFF readers. [[`ARE` field model](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L31-L123), [`construct_are`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L311-L430)] `LoadAreaHeader @ (/K1/k1_win_gog_swkotor.exe @ 0x00508c50, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00718a20)` `GetListCount @ (/K1/k1_win_gog_swkotor.exe @ 0x00411940, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00624970, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a0370)` `ReadFieldCResRef @ (/K1/k1_win_gog_swkotor.exe @ 0x00411e10, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00624fa0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a12d0)` `ReadFieldCExoLocString @ (/K1/k1_win_gog_swkotor.exe @ 0x00411fd0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00625240, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a0f80)`

The field-name visibility is not identical across builds. K1 preserves the labels `OnHeartbeat`, `OnUserDefined`, `OnEnter`, and `OnExit` directly in the recovered area loader; the current TSL recovery exposes `OnHeartbeat` and `OnUserDefined` clearly in the same loader block and then continues through additional `ResRef` reads with less helpful symbol text, so the stable engine-level claim here is that retail area loading consumes ARE hook `ResRef`s through the same typed GFF path rather than that every label survives equally in every disassembly. `LoadAreaHeader @ (/K1/k1_win_gog_swkotor.exe @ 0x00508c50, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00718a20)` `ReadFieldCResRef @ (/K1/k1_win_gog_swkotor.exe @ 0x00411e10, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00624fa0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a12d0)`

That means the safest description is still the obvious one: ARE carries environmental and area-scope metadata, while dynamic placement lives elsewhere. Associated resources often include:

- [GIT](GFF-Module-and-Area#git)
- [LYT](Level-Layout-Formats#lyt)
- [VIS](Level-Layout-Formats#vis)

Those resources use the usual [resource resolution order](Concepts#resource-resolution-order).

For the original Aurora-facing specification, see [Bioware Aurora Area File Format](Bioware-Aurora-Module-and-Area#areafile). For patching ARE data in installers, see [TSLPatcher GFFList Syntax Guide](TSLPatcher-GFF-Syntax#gfflist-syntax); for general installer-side modding context, see [HoloPatcher README for Mod Developers](HoloPatcher#mod-developers).

Related formats:

- [GIT](GFF-File-Format#git-game-instance-template)
- [BWM](Level-Layout-Formats#bwm)
- [LYT](Level-Layout-Formats#lyt)
- [VIS](Level-Layout-Formats#vis)
- [2DA](2DA-File-Format) (e.g. camerastyle, ambientmusic)
- [TLK](Audio-and-Localization-Formats#tlk)

Loading uses the same [resource resolution order](Concepts#resource-resolution-order).

PyKotor models areas through [`ARE`, `construct_are`, `read_are`, and `write_are`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L21), identifies them as [`GFFContent.ARE`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py#L159), and decodes them through the shared [`GFFBinaryReader.load`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/io_gff.py#L82) pipeline; Holocron Toolset exposes the same fields in its [`are.py` area editor](https://github.com/OpenKotOR/HolocronToolset/src/toolset/gui/editors/are.py). Other implementations keep ARE in the generic GFF path too, including reone's [`gff.cpp`](https://github.com/seedhartha/reone/blob/master/src/libs/resource/gff.cpp) and [`gffreader.cpp`](https://github.com/seedhartha/reone/blob/master/src/libs/resource/format/gffreader.cpp), KotOR.js's [`GFFObject.ts`](https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/resource/GFFObject.ts#L24), Kotor.NET's [`GFF.cs`](https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Formats/KotorGFF/GFF.cs#L18), and xoreos's Aurora pipeline.

## Core Identity fields

These root fields are schema-derived from the current local ARE reader. `construct_are` acquires `Version`, `Tag`, `Name`, and `Comments` directly from the ARE root, while `ID`, `Creator_ID`, and `Flags` remain part of the broader optional/deprecated block that the local model preserves but does not treat as the core runtime area state. [[`construct_are` root identity reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L345-L349), [`construct_are` deprecated root reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L379-L396)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Tag` | [CExoString](GFF-File-Format#gff-data-types) | Unique area identifier |
| `Name` | [CExoLocString](GFF-File-Format#gff-data-types) | Area name (localized) |
| `Comments` | [CExoString](GFF-File-Format#gff-data-types) | Developer notes/documentation |
| `Creator_ID` | UInt32 | Toolset creator identifier |
| `ID` | UInt32 | Area ID field |
| `Version` | UInt32 | Area version field |
| `Flags` | UInt32 | Area flags field |

## Lighting & Sun

The local ARE schema stores the main lighting state as RGB integers plus two shadow controls. `construct_are` reads `SunAmbientColor`, `SunDiffuseColor`, and `DynAmbientColor` through `Color.from_rgb_integer`, while `SunShadows` and `ShadowOpacity` are acquired as scalar fields. [[`construct_are` lighting reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L364-L368), [`construct_are` color conversion block](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L401-L405)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `SunAmbientColor` | color | Ambient light color RGB |
| `SunDiffuseColor` | color | Sun diffuse light color RGB |
| `SunShadows` | [byte](GFF-File-Format#gff-data-types) | Enable shadow rendering |
| `ShadowOpacity` | [byte](GFF-File-Format#gff-data-types) | Shadow opacity (0-255) |
| `DynAmbientColor` | color | Dynamic ambient light RGB |

## Fog Settings

Fog is also explicit in the local read path: `SunFogOn` defaults to `0`, `SunFogNear` and `SunFogFar` default to `10000.0` when omitted, and `SunFogColor` is converted from the stored RGB integer payload. [[`construct_are` fog reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L359-L364), [`construct_are` fog color conversion](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L404-L404)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `SunFogOn` | [byte](GFF-File-Format#gff-data-types) | Enable fog rendering |
| `SunFogNear` | float | Fog start distance (default 10000.0) [[`are.py` L380](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L380)] |
| `SunFogFar` | float | Fog end distance (default 10000.0) [[`are.py` L381](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L381)] |
| `SunFogColor` | color | Fog color RGB |

## Moon Lighting and Night Fields

The moon-lighting block remains in the schema and is preserved by the local reader, but it is grouped with the legacy/deprecated-style fields rather than the main ARE state. `MoonFogNear` and `MoonFogFar` use the same `10000.0` default pattern as the sun fog fields when absent. [[`construct_are` moon-field reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L383-L391)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `MoonAmbientColor` | color | Moon ambient light color |
| `MoonDiffuseColor` | color | Moon diffuse light color |
| `MoonFogOn` | [byte](GFF-File-Format#gff-data-types) | Moon fog toggle |
| `MoonFogNear` | float | Moon fog start distance |
| `MoonFogFar` | float | Moon fog end distance |
| `MoonFogColor` | color | Moon fog color |
| `MoonShadows` | [byte](GFF-File-Format#gff-data-types) | Moon-shadow toggle |
| `IsNight` | [byte](GFF-File-Format#gff-data-types) | Night-state flag |

## Grass Rendering

Grass-related fields are read directly from the ARE root: `Grass_TexName` as a `ResRef`, the density/size/probability controls as scalars, and the ambient/diffuse/emissive colors through RGB conversion. The local reader treats `Grass_Emissive` as optional and KotOR II-specific. [[`construct_are` grass scalar reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L350-L358), [`construct_are` grass color reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L405-L408)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Grass_TexName` | *ResRef* | Grass [texture](Texture-Formats#tpc) name |
| `Grass_Density` | float | Grass blade density (0.0-1.0) |
| `Grass_QuadSize` | float | Size of grass patches |
| `Grass_Ambient` | color | Grass ambient color RGB |
| `Grass_Diffuse` | color | Grass diffuse color RGB |
| `Grass_Emissive` (KotOR2) | color | Grass emissive color RGB |
| `Grass_Prob_LL` | float | Spawn probability lower-left |
| `Grass_Prob_LR` | float | Spawn probability lower-right |
| `Grass_Prob_UL` | float | Spawn probability upper-left |
| `Grass_Prob_UR` | float | Spawn probability upper-right |

## Weather System (KotOR2)

The KotOR II weather block is schema-derived from the local reader: `ChanceRain`, `ChanceSnow`, and `ChanceLightning` are acquired as optional integers with `0` defaults when absent. [[`construct_are` weather reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L373-L375)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `ChanceRain` (KotOR2) | [int32](GFF-File-Format#gff-data-types) | Rain probability (0-100) |
| `ChanceSnow` (KotOR2) | [int32](GFF-File-Format#gff-data-types) | Snow probability (0-100) |
| `ChanceLightning` (KotOR2) | [int32](GFF-File-Format#gff-data-types) | Lightning probability (0-100) |

## Dirty/Dust Settings (KotOR2)

The dirty/dust block is likewise schema-derived from the current reader: each of the three layers stores an ARGB color plus size, formula, and function integers, all defaulting to `0` when missing. [[`construct_are` dirty-field reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L376-L382), [`construct_are` dirty-color reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L408-L410)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `DirtyARGBOne` (KotOR2) | UInt32 | First dust color ARGB |
| `DirtySizeOne` (KotOR2) | float | First dust particle size |
| `DirtyFormulaOne` (KotOR2) | [int32](GFF-File-Format#gff-data-types) | First dust formula type |
| `DirtyFuncOne` (KotOR2) | [int32](GFF-File-Format#gff-data-types) | First dust function |
| `DirtyARGBTwo` (KotOR2) | UInt32 | Second dust color ARGB |
| `DirtySizeTwo` (KotOR2) | float | Second dust particle size |
| `DirtyFormulaTwo` (KotOR2) | [int32](GFF-File-Format#gff-data-types) | Second dust formula type |
| `DirtyFuncTwo` (KotOR2) | [int32](GFF-File-Format#gff-data-types) | Second dust function |
| `DirtyARGBThree` (KotOR2) | UInt32 | Third dust color ARGB |
| `DirtySizeThree` (KotOR2) | float | Third dust particle size |
| `DirtyFormulaThre` (KotOR2) | [int32](GFF-File-Format#gff-data-types) | Third dust formula type |
| `DirtyFuncThree` (KotOR2) | [int32](GFF-File-Format#gff-data-types) | Third dust function |

## Environment & Camera

The environment block mixes two different field families in the local schema: `DefaultEnvMap`, `CameraStyle`, `AlphaTest`, and `WindPower` are part of the primary read path, while `LightingScheme` remains in the legacy/deprecated-style group. `AlphaTest` defaults to `0.2` and `WindPower` is normalized into the local `AREWindPower` enum. [[`construct_are` environment reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L349-L350), [`construct_are` alpha/wind reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L364-L367), [`construct_are` lighting scheme read](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L391-L392)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `DefaultEnvMap` | *ResRef* | Default environment map [texture](Texture-Formats#tpc) |
| `CameraStyle` | [int32](GFF-File-Format#gff-data-types) | Camera behavior type |
| `AlphaTest` | float | Alpha testing threshold (default 0.2) [[`are.py` L368](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L368), [reone `are.cpp` L302](https://github.com/seedhartha/reone/blob/master/src/libs/resource/parser/gff/are.cpp#L302)] |
| `WindPower` | [int32](GFF-File-Format#gff-data-types) | Wind strength for effects (`AREWindPower`: Still=0, Weak=1, Strong=2) [[`are.py` L298](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L298), [reone `are.cpp` L383](https://github.com/seedhartha/reone/blob/master/src/libs/resource/parser/gff/are.cpp#L383)] |
| `LightingScheme` | [int32](GFF-File-Format#gff-data-types) | Lighting-scheme identifier |

## Area behavior flags

The area-behavior block is mostly scalar flag state in the local schema. `construct_are` reads `Unescapable`, `DisableTransit`, `StealthXPEnabled`, `StealthXPLoss`, and `StealthXPMax` as part of the main path, while `DayNightCycle`, `LoadScreenID`, `NoRest`, `NoHangBack`, `PlayerOnly`, and `PlayerVsPlayer` live in the broader preserved field set. [[`construct_are` flag reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L367-L372), [`construct_are` preserved area flags](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L391-L396)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Unescapable` | [byte](GFF-File-Format#gff-data-types) | Cannot use save/travel functions |
| `DisableTransit` | [byte](GFF-File-Format#gff-data-types) | Cannot travel to other modules |
| `StealthXPEnabled` | [byte](GFF-File-Format#gff-data-types) | Award stealth XP |
| `StealthXPLoss` | [int32](GFF-File-Format#gff-data-types) | Stealth detection XP penalty |
| `StealthXPMax` | [int32](GFF-File-Format#gff-data-types) | Maximum stealth XP per area |
| `DayNightCycle` | [byte](GFF-File-Format#gff-data-types) | Day/night-cycle toggle [[`are.py` L421](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L421), [reone `are.cpp` L309](https://github.com/seedhartha/reone/blob/master/src/libs/resource/parser/gff/are.cpp#L309)] |
| `LoadScreenID` | UInt16 | Loading screen to display [[`are.py` L422](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L422), [reone `are.cpp` L339](https://github.com/seedhartha/reone/blob/master/src/libs/resource/parser/gff/are.cpp#L339)] |
| `NoRest` | [byte](GFF-File-Format#gff-data-types) | No-rest area flag [[`are.py` L423](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L423), [reone `are.cpp` L359](https://github.com/seedhartha/reone/blob/master/src/libs/resource/parser/gff/are.cpp#L359)] |
| `NoHangBack` | [byte](GFF-File-Format#gff-data-types) | Hang-back behavior flag [[`are.py` L424](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L424)] |
| `PlayerOnly` | [byte](GFF-File-Format#gff-data-types) | Player-only area flag [[`are.py` L425](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L425)] |
| `PlayerVsPlayer` | [byte](GFF-File-Format#gff-data-types) | Player-versus-player flag [[`are.py` L426](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L426)] |

## Skill Check Modifiers

`ModSpotCheck` and `ModListenCheck` are preserved by the local reader as optional integer fields with `0` defaults, but they are part of the same deprecated-style group as the other legacy Aurora carryovers rather than the minimal KotOR area state. [[`construct_are` skill-modifier reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L383-L384)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `ModSpotCheck` | [int32](GFF-File-Format#gff-data-types) | Area awareness-skill modifier |
| `ModListenCheck` | [int32](GFF-File-Format#gff-data-types) | Area listen-skill modifier |

## Script Hooks

The ARE script hooks are explicit in both the local schema and the recovered K1/TSL area loaders. `construct_are` reads `OnEnter`, `OnExit`, `OnHeartbeat`, and `OnUserDefined` as `ResRef`s with blank defaults, and the current retail loader recovery already shows those labels feeding the shared `ReadFieldCResRef` path in the area-header load. [[`construct_are` hook reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L372-L372), [`construct_are` hook reads continuation](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L372-L375)] `LoadAreaHeader @ (/K1/k1_win_gog_swkotor.exe @ 0x00508c50, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00718a20)` `ReadFieldCResRef @ (/K1/k1_win_gog_swkotor.exe @ 0x00411e10, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00624fa0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a12d0)`

| Field | Type | Description |
| ----- | ---- | ----------- |
| `OnEnter` | *ResRef* | Fires when entering area |
| `OnExit` | *ResRef* | Fires when leaving area |
| `OnHeartbeat` | *ResRef* | Fires periodically |
| `OnUserDefined` | *ResRef* | Fires on user-defined events |

## Minimap coordinate system

The ARE file contains a `Map` struct that defines how the minimap texture (`lbl_map<resname>`) aligns with the world space [walkmesh](Level-Layout-Formats#bwm). This coordinate system allows the game to display the player's position on the minimap and render map notes at correct locations.

### Map struct fields

| Field | Type | Description |
| ----- | ---- | ----------- |
| `MapPt1X` | float | First map point X coordinate (normalized 0.0-1.0) |
| `MapPt1Y` | float | First map point Y coordinate (normalized 0.0-1.0) |
| `MapPt2X` | float | Second map point X coordinate (normalized 0.0-1.0) |
| `MapPt2Y` | float | Second map point Y coordinate (normalized 0.0-1.0) |
| `WorldPt1X` | float | First world point X coordinate (world units) |
| `WorldPt1Y` | float | First world point Y coordinate (world units) |
| `WorldPt2X` | float | Second world point X coordinate (world units) |
| `WorldPt2Y` | float | Second world point Y coordinate (world units) |
| `NorthAxis` | [int32](GFF-File-Format#gff-data-types) | North direction orientation (0-3) |
| `MapZoom` | [int32](GFF-File-Format#gff-data-types) | Map zoom level |
| `MapResX` | [int32](GFF-File-Format#gff-data-types) | Map [texture](Texture-Formats#tpc) resolution X dimension |

These fields form two calibration pairs: two normalized map-space points and their matching world-space points, plus the `NorthAxis` flag that decides whether the transform is direct or axis-swapped. That is the same data shape PyKotor reads from `construct_are`, reone parses into `ARE_Map`, and reone copies into its live map object before doing coordinate conversion. [[`construct_are` map reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L323-L344), [reone `parseARE_Map`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/are.cpp#L283-L298), [reone `Map::loadProperties`](https://github.com/seedhartha/reone/blob/main/src/libs/game/gui/map.cpp#L51-L63)]

### Coordinate [transformation](Level-Layout-Formats#adjacencies-wok-only)

reone's `Map::getMapPosition()` is the cleanest published implementation of the ARE map transform. For `NorthAxis` values `0` and `1`, it scales world X and Y directly into map X and Y; for values `2` and `3`, it swaps the axes before applying the same linear interpolation shape. [[reone `Map::getMapPosition` direct case](https://github.com/seedhartha/reone/blob/main/src/libs/game/gui/map.cpp#L174-L188), [reone `Map::getMapPosition` swapped case](https://github.com/seedhartha/reone/blob/main/src/libs/game/gui/map.cpp#L188-L198)]

For **NorthAxis 0 or 1** (PositiveY or NegativeY):

```
scaleX = (MapPt1X - MapPt2X) / (WorldPt1X - WorldPt2X)
scaleY = (MapPt1Y - MapPt2Y) / (WorldPt1Y - WorldPt2Y)
mapPos.x = (world.x - WorldPt1X) * scaleX + MapPt1X
mapPos.y = (world.y - WorldPt1Y) * scaleY + MapPt1Y
```

For **NorthAxis 2 or 3** (PositiveX or NegativeX - swapped mapping):

```
scaleX = (MapPt1Y - MapPt2Y) / (WorldPt1X - WorldPt2X)
scaleY = (MapPt1X - MapPt2X) / (WorldPt1Y - WorldPt2Y)
mapPos.x = (world.y - WorldPt1Y) * scaleY + MapPt1X
mapPos.y = (world.x - WorldPt1X) * scaleX + MapPt1Y
```

### Inverse transformation

For rendering the minimap [texture](Texture-Formats#tpc) in world space:

```
worldScaleX = (WorldPt1X - WorldPt2X) / (MapPt1X - MapPt2X)
worldScaleY = (WorldPt1Y - WorldPt2Y) / (MapPt1Y - MapPt2Y)
world.x = WorldPt1X + (mapPos.x - MapPt1X) * worldScaleX
world.y = WorldPt1Y + (mapPos.y - MapPt1Y) * worldScaleY
```

For [texture](Texture-Formats#tpc) origin (0,0) in world space:

```
originX = WorldPt1X - MapPt1X * worldScaleX
originY = WorldPt1Y - MapPt1Y * worldScaleY
```

### NorthAxis values

| Value | Enum | Description | Coordinate Mapping |
| ----- | ---- | ----------- | ------------------ |
| 0 | PositiveY | +Y is north | Direct X/Y mapping |
| 1 | NegativeY | -Y is north | Direct X/Y mapping |
| 2 | PositiveX | +X is north | Swapped: world.x --> map.y, world.y --> map.x |
| 3 | NegativeX | -X is north | Swapped: world.x --> map.y, world.y --> map.x |

### Map [texture](Texture-Formats#tpc)

reone loads the area minimap texture as `lbl_map` plus the area resref and pairs it with the player-arrow texture at render time. Holocron Toolset's walkmesh renderer takes the complementary editor view: it builds 2D paths from walkmesh faces and then draws textures with an explicit translate, rotate, and scale step on top of that projection. [[reone `Map::loadTextures`](https://github.com/seedhartha/reone/blob/main/src/libs/game/gui/map.cpp#L64-L86), [walkmesh renderer face build](https://github.com/OpenKotOR/PyKotor/blob/master/Tools/HolocronToolset/src/toolset/gui/widgets/renderer/walkmesh.py#L560-L577), [walkmesh renderer image draw](https://github.com/OpenKotOR/PyKotor/blob/master/Tools/HolocronToolset/src/toolset/gui/widgets/renderer/walkmesh.py#L612-L635)]

### Implementation Notes

The evidence-backed implementation point here is simply that these values are float calibration data used to align a texture-space minimap with world-space area geometry. The page intentionally stops at that transform and renderer shape rather than prescribing extra editor heuristics that are not directly anchored in one of the cited code paths. [[`construct_are` map reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L323-L344), [reone `Map::getMapPosition`](https://github.com/seedhartha/reone/blob/main/src/libs/game/gui/map.cpp#L174-L198), [walkmesh renderer face build](https://github.com/OpenKotOR/PyKotor/blob/master/Tools/HolocronToolset/src/toolset/gui/widgets/renderer/walkmesh.py#L560-L577)]

## Rooms & Audio Zones

`Rooms` is another straightforward schema-derived list. PyKotor reads each row into `ARERoom` objects with `RoomName`, `EnvAudio`, `AmbientScale`, `DisableWeather`, and `ForceRating`, and reone parses the same members from the ARE GFF. [[`construct_are` rooms read](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L412-L419), [reone `parseARE_Rooms`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/are.cpp#L243-L252)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Rooms` | [List](GFF-File-Format#gff-data-types) | Room definitions for audio zones and minimap regions |

Each room row contains `RoomName`, `EnvAudio`, `AmbientScale`, and, in the KotOR II-shaped schema, optional `DisableWeather` and `ForceRating` values. [[`construct_are` rooms read](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L412-L419), [reone `parseARE_Rooms`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/are.cpp#L243-L252)]

## Implementation Notes

PyKotor deserializes ARE fields through `construct_are`, and the evidence-backed part of the minimap discussion is now confined to the map struct shape, the linear transform used by reone, and the corresponding walkmesh-plus-texture renderer shape in Holocron Toolset. The page intentionally avoids extra editor-specific bug taxonomies or workflow advice that are not directly grounded in those cited code paths. [[`construct_are`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L311-L419), [reone `Map::getMapPosition`](https://github.com/seedhartha/reone/blob/main/src/libs/game/gui/map.cpp#L174-L198), [walkmesh renderer image draw](https://github.com/OpenKotOR/PyKotor/blob/master/Tools/HolocronToolset/src/toolset/gui/widgets/renderer/walkmesh.py#L612-L635)]

## See also

- [GFF File Format](GFF-File-Format) - Generic format underlying ARE
- [GFF Creature and Dialogue](GFF-Creature-and-Dialogue) - UTC and DLG types
- [GFF Items and Economy](GFF-Items-and-Economy) - UTI, UTM, JRL, FAC types
- [GFF Spatial Objects](GFF-Spatial-Objects) - UTD, UTP, UTT, UTE, UTS, UTW types
- [BWM (Walkmesh)](Level-Layout-Formats#bwm) - Area walkable surfaces and minimap alignment
- [LYT](Level-Layout-Formats#lyt) — layout
- [VIS](Level-Layout-Formats#vis) — visibility
- [Bioware Aurora Area File Format](Bioware-Aurora-Module-and-Area#areafile) - Official ARE specification


---

<a id="git"></a>

# GIT ([game instance template](GFF-File-Format#git-game-instance-template))

Part of the [GFF File Format Documentation](GFF-File-Format).

[GIT files](GFF-File-Format#git-game-instance-template) are the dynamic companion to ARE: the local schema stores per-area instance lists for creatures, doors, placeables, triggers, waypoints, stores, encounters, sounds, and cameras, plus an `AreaProperties` struct for ambient-audio and music integers. The exact KotOR retail list-label reads still need a cleaner caller pass than the current ARE loader work, so the object-family split below is intentionally schema-derived, but the underlying consumption path is the same typed GFF machinery used across KotOR I, KotOR II, and Aurora. [[`GIT` class and section layout](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L57-L147), [`construct_git` root reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1128-L1334)] `GetFieldByLabel @ (/K1/k1_win_gog_swkotor.exe @ 0x00411630, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00623a40, /Other BioWare Engines/Aurora/nwmain.exe @ 0x14019fcc0)` `GetListCount @ (/K1/k1_win_gog_swkotor.exe @ 0x00411940, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00624970, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a0370)` `ReadFieldCResRef @ (/K1/k1_win_gog_swkotor.exe @ 0x00411e10, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00624fa0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a12d0)`

PyKotor carries area instance state through [`GIT`, its `GITCreature` / `GITDoor` / related subclasses, plus `construct_git`, `read_git`, and `write_git`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L57), labels the resource as [`GFFContent.GIT`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py#L162), and parses it through [`GFFBinaryReader.load`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/io_gff.py#L82); Holocron Toolset mirrors that data in its [`git.py` instance editor](https://github.com/OpenKotOR/HolocronToolset/src/toolset/gui/editors/git/git.py) and related module-resource workflows. The same generic-GFF treatment appears in reone's [`gff.cpp`](https://github.com/seedhartha/reone/blob/master/src/libs/resource/gff.cpp) and [`gffreader.cpp`](https://github.com/seedhartha/reone/blob/master/src/libs/resource/format/gffreader.cpp), KotOR.js's [`GFFObject.ts`](https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/resource/GFFObject.ts#L24), Kotor.NET's [`GFF.cs`](https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Formats/KotorGFF/GFF.cs#L18), and xoreos's Aurora loader stack.

## Root properties (ambient audio and music)

These integers are schema-derived from the `AreaProperties` nested struct inside the GIT root. PyKotor acquires that struct first and then reads `AmbientSndDayVol`, `AmbientSndDay`, `EnvAudio`, `MusicDay`, `MusicBattle`, and `MusicDelay` with `0` defaults when the struct or individual fields are absent, which is the narrow claim justified here. [[`construct_git` AreaProperties reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1147-L1154)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `AmbientSndDay` | Int | Day ambient sound ID |
| `AmbientSndDayVol` | Int | Day ambient volume (0-127) |
| `AmbientSndNight` | Int | Night ambient sound ID |
| `AmbientSndNitVol` | Int | Night ambient volume |
| `EnvAudio` | Int | Environment audio type |
| `MusicBattle` | Int | Battle music track ID |
| `MusicDay` | Int | Standard/exploration music ID |
| `MusicNight` | Int | Night music track ID |
| `MusicDelay` | Int | Delay before music starts (seconds) |

PyKotor's current retail-oriented reader does not populate `AmbientSndNight`, `AmbientSndNitVol`, or `MusicNight` in `construct_git`, so those fields should be read here as schema members that appear in older format descriptions and sibling implementations, not as fields this specific local reader currently depends on during deserialization. [[`construct_git` AreaProperties reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1147-L1154)]

## Instance Lists

[GIT](GFF-File-Format#git-game-instance-template) files carry multiple top-level instance lists, and PyKotor deserializes each one independently with blank `ResRef`, zero transform, or empty-list defaults when the list or fields are absent. The table below is therefore schema-derived from the actual list names consumed by `construct_git`, not from a fully recovered retail caller walk yet. [[`construct_git` list iteration](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1156-L1334)]

| List field | Contains | Description |
| ---------- | -------- | ----------- |
| `Creature List` | GITCreature | Spawned NPCs and enemies |
| `Door List` | GITDoor | Placed doors |
| `Placeable List` | GITPlaceable | Containers, furniture, objects |
| `Encounter List` | GITEncounter | Encounter spawn zones |
| `TriggerList` | GITTrigger | Trigger volumes |
| `WaypointList` | GITWaypoint | Waypoint markers |
| `StoreList` | GITStore | Merchant vendors |
| `SoundList` | GITSound | Positional audio emitters |
| `CameraList` | GITCamera | Camera definitions |

Across those lists, the repeated pattern is straightforward: most instance structs store a template `ResRef`, placement coordinates, and then a small set of per-instance overrides such as tag strings, bearings, link targets, or local payload structs like trigger geometry. [[`construct_git` creature/door/placeable/store/trigger/waypoint reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1166-L1334)]

## GITCreature Instances

Creature rows are the simplest placement records in the file. The current reader acquires `TemplateResRef`, `XPosition`, `YPosition`, `ZPosition`, and the planar orientation pair, then derives the stored bearing from those orientation components. [[`construct_git` creature reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1166-L1177)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `TemplateResRef` | *ResRef* | [UTC](GFF-File-Format#utc-creature) template to spawn |
| `XPosition` | Float | World X coordinate |
| `YPosition` | Float | World Y coordinate |
| `ZPosition` | Float | World Z coordinate |

## GITDoor Instances

Door instances extend the same placement pattern with module-link data and an optional tweak-color override. In the local reader, `Door List` rows acquire `LinkedTo`, `LinkedToFlags`, `LinkedToModule`, `TransitionDestin`, `Bearing`, placement coordinates, and an optional `TweakColor` gated by `UseTweakColor`. [[`construct_git` door reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1179-L1197)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `LinkedToFlags` | Byte | Transition flags |
| `TransitionDestin` | [CExoLocString](GFF-File-Format#gff-data-types) | Destination label (UI) |
| `X`, `Y`, `Z` | Float | position coordinates |

## GITPlaceable Instances

Placeable rows are simpler: the current reader acquires `TemplateResRef`, `X`, `Y`, `Z`, `Bearing`, and the same optional tweak-color pattern used by doors. [[`construct_git` placeable reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1220-L1233)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Bearing` | Float | rotation angle |
| `TweakColor` | DWord | color tint |
| `Hitpoints` | Short | Current HP override |
| `Useable` | Byte | Can be used override |

## GITTrigger Instances

Trigger rows add module-transition linkage and local geometry. The current reader acquires `TemplateResRef`, `Tag`, `LinkedTo`, `LinkedToFlags`, `LinkedToModule`, `TransitionDestin`, placement coordinates, and then optionally walks a `Geometry` list whose rows carry `PointX`, `PointY`, and `PointZ`. [[`construct_git` trigger reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1260-L1287)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `TemplateResRef` | *ResRef* | [UTT](GFF-File-Format#utt-trigger) template |
| `Tag` | [CExoString](GFF-File-Format#gff-data-types) | Instance tag |
| `TransitionDestin` | [CExoLocString](GFF-File-Format#gff-data-types) | Transition label |
| `LinkedToModule` | *ResRef* | Destination module |
| `LinkedTo` | [CExoString](GFF-File-Format#gff-data-types) | Destination waypoint |
| `LinkedToFlags` | Byte | Transition flags |
| `X`, `Y`, `Z` | Float | Trigger position |
| `XPosition`, `YPosition`, `ZPosition` | Float | Position (alternate) |
| `XOrientation`, `YOrientation`, `ZOrientation` | Float | orientation |
| `Geometry` | List | Trigger volume [vertices](MDL-MDX-File-Format#vertex-structure) |

## GITWaypoint Instances

Waypoint rows combine the shared placement fields with waypoint-specific UI state. PyKotor reads `LocalizedName`, `Tag`, `TemplateResRef`, `XPosition`, `YPosition`, `ZPosition`, planar orientation, appearance, map-note flags, and an optional localized `MapNote`. [[`construct_git` waypoint reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1289-L1310)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `TemplateResRef` | *ResRef* | [UTW](GFF-File-Format#utw-waypoint) template |
| `Tag` | [CExoString](GFF-File-Format#gff-data-types) | Waypoint identifier |
| `Appearance` | DWord | Waypoint appearance type |
| `LinkedTo` | [CExoString](GFF-File-Format#gff-data-types) | Linked waypoint tag |
| `X`, `Y`, `Z` | Float | position coordinates |
| `XOrientation`, `YOrientation` | Float | orientation |
| `HasMapNote` | Byte | Has map note |
| `MapNote` | [CExoLocString](GFF-File-Format#gff-data-types) | Map note text |
| `MapNoteEnabled` | Byte | Map note visible |

## GITEncounter Instances

Encounter rows are schema-derived from `Encounter List`: the local reader acquires a template `ResRef`, position, an optional `Geometry` list using `X`, `Y`, `Z` point fields, and an optional `SpawnPointList` with spawn coordinates plus a single `Orientation` float. [[`construct_git` encounter reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1199-L1218)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `TemplateResRef` | *ResRef* | [UTE](GFF-File-Format#ute-encounter) template |
| `Tag` | [CExoString](GFF-File-Format#gff-data-types) | Encounter identifier |
| `X`, `Y`, `Z` | Float | Spawn position |
| `Geometry` | List | Spawn zone boundary |

## GITStore Instances

Store rows are one of the clearer examples of GIT-as-instance-data: the local reader acquires a store `ResRef`, position, and the planar orientation pair, then derives the bearing exactly as it does for creature instances. [[`construct_git` store reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1242-L1258)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `TemplateResRef` | *ResRef* | [UTM](GFF-File-Format#utm-merchant) template |
| `ResRef` | *ResRef* | Store ResRef |
| `Tag` | [CExoString](GFF-File-Format#gff-data-types) | Store identifier |
| `X`, `Y`, `Z` | Float | Position (for UI, not physical) |
| `XOrientation`, `YOrientation` | Float | orientation |

## GITSound Instances

Sound rows are minimal in the current local reader: PyKotor acquires a `TemplateResRef` plus `XPosition`, `YPosition`, and `ZPosition`, leaving the richer sound-emitter schema to the broader format table and sibling implementations. [[`construct_git` sound reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1234-L1240)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `TemplateResRef` | *ResRef* | [UTS](GFF-File-Format#uts-sound) template |
| `Tag` | [CExoString](GFF-File-Format#gff-data-types) | Sound identifier |
| `X`, `Y`, `Z` | Float | Emitter position |
| `MaxDistance` | Float | Audio falloff distance |
| `MinDistance` | Float | Full volume radius |
| `RandomRangeX`, `RandomRangeY` | Float | position randomization |
| `Volume` | Byte | Volume level (0-127) |

## GITCamera Instances

Camera rows are also explicit in the local schema: `CameraList` entries acquire `CameraID`, `FieldOfView`, `Height`, `MicRange`, `Orientation`, `Position`, and `Pitch`, which is enough to justify the table below without leaning on unsourced editor behavior claims. [[`construct_git` camera reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1156-L1164)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `CameraID` | Int | Camera identifier |
| `FieldOfView` | Float | Field of view (degrees) |
| `Height` | Float | Camera height |
| `MicRange` | Float | Audio capture range |
| `Orientation` | Vector4 | Camera rotation ([quaternion](MDL-MDX-File-Format#node-header)) |
| `Pitch` | Float | Camera pitch angle |
| `Position` | Vector3 | Camera position |

## Implementation Notes

At the schema level, GIT is the instance layer that places and selectively overrides blueprint-backed objects, while ARE remains the static area-configuration layer. That division is visible directly in the local model types: `construct_git` builds per-instance rows around template `ResRef`s and placement/orientation data, whereas `construct_are` handles the area's persistent environmental configuration. [[`GIT` model types and `construct_git`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L57-L147), [`construct_are`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L311-L419)]

### See also

- [GFF-File-Format](GFF-File-Format) -- GFF structure
- [TSLPatcher GFFList Syntax](TSLPatcher-GFF-Syntax#gfflist-syntax) -- Patching GIT via mod installers
- [Container-Formats#key](Container-Formats#key) -- Resource resolution


---

<a id="ifo"></a>

# IFO ([module info](GFF-File-Format#ifo-module-info))

Part of the [GFF File Format Documentation](GFF-File-Format).

IFO is the module-scope companion to ARE and GIT. PyKotor's schema records `Mod_Entry_Area`, entry coordinates and facing, `Mod_Area_list`, and the module-wide `Mod_On*` script hooks as first-class fields, which is the safest level to document until the KotOR retail module-loader names are recovered with the same field-name visibility already available for ARE. [[`IFO` class fields](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L25-L84), [`construct_ifo`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L87-L154)] `GetFieldByLabel @ (/K1/k1_win_gog_swkotor.exe @ 0x00411630, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00623a40, /Other BioWare Engines/Aurora/nwmain.exe @ 0x14019fcc0)` `ReadFieldCResRef @ (/K1/k1_win_gog_swkotor.exe @ 0x00411e10, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00624fa0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a12d0)` `ReadFieldCExoLocString @ (/K1/k1_win_gog_swkotor.exe @ 0x00411fd0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00625240, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a0f80)`

PyKotor models module descriptors through [`IFO`, `construct_ifo`, `read_ifo`, and `write_ifo`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L18), tags them as [`GFFContent.IFO`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py#L164), and decodes them through the same shared [`GFFBinaryReader.load`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/io_gff.py#L82) path that Holocron Toolset builds on for entry points, area lists, and module scripts in its getting-started, module-editor, and module-resources flows. Reone's [`gff.cpp`](https://github.com/seedhartha/reone/blob/master/src/libs/resource/gff.cpp) and [`gffreader.cpp`](https://github.com/seedhartha/reone/blob/master/src/libs/resource/format/gffreader.cpp), KotOR.js's [`GFFObject.ts`](https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/resource/GFFObject.ts#L24), Kotor.NET's [`GFF.cs`](https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Formats/KotorGFF/GFF.cs#L18), and xoreos's Aurora loader likewise treat IFO as a typed GFF root rather than a separate binary dialect.

## Core Module Identity

These fields are schema-derived from the IFO root. PyKotor reads `Mod_ID`, `Mod_VO_ID`, `Mod_Name`, `Mod_Tag`, and the module entry configuration directly from the root struct, defaulting missing binary/string fields to empty values and missing localized strings to `LocalizedString.from_invalid()`. [[`construct_ifo` root reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L98-L106), [`IFO` defaults](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L25-L84)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Mod_ID` | Void (16 bytes) | Unique module identifier (GUID) |
| `Mod_Tag` | [CExoString](GFF-File-Format#gff-data-types) | Module tag identifier |
| `Mod_Name` | [CExoLocString](GFF-File-Format#gff-data-types) | Module name (localized) |
| `Mod_Description` | [CExoLocString](GFF-File-Format#gff-data-types) | Module description (localized) |
| `Mod_Creator_ID` | UInt32 | Toolset creator ID |
| `Mod_Version` | UInt32 | Module version number |
| `Mod_VO_ID` | [CExoString](GFF-File-Format#gff-data-types) | Voice-over folder name |

`Mod_Description`, `Mod_Creator_ID`, and `Mod_Version` live in the same root schema but are part of the broader optional/deprecated-style block in the current reader rather than the minimum entry-state read path. [[`construct_ifo` optional block](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L118-L139)]

## Entry Configuration

The module entry block is one of the cleanest parts of the local IFO schema: `Mod_Entry_Area` is read as a `ResRef`, `Mod_Entry_X/Y/Z` are read as floats, and `Mod_Entry_Dir_X/Y` are combined into the stored facing angle. When both direction components are absent or zero, the local reader documents the observed-retail fallback as a forward `(1, 0)` entry vector. [[`construct_ifo` entry reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L102-L145)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Mod_Entry_Area` | *ResRef* | Starting [area](GFF-File-Format#are-area) *ResRef* |
| `Mod_Entry_X` | Float | Entry X coordinate |
| `Mod_Entry_Y` | Float | Entry Y coordinate |
| `Mod_Entry_Z` | Float | Entry Z coordinate |
| `Mod_Entry_Dir_X` | Float | Entry direction X (facing) |
| `Mod_Entry_Dir_Y` | Float | Entry direction Y (facing) |

## Area List

`Mod_Area_list` is also schema-derived but precise in the local reader: PyKotor acquires the list, inspects only the first row during construction, and reads `Area_Name` from that row as the canonical area `ResRef` when present. The writer side always emits at least one `Area_Name` row, so the current local tooling model treats one explicit area reference as the minimum serialized shape. [[`construct_ifo` area list read](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L146-L151), [`dismantle_ifo` area list write](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L192-L193)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Mod_Area_list` | [List](GFF-File-Format#gff-data-types) | Areas in this module |

The row structure relevant to current tooling is just `Area_Name`, stored as the referenced area `ResRef`. [[`construct_ifo` area list read](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L146-L151), [reone `IFO_Mod_Area_list` and `parseIFO_Mod_Area_list`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/ifo.cpp#L27-L32)]

## Expansion Pack Requirements

This block should stay at the schema level for now. PyKotor reads `Expansion_Pack` into `ifo.expansion_id`, and reone parses the same field into its generated `IFO` struct; that is the strongest claim currently supported here, while `Mod_MinGameVer` still reads as a format-convention field pending a better source-backed pass. [[`construct_ifo` expansion read](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L130), [reone `IFO` field layout](https://github.com/seedhartha/reone/blob/main/include/reone/resource/parser/gff/ifo.h#L32-L49), [reone `parseIFO`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/ifo.cpp#L34-L46)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Expansion_Pack` | [word](GFF-File-Format#gff-data-types) | Expansion-pack field |
| `Mod_MinGameVer` | [CExoString](GFF-File-Format#gff-data-types) | Minimum game version |

Older format references often describe `Expansion_Pack` as a bitfield, but that interpretation should remain secondary here until it is tied to stronger runtime evidence. [[`construct_ifo` expansion read](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L130), [reone `parseIFO`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/ifo.cpp#L34-L46)]

## Starting Movie & HAK files

These are straightforward root fields in both the local and sibling parsers. PyKotor reads `Mod_Hak` as a string and `Mod_StartMovie` as a `ResRef`, while reone parses the same two members into its generated `IFO` struct. [[`construct_ifo` HAK/movie reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L131-L142), [reone `IFO` field layout](https://github.com/seedhartha/reone/blob/main/include/reone/resource/parser/gff/ifo.h#L32-L75), [reone `parseIFO`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/ifo.cpp#L46-L78)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Mod_StartMovie` | *ResRef* | Starting movie file |
| `Mod_Hak` | [CExoString](GFF-File-Format#gff-data-types) | Required HAK file list |

The safer wording here is simply that IFO stores a starting-movie resref and a HAK-list string; specific launch semantics are left for a runtime audit. [[`construct_ifo` HAK/movie reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L131-L142)]

## Cache & XP Settings

This subsection needs one distinction that the older text blurred: PyKotor reads `Mod_XPScale`, but its current `construct_ifo` path does not preserve `Mod_IsSaveGame` on read. reone parses both fields, and PyKotor's writer emits `Mod_IsSaveGame` as `0` when constructing a fresh IFO. [[`construct_ifo` XP read](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L141), [`dismantle_ifo` savegame write](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L170-L181), [reone `IFO` field layout](https://github.com/seedhartha/reone/blob/main/include/reone/resource/parser/gff/ifo.h#L49-L75), [reone `parseIFO`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/ifo.cpp#L46-L78)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Mod_IsSaveGame` | [byte](GFF-File-Format#gff-data-types) | Module is from save file |
| `Mod_XPScale` | [byte](GFF-File-Format#gff-data-types) | Experience point multiplier (0-200%) |

So `Mod_IsSaveGame` belongs here as a schema-visible field, but not as a value the current local reader fully round-trips. [[`construct_ifo` XP read](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L141), [`dismantle_ifo` savegame write](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L170-L181), [reone `parseIFO`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/ifo.cpp#L46-L78)]

## Timekeeping Fields

These timing fields are still part of the active schema in both codebases even though the current module-entry evidence collected for this page does not depend on them. PyKotor reads them into `dawn_hour`, `dusk_hour`, `time_scale`, `start_month`, `start_day`, `start_hour`, and `start_year`, and reone parses the same members into its generated `IFO` struct. [[`construct_ifo` time-field reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L134-L141), [reone `IFO` field layout](https://github.com/seedhartha/reone/blob/main/include/reone/resource/parser/gff/ifo.h#L32-L75), [reone `parseIFO`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/ifo.cpp#L34-L78)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Mod_StartMonth` | UInt32 | Module start month |
| `Mod_StartDay` | UInt32 | Module start day |
| `Mod_StartHour` | UInt32 | Module start hour |
| `Mod_StartYear` | UInt32 | Module start year |
| `Mod_DawnHour` | [byte](GFF-File-Format#gff-data-types) | Dawn start hour |
| `Mod_DuskHour` | [byte](GFF-File-Format#gff-data-types) | Dusk start hour |
| `Mod_MinPerHour` | UInt32 | Minutes per in-game hour |

For now, these remain documented as schema-visible timing fields rather than as proven live day/night controls in KotOR retail. [[`construct_ifo` time-field reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L134-L141), [reone `parseIFO`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/ifo.cpp#L34-L78)]

## Module Script Hooks

The module-hook block is straightforward in the local reader: `construct_ifo` acquires the `Mod_On*` `ResRef` fields directly from the IFO root and defaults them to blank `ResRef`s when omitted. That is the evidence-backed claim here; anything more specific about exact retail dispatch timing still belongs in a later reverse-engineering pass. [[`construct_ifo` hook reads](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L106-L118)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Mod_OnAcquirItem` | *ResRef* | Fires when item acquired |
| `Mod_OnActvtItem` | *ResRef* | Fires when item activated/used |
| `Mod_OnClientEntr` | *ResRef* | Fires on player enter (multiplayer) |
| `Mod_OnClientLeav` | *ResRef* | Fires on player leave (multiplayer) |
| `Mod_OnCutsnAbort` | *ResRef* | Fires when cutscene aborted |
| `Mod_OnHeartbeat` | *ResRef* | Fires periodically |
| `Mod_OnModLoad` | *ResRef* | Fires when module finishes loading |
| `Mod_OnModStart` | *ResRef* | Fires after player spawned |
| `Mod_OnPlrDeath` | *ResRef* | Fires when player dies |
| `Mod_OnPlrDying` | *ResRef* | Fires when player HP reaches 0 |
| `Mod_OnPlrLvlUp` | *ResRef* | Fires on level up |
| `Mod_OnPlrRest` | *ResRef* | Fires when player rests |
| `Mod_OnSpawnBtnDn` | *ResRef* | Fires on spawn button (multiplayer) |
| `Mod_OnUnAqreItem` | *ResRef* | Fires when item lost/sold |
| `Mod_OnUsrDefined` | *ResRef* | Fires on user-defined events |

## Implementation Notes

At the code level, IFO still fills the module-metadata and entry-selection role, while ARE and GIT supply the chosen area's static and dynamic data. reone's module loader makes that split explicit by parsing IFO first and then loading the target area's ARE and GIT together. [[`construct_ifo`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/ifo.py#L94-L166), [`construct_are`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py#L311-L419), [`construct_git`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/git.py#L1128-L1334), [reone `Module::load` and `loadArea`](https://github.com/seedhartha/reone/blob/main/src/libs/game/object/module.cpp#L42-L96)]

### See also

- [GFF-File-Format](GFF-File-Format) -- Generic format underlying IFO
- [GFF-ARE (Area)](GFF-Module-and-Area#are) - Area properties; Mod_Entry_Area and Mod_Area_list
- [GIT (Game Instance Template)](GFF-File-Format#git-game-instance-template) - Dynamic area contents
- [Bioware Aurora IFO Format](Bioware-Aurora-Module-and-Area#ifo) - Official module info specification


---

<a id="pth"></a>

# PTH (Path)

PTH is the area path graph resource. PyKotor models it as a GFF-backed `PTH` object whose `Path_Points` rows store 2D coordinates plus an edge-count window into `Path_Conections`, and reone parses the same two lists before converting them into an adjacency list for runtime pathfinding. [[`PTH` and `construct_pth`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/pth.py#L16-L169), [reone `PTH` structs](https://github.com/seedhartha/reone/blob/main/include/reone/resource/parser/gff/pth.h#L19-L50), [reone `parsePTH`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/pth.cpp#L27-L52), [reone `Paths::loadPath`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/provider/paths.cpp#L36-L64)]

In reone's area loader, that parsed path data is elevated into 3D by sampling walkmesh elevation and then handed to the pathfinder, which makes the narrow runtime claim here defensible: PTH is the coarse graph layer, while the walkmesh still supplies area elevation and collision context. [[reone `Area::loadPTH`](https://github.com/seedhartha/reone/blob/main/src/libs/game/object/area.cpp#L394-L415), [reone `Pathfinder::load`](https://github.com/seedhartha/reone/blob/main/src/libs/game/pathfinder.cpp#L40-L55)]

## Path points

Each `Path_Points` row stores a 2D waypoint plus the slice of the connection list that belongs to it. PyKotor reconstructs outgoing edges by reading `Conections` and `First_Conection` and then walking the `Path_Conections` list; reone's provider does the same when building `Path::Point::adjPoints`. [[`construct_pth`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/pth.py#L138-L163), [reone `PTH_Path_Points`](https://github.com/seedhartha/reone/blob/main/include/reone/resource/parser/gff/pth.h#L25-L33), [reone `Paths::loadPath`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/provider/paths.cpp#L36-L64)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Path_Points` | List | List of 2D navigation nodes for this area |

The row members are `X`, `Y`, `Conections`, and `First_Conection`. The misspelling is part of the on-disk schema and is preserved by both PyKotor and reone. [[`construct_pth`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/pth.py#L145-L157), [reone `parsePTH_Path_Points`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/pth.cpp#L27-L41)]

## Path connections

`Path_Conections` is the flat edge table referenced by those point rows. Both PyKotor and reone treat each row as a single destination index. [[`construct_pth`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/pth.py#L138-L163), [reone `PTH_Path_Conections`](https://github.com/seedhartha/reone/blob/main/include/reone/resource/parser/gff/pth.h#L34-L40), [reone `parsePTH_Path_Conections`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/pth.cpp#L35-L41)]

| Field | Type | Description |
| ----- | ---- | ----------- |
| `Path_Connections` | List | Directed edges between path nodes |

The only member on each row is `Destination`, which indexes another entry in `Path_Points`. [[`construct_pth`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/pth.py#L159-L162), [reone `parsePTH_Path_Conections`](https://github.com/seedhartha/reone/blob/main/src/libs/resource/parser/gff/pth.cpp#L35-L41)]

## Notes

PyKotor explicitly treats missing `Path_Points` and `Path_Conections` lists as empty and defaults per-point coordinates and indices to `0.0` and `0` respectively when fields are absent. [[`PTH` docstring and `construct_pth`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/pth.py#L16-L163)]

The path graph itself is 2D on disk: PTH stores only `X` and `Y`, while reone derives per-node `Z` values later by testing walkmesh elevation before loading the graph into the pathfinder. [[reone `PTH_Path_Points`](https://github.com/seedhartha/reone/blob/main/include/reone/resource/parser/gff/pth.h#L25-L33), [reone `Area::loadPTH`](https://github.com/seedhartha/reone/blob/main/src/libs/game/object/area.cpp#L394-L415)]

That separation is the important distinction from [BWM](Level-Layout-Formats#bwm): PTH supplies graph connectivity, while the walkmesh still supplies the physical surface the game samples against. [[reone `Area::loadPTH`](https://github.com/seedhartha/reone/blob/main/src/libs/game/object/area.cpp#L394-L415), [reone `Pathfinder::load`](https://github.com/seedhartha/reone/blob/main/src/libs/game/pathfinder.cpp#L40-L55)]

### See also

- [GFF File Format](GFF-File-Format) - Parent GFF format
- [GFF-ARE](GFF-Module-and-Area#are) - Area properties
- [GFF-GIT](GFF-Module-and-Area#git) - Game instance template (creature and encounter placement)
- [BWM File Format](Level-Layout-Formats#bwm) - Walkmesh (distinct from PTH)
- [GFF-UTW](GFF-Spatial-Objects#utw) - Waypoints (used for NPC patrol scripts)

