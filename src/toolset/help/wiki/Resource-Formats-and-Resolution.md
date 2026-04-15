# Resource formats and resolution

KotOR does not resolve resources by extension alone. The effective lookup key is a `(ResRef, type ID)` pair, and both PyKotor's registry model and the recovered engine routines treat those two values as the identity of a resource rather than as optional metadata attached after a filename match. [[`ResourceTuple`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L147-L172), [`ResourceType`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L175-L209)] `CExoResMan::Exists @ (/K1/k1_win_gog_swkotor.exe @ 0x00408bc0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x0061b830, /Other BioWare Engines/Aurora/nwmain.exe @ 0x14018f590)` `CResGFF::ReadFieldCResRef @ (/K1/k1_win_gog_swkotor.exe @ 0x00411e10, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00624fa0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a12d0)`

This page deliberately mixes two different evidence classes and labels them accordingly. Runtime-behavior statements in the opening sections are restricted to claims that can be anchored in at least three binaries from the current Odyssey project; the large type-ID tables later in the page are explicitly **registry-derived** from PyKotor's `ResourceType` enum and its `supported_engines` metadata. [[`BiowareEngine`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L49-L67), [`ResourceType`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L175-L209)] For the broader prose on precedence and localized-string behavior, see [Concepts](Concepts).

## Resource resolution order

Full prose (resource manager demands, KEY's role, override vs [MOD/ERF](Container-Formats#erf)/[RIM](Container-Formats#rim)): **[Concepts — Resource resolution order](Concepts#resource-resolution-order)**.

Operational summary:

1. PyKotor exposes the top-level search layers as `OVERRIDE`, `MODULES`, and `CHITIN`, and its CHITIN branch explicitly checks both `self._chitin` and `self._patch_erf`. [[`SearchLocation`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/installation.py#L67-L104), [`check_list(self._chitin) or check_list(self._patch_erf)`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/installation.py#L1984)]
2. The recovered existence probe confirms that resource lookup is a typed table lookup, not a loose filename search. K1 routes `CExoResMan::Exists` through `GetKeyEntry`; TSL routes the same public probe through a less descriptive helper; Aurora exposes an override-first step by calling `GetOverride` and then `FindKey` on resident tables. `CExoResMan::Exists @ (/K1/k1_win_gog_swkotor.exe @ 0x00408bc0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x0061b830, /Other BioWare Engines/Aurora/nwmain.exe @ 0x14018f590)`
3. The keyed-archive fallback is maintained as live state. `CExoKeyTable::RebuildTable` is present in all three binaries and rewires entries into lookup structures after table changes or reloads, which is the engine-side reason the KEY/BIF layer behaves like an indexed fallback rather than as ad hoc archive scanning. `CExoKeyTable::RebuildTable @ (/K1/k1_win_gog_swkotor.exe @ 0x00410260, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x006304a0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x14018ccf0)`
4. This page therefore treats override, module capsules, and keyed archives as distinct layers, but only the override and keyed-table parts are directly anchored here at function scope. The more detailed prose about module precedence remains on [Concepts](Concepts), where the same distinction is scoped to the evidence currently recovered.

## ResRef and resource type

**ResRef** is the base resource name. **Resource type** is the numeric discriminator that tells the engine what the bytes represent. PyKotor records that distinction directly in each `ResourceTuple`, which stores the numeric `type_id`, extension, broad category, storage family, and declared engine support rather than only a filename extension. [[`ResourceTuple`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L147-L172), [`ResourceType`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L175-L209)]

The binary GFF decode path reinforces the same model. `CResGFF::ReadFieldCResRef` checks for field type `0xb`, validates the serialized payload length, reads the leading name length byte, and then constructs a `CResRef` from the remaining bytes in K1, TSL, and Aurora. `CResGFF::ReadFieldCResRef @ (/K1/k1_win_gog_swkotor.exe @ 0x00411e10, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00624fa0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a12d0)`

The discrepancies are implementation-level rather than semantic. K1 reaches a `CResRef` constructor quickly after the field and size checks; TSL performs the same validation inside a larger x86 routine; Aurora exposes the final decode step as `InitFromCharArray`. `CResGFF::ReadFieldCResRef @ (/K1/k1_win_gog_swkotor.exe @ 0x00411e10, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00624fa0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a12d0)`

Use the tables on this page with the following reading rules:

- **Type ID** is the canonical numeric value stored by containers and resource managers.
- **Contents** tells you the storage family, which matters for whether a file is raw binary, text, [GFF](GFF-File-Format)-backed, [ERF](Container-Formats#erf)-backed, or LIP-specific.
- **Engine support** should be read as "known/declared support in the registry", not "confirmed retail usage in every shipped title". Some entries survive in the registry because KotOR tooling inherits broader Aurora/Odyssey lineage [[`BiowareEngine`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L49-L67)].

**Language IDs** (`dialog.tlk`, localization): [Concepts — Language IDs](Concepts#language-ids-kotor).

## Resource Type Identifiers

The type-ID catalog below is registry-derived. Its authoritative source is PyKotor's `ResourceType` enum and the attached `supported_engines` metadata, not the current reverse-engineering pass. [[`ResourceType`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L175-L209), [`ResourceType` classic range](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L231-L320), [`ResourceType` Odyssey extension block](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L992-L1052)]

For KotOR specifically, the important structural split is that the inherited classic range and the Odyssey-only `3000+` extension block live in the same registry. That extension block includes several of the format families modders actually touch, including `lyt`, `vis`, `rim`, `pth`, `lip`, `bwm`, `tpc`, `mdx`, and `bip`. [[`LYT` through `MDX`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L992-L1052), [`BIP`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L1139-L1145)]

### Common KotOR resource types

| Resource | Type ID | Contents | Engine support | Typical use |
| -------- | ------- | -------- | -------------- | ----------- |
| [2DA](2DA-File-Format) | `0x07E1` | binary table | Aurora, Odyssey, Eclipse | Gameplay tables, progression data, spell rows, appearances, and shared configuration |
| [ARE](GFF-Module-and-Area#are) | `0x07DC` | GFF | Aurora, Odyssey | Area metadata |
| [DLG](GFF-Creature-and-Dialogue#dlg) | `0x07ED` | GFF | Aurora, Odyssey, Eclipse | Dialog trees and conversation state |
| [ERF](Container-Formats#erf) / [MOD](Container-Formats#erf) / [SAV](Container-Formats#erf) / [RIM](Container-Formats#rim) | `0x270D` / `0x07DB` / `0x0809` / `3002` | container | Aurora/Odyssey, Odyssey | Capsule-style module, save, and shipped-area containers |
| [GFF](GFF-File-Format) | `0x07F5` | GFF | Aurora, Odyssey, Eclipse | Structured binary payload family used by most UT*, DLG, GIT, IFO, JRL, GUI, and related resources |
| [GIT](GFF-Module-and-Area#git) / [IFO](GFF-Module-and-Area#ifo) | `0x07E7` / `0x07DE` | GFF | Aurora, Odyssey | Module instance state and module metadata |
| [LIP](Audio-and-Localization-Formats#lip) / `BIP` | `3004` / `3028` | lips | Odyssey | Lip-sync timing and related facial timing data |
| [LYT](Level-Layout-Formats#lyt) / [VIS](Level-Layout-Formats#vis) / [PTH](GFF-Spatial-Objects#pth) | `3000` / `3001` / `3003` | plaintext / plaintext / GFF | Odyssey | Area layout, room visibility, and path data |
| [MDL](MDL-MDX-File-Format) / [MDX](MDL-MDX-File-Format) | `0x07D2` / `3008` | binary | Aurora/Odyssey/Eclipse, Odyssey | Model hierarchy plus mesh-sidecar data |
| [NCS](NCS-File-Format) / [NSS](NSS-File-Format) | `0x07DA` / `0x07D9` | binary / plaintext | Aurora, Odyssey | Compiled and source NWScript |
| [SSF](Audio-and-Localization-Formats#ssf) / [TLK](Audio-and-Localization-Formats#tlk) | `0x080C` / `0x07E2` | binary | Aurora, Odyssey / Aurora, Odyssey, Eclipse | Soundset-to-StrRef mappings and localized talk table strings |
| [TPC](Texture-Formats#tpc) / [TGA](https://en.wikipedia.org/wiki/Truevision_TGA) / [DDS](Texture-Formats#dds) / [TXI](Texture-Formats#txi) | `3007` / `0x0003` / `0x07F1` / `0x07E6` | binary / binary / binary / plaintext | Odyssey / shared / shared / Aurora, Odyssey | Common texture payloads and texture metadata |
| [UTC](GFF-Creature-and-Dialogue#utc) / [UTI](GFF-Items-and-Economy#uti) / [UTP](GFF-Spatial-Objects#utp) / [UTD](GFF-Spatial-Objects#utd) / [UTM](GFF-Items-and-Economy#utm) / [UTW](GFF-Spatial-Objects#utw) | `0x07EB` / `0x07E9` / `0x07FC` / `0x07FA` / `0x0803` / `0x080A` | GFF | Aurora, Odyssey | Creature, item, placeable, door, merchant, and waypoint templates |
| [WOK](Level-Layout-Formats#bwm) / [DWK](Level-Layout-Formats#bwm) / [PWK](Level-Layout-Formats#bwm) / `BWM` | `0x07E0` / `0x0804` / `0x0805` / `3005` | binary | Aurora, Odyssey / Odyssey | Walkmesh family for areas, doors, placeables, and Odyssey binary walkmesh assets |

The practical split is simple: most modders live in GFF resources, 2DA tables, scripts, talk tables, and models/textures, while engine and tool authors also need the Odyssey-specific `3000+` block because that is where layout, visibility, binary walkmesh, texture-container, and MDX sidecar types are declared [[`ResourceType` 2000-2063 block](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L239-L307), [`ResourceType` 3000-3028 block](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L411-L479)].

### Odyssey extension block (`3000+`)

These IDs are the biggest omission in many older KotOR summaries because they sit outside the classic Aurora range. In practice they cover exactly the kinds of assets that make Odyssey areas, rooms, visibility, lips, and texture/model sidecars work.

| Extension | Type ID | Contents | Typical KotOR role |
| --------- | ------- | -------- | ------------------ |
| [LYT](Level-Layout-Formats#lyt) | `3000` | plaintext | Area room/layout mapping |
| [VIS](Level-Layout-Formats#vis) | `3001` | plaintext | Room-to-room visibility graph |
| [RIM](Container-Formats#rim) | `3002` | binary container | Odyssey area/archive container |
| [PTH](GFF-Spatial-Objects#pth) | `3003` | GFF | Path and waypoint-network data |
| [LIP](Audio-and-Localization-Formats#lip) | `3004` | lips | Lip-sync timing |
| `bwm` | `3005` | binary | Odyssey binary walkmesh |
| `txb` | `3006` | binary | Texture-related Odyssey helper type retained in the registry |
| [TPC](Texture-Formats#tpc) | `3007` | binary | Primary Odyssey texture container |
| [MDX](MDL-MDX-File-Format) | `3008` | binary | Model mesh/geometry sidecar |
| `rsv` / `sig` | `3009` / `3010` | binary | Registry placeholder Odyssey IDs with no current documented KotOR usage |
| `mab` | `3011` | binary | Material-related binary type |
| `qst2` / `sto` | `3012` / `3013` | GFF | Odyssey quest/store-adjacent data types retained in the registry |
| `hex` | `3015` | binary | Hex-grid related helper type |
| `mdx2` / `txb2` | `3016` / `3017` | binary | Secondary model/texture helper types |
| `fsm` / `art` / `amp` / `cwa` | `3022` / `3023` / `3024` / `3025` | binary / plaintext / binary / GFF | State-machine, area-environment, brightness, and crowd-attribute helpers |
| `bip` | `3028` | lips | Binary lip-sync companion type |

All of those entries are declared as Odyssey-supported in the current registry, even when only a smaller subset is encountered in normal KotOR mod distribution workflows [[`LYT` through `BIP`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L411-L479)].

### Legacy and cross-engine IDs that still matter in KotOR tooling

Some registry members survive because KotOR shares lineage with broader Aurora/Odyssey tooling, not because every title uses them equally. The most relevant examples are `BMU`, `MPG`, `WMA`, `WMV`, and `XMV` for audio/video payload families; `HAK` and `NWM` from Aurora container history; and `BIK` for Bink video. They are worth keeping documented because extraction tools, archive browsers, and cross-engine libraries need one registry that can reason about both KotOR and its neighboring BioWare formats [[`BMU`-`XMV`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L231-L238), [`HAK`-`BIK`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L303-L307), [xoreos 0.0.6 release notes](https://xoreos.org/blog/2020/08/03/xoreos-0-dot-0-6-elanee-released/)].

### Extended classic registry table

All entries derive from PyKotor's [`ResourceType` enum in `type.py`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py); each member's `supported_engines` field is the authoritative source for engine support [[`BiowareEngine`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L49-L67), [`ResourceType` members L209-L480](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L209-L480)]. Rows described as having "no known retail game files" are engine-registered types not observed in shipped KotOR archives.

| Resource Name | Type ID | Description                                    |
| ------------- | ------- | ---------------------------------------------- |
| [RES](GFF-File-Format)           | 0x0000  | Used for `.res` resources within the [save game containers](Container-Formats#erf)                     |
| BMP           | 0x0001  | Bitmap image                         |
| MVE           | 0x0002  | Movie/video file; Infinity-engine only — not present in KotOR [[`MVE`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L215-L216)] |
| [TGA](https://en.wikipedia.org/wiki/Truevision_TGA)           | 0x0003  | TarGA image format                          |
| [WAV](Audio-and-Localization-Formats#wav)           | 0x0004  | Wave audio file (see [WAV File Format](Audio-and-Localization-Formats#wav)) |
| [INI](https://en.wikipedia.org/wiki/INI_file)           | 0x0007  | Configuration file (e.g., `swkotor.ini`, `swkotor2.ini`)                          |
| [BMU](Audio-and-Localization-Formats)           | 0x0008  | Odyssey audio payload family; TSL commonly treats these as music-like assets rather than generic unknown data [[`BMU`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L231)]                                |
| [MPG](Audio-and-Localization-Formats)           | 0x0009  | MPEG video/audio-adjacent payload retained in the Odyssey registry [[`MPG`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L232)]                            |
| [TXT](https://en.wikipedia.org/wiki/Text_file)           | 0x000A  | Text file                                  |
| [WMA](Audio-and-Localization-Formats)           | 0x000B  | Windows Media Audio; retained as an Odyssey-supported registry type [[`WMA`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L236)] |
| [WMV](Audio-and-Localization-Formats)           | 0x000C  | Windows Media Video; retained as an Odyssey-supported registry type [[`WMV`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L237)] |
| [XMV](Audio-and-Localization-Formats)           | 0x000D  | Xbox media/video type retained as an Odyssey-supported registry type [[`XMV`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L238)] |
| PLH           | 0x07D0  | Placeable header type; Odyssey-registered though no known retail KotOR game files of this type are shipped [[`PLH`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L239)] |
| TEX           | 0x07D1  | Texture type; Odyssey-registered though no known retail KotOR game files of this type are shipped [[`TEX`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L240)] |
| [MDL](MDL-MDX-File-Format)           | 0x07D2  | 3D [model](MDL-MDX-File-Format) file (see [MDL/MDX File Format](MDL-MDX-File-Format))                                   |
| THG           | 0x07D3  | Unknown Odyssey-registered type; no known usage [[`THG`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L242)] |
| FNT           | 0x07D5  | Font file; Odyssey-registered though no known retail KotOR game files of this type are shipped [[`FNT`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L244)] |
| [Lua](https://www.lua.org/)           | 0x07D7  | Lua script source; Odyssey/Eclipse-registered though no known retail KotOR game files of this type are shipped [[`LUA`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L246)] |
| SLT           | 0x07D8  | Unknown Odyssey-registered type; no known usage [[`SLT`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L247)] |
| [NSS](NSS-File-Format)           | 0x07D9  | *NWScript* source code (see [NSS File Format](NSS-File-Format))                            |
| [NCS](NCS-File-Format)           | 0x07DA  | *Compiled NWScript* bytecode (see [NCS File Format](NCS-File-Format))                     |
| [MOD](Container-Formats#erf)           | 0x07DB  | [*Module* ERF archive/container](Container-Formats#erf)                         |
| [ARE](GFF-File-Format#are-area)           | 0x07DC  | *Area* definition (see [GFF-ARE](GFF-Module-and-Area#are))                                 |
| SET           | 0x07DD  | Tileset; Odyssey-registered though no known retail KotOR game files of this type are shipped [[`SET`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L252)] |
| [IFO](GFF-File-Format#ifo-module-info)           | 0x07DE  | *Module* InFOrmation (see [GFF-IFO](GFF-Module-and-Area#ifo))                              |
| BIC          | 0x07DF  | Character export data (GFF format); used in Aurora/Odyssey character exports and some save workflows [[`BIC`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L254)] |
| [WOK](Level-Layout-Formats#bwm)           | 0x07E0  | *Walkmesh* (see [BWM File Format](Level-Layout-Formats#bwm))                                |
| [2DA](2DA-File-Format)           | 0x07E1  | *Two-Dimensional Array* data (see [2DA File Format](2DA-File-Format))                      |
| [TLK](Audio-and-Localization-Formats#tlk)           | 0x07E2  | *Talk Table* (Localized Strings, see [TLK File Format](Audio-and-Localization-Formats#tlk))                 |
| [TXI](Texture-Formats#txi)           | 0x07E6  | [TeXture Information](Texture-Formats#txi)                            |
| [GIT](GFF-File-Format#git-game-instance-template)           | 0x07E7  | [Game Instance Template](GFF-File-Format#git-game-instance-template) (see [GFF-GIT](GFF-Module-and-Area#git))                          |
| [BTI](GFF-File-Format#bti-item-template--bioware)           | 0x07E8  | Blueprint Template Item. *KotOR* supports these but nobody uses them, use [UTI](GFF-Items-and-Economy#uti) instead.                 |
| [UTI](GFF-File-Format#uti-item)           | 0x07E9  | [item templates](GFF-File-Format#uti-item) (see [GFF-UTI](GFF-Items-and-Economy#uti))                                   |
| [BTC](GFF-File-Format#btc-creature-template--bioware)           | 0x07EA  | Blueprint Template Creature. *KotOR* supports these but nobody uses them, use [UTC](GFF-Creature-and-Dialogue#utc) instead.                |
| [UTC](GFF-File-Format#utc-creature)           | 0x07EB  | [Creature Template](GFF-File-Format#utc-creature) (see [GFF-UTC](GFF-Creature-and-Dialogue#utc))                               |
| [DLG](GFF-File-Format#dlg-dialogue)           | 0x07ED  | Dialogue/conversation (see [GFF-DLG](GFF-Creature-and-Dialogue#dlg))                           |
| [ITP](Bioware-Aurora-Module-and-Area#paletteitp)           | 0x07EE  | *ITP* format (see [Bioware-Aurora-PaletteITP](Bioware-Aurora-Module-and-Area#paletteitp)).                         |
| [BTT](GFF-File-Format#btt-trigger-template--bioware)           | 0x07EF  | *Blueprint Template Trigger*. *KotOR* supports these but nobody uses them, use [UTT](GFF-Spatial-Objects#utt) instead.                 |
| [UTT](GFF-File-Format#utt-trigger)           | 0x07F0  | *Trigger Template* (see [GFF-UTT](GFF-Spatial-Objects#utt)).                                |
| [DDS](Texture-Formats#dds)           | 0x07F1  | *DirectDraw Surface Texture* (see [DDS File Format](Texture-Formats#dds)).                                |
| [BTS](GFF-File-Format)           | 0x07F2  | Sound template (BioWare), GFF (`bts` extension). BioWare-authored sound blueprint counterpart to the user-created [`uts`](GFF-Spatial-Objects#uts). |
| [UTS](GFF-File-Format#uts-sound)           | 0x07F3  | *Sound Template* (see [GFF-UTS](GFF-Spatial-Objects#uts)).                                |
| [LTR](LTR-File-Format)           | 0x07F4  | *Letter Format* (see [LTR File Format](LTR-File-Format)). Not used in *KotOR*                                |
| [GFF](GFF-File-Format)           | 0x07F5  | Generic file format (container, see [GFF File Format](GFF-File-Format))                 |
| [FAC](GFF-File-Format#fac-faction)           | 0x07F6  | [Faction](GFF-File-Format#fac-faction)                               |
| [BTE](GFF-File-Format#bte-encounter-template--bioware)           | 0x07F7  | Blueprint encounter                   |
| [UTE](GFF-File-Format#ute-encounter)           | 0x07F8  | [Encounter Template](GFF-File-Format#ute-encounter) (see [GFF-UTE](GFF-Spatial-Objects#ute))                              |
| [BTD](GFF-File-Format#btd-door-template--bioware)           | 0x07F9  | Door template (BioWare), GFF. Rarely used directly; [`utd`](GFF-Spatial-Objects#utd) is the modder-facing equivalent. |
| [UTD](GFF-File-Format#utd-door)           | 0x07FA  | [Door Template](GFF-File-Format#utd-door) (see [GFF-UTD](GFF-Spatial-Objects#utd))                                   |
| [BTP](GFF-File-Format#btp-placeable-template--bioware)           | 0x07FB  | Blueprint placeable   Not used in *KotOR*  |
| [UTP](GFF-File-Format#utp-placeable)           | 0x07FC  | [Placeable Template](GFF-File-Format#utp-placeable) (see [GFF-UTP](GFF-Spatial-Objects#utp))                              |
| DTF / DFT     | 0x07FD  | Default value file, INI format (`.dtf` / `.dft` extension). Used by area properties dialogs in the Aurora toolset. Not needed directly by modders. |
| GIC           | 0x07FE  | Game instance comments, GFF. Toolset-only — instance labels are stored in `.gic` separately from runtime `.git` data. Not processed by the game engine itself. |
| [GUI](GFF-File-Format#gui-graphical-user-interface)           | 0x07FF  | User interface definition (see [GFF-GUI](GFF-GUI))                       |
| CSS           | 0x0800  | Conditional source script. Not used at runtime in *KotOR*. |
| CCS           | 0x0801  | Conditional compiled script. Not used at runtime in *KotOR*. |
| [BTM](GFF-File-Format#btm-merchant-template--bioware)           | 0x0802  | Blueprint merchant.  *KotOR* supports these but nobody uses them, use [UTM](GFF-Items-and-Economy#utm) instead.              |
| [UTM](GFF-File-Format#utm-merchant)           | 0x0803  | [Merchant/store template](GFF-File-Format#utm-merchant) (see [GFF-UTM](GFF-Items-and-Economy#utm))                         |
| [DWK](Level-Layout-Formats#bwm)           | 0x0804  | [Door walkmesh](Level-Layout-Formats#bwm) (see [BWM File Format](Level-Layout-Formats#bwm))                                |
| [PWK](Level-Layout-Formats#bwm)           | 0x0805  | [Placeable walkmesh](Level-Layout-Formats#bwm) (see [BWM File Format](Level-Layout-Formats#bwm))                                |
| [BTG](GFF-File-Format#btg-random-item-generator--bioware)           | 0x0806  | Random item generator template (BioWare), GFF. |
| [UTG](GFF-File-Format#utg-random-item-generator)           | 0x0807  | Random item generator template (user), GFF. |
| [JRL](GFF-File-Format#jrl-journal)           | 0x0808  | Journal/quest log (see [GFF-JRL](GFF-Items-and-Economy#jrl))                               |
| [SAV](Container-Formats#erf)           | 0x0809  | [Save Game Containers](Container-Formats#erf) (see [ERF File Format](Container-Formats#erf))                               |
| [UTW](GFF-File-Format#utw-waypoint)           | 0x080A  | [Waypoint Template](GFF-File-Format#utw-waypoint)                               |
| 4PC           | 0x080B  | Texture, custom 16-bit RGBA palette format. Odyssey-only type. |
| [SSF](Audio-and-Localization-Formats#ssf)           | 0x080C  | [Sound Set Files](Audio-and-Localization-Formats#ssf) (see [SSF File Format](Audio-and-Localization-Formats#ssf))                                  |
| HAK           | 0x080D  | Hak pak container. Not used in *KotOR*                                |
| NWM           | 0x080E  | *Neverwinter Nights* module (Not used in *KotOR*)                                 |
| [BIK](https://en.wikipedia.org/wiki/Bink_(video_codec))           | 0x080F  | BInK video format                                |
| NDB           | 0x0810  | Script debugger file. Generated by the *Aurora* toolset debugger; not used by the game engine. |
| PTM           | 0x0811  | Plot instance/manager, GFF. |
| PTT           | 0x0812  | Plot wizard blueprint, GFF. |
| NCM           | 0x0813  | Registry placeholder type with no current documented BioWare usage. |
| MFX           | 0x0814  | Registry placeholder type with no current documented BioWare usage. |
| MAT           | 0x0815  | Material file. Used in later BioWare titles; not present in *KotOR*. |
| MDB           | 0x0816  | BioWare geometry model (`.mdb`). Used in NWN2 / Dragon Age; not present in *KotOR*. |
| SAY           | 0x0817  | Registry placeholder type with no current documented BioWare usage. |
| [TTF](https://en.wikipedia.org/wiki/TrueType)           | 0x0818  | TrueType font (`.ttf`). Used in some BioWare titles; not present in *KotOR*. |
| TTC           | 0x0819  | Registry placeholder type with no current documented BioWare usage. |
| CUT           | 0x081A  | Cutscene, GFF. Not present in *KotOR*. |
| KA            | 0x081B  | Karma data, XML format. Not present in *KotOR*. |
| [JPG](https://en.wikipedia.org/wiki/JPEG)           | 0x081C  | JPEG image. Eclipse engine only (Dragon Age). |
| [ICO](https://en.wikipedia.org/wiki/ICO_(file_format))           | 0x081D  | Windows icon format. Eclipse engine only (Dragon Age). |
| [OGG](https://en.wikipedia.org/wiki/Ogg)           | 0x081E  | Audio, Ogg Vorbis. Eclipse engine only (Dragon Age). |
| SPT           | 0x081F  | Tree data, SpeedTree format. Not present in *KotOR*. |
| SPW           | 0x0820  | Registry placeholder type with no current documented BioWare usage. |
| WFX           | 0x0821  | Woot effect class, XML format. Not present in *KotOR*. |
| UGM           | 0x0822  | Registry placeholder type with no current documented BioWare usage. |
| QDB           | 0x0823  | Quest database, GFF. Not present in *KotOR*. |
| QST           | 0x0824  | Quest, GFF. Not present in *KotOR*. |
| NPC           | 0x0825  | Registry placeholder type with no current documented BioWare usage. |
| SPN           | 0x0826  | Registry placeholder type with no current documented BioWare usage. |
| UTX           | 0x0827  | Registry placeholder type with no current documented BioWare usage. |
| MMD           | 0x0828  | Registry placeholder type with no current documented BioWare usage. |
| SMM           | 0x0829  | Registry placeholder type with no current documented BioWare usage. |
| UTA           | 0x082A  | Registry placeholder type with no current documented BioWare usage. |
| MDE           | 0x082B  | Registry placeholder type with no current documented BioWare usage. |
| MDV           | 0x082C  | Registry placeholder type with no current documented BioWare usage. |
| MDA           | 0x082D  | Registry placeholder type with no current documented BioWare usage. |
| MBA           | 0x082E  | Registry placeholder type with no current documented BioWare usage. |
| OCT           | 0x082F  | Registry placeholder type with no current documented BioWare usage. |
| BFX           | 0x0830  | Registry placeholder type with no current documented BioWare usage. |
| PDB           | 0x0831  | Registry placeholder type with no current documented BioWare usage. |
| TheWitcherSave | 0x0832 | The Witcher save file. Non-BioWare game; tracked in xoreos type registry. |
| PVS           | 0x0833  | Registry placeholder type with no current documented BioWare usage. |
| CFX           | 0x0834  | Registry placeholder type with no current documented BioWare usage. |
| LUC           | 0x0835  | Script, LUA bytecode. Eclipse engine only (Dragon Age). |
| *(reserved)*  | 0x0836  | Type ID 2102 is reserved/skipped in the xoreos registry. |
| PRB           | 0x0837  | Registry placeholder type with no current documented BioWare usage. |
| CAM           | 0x0838  | Campaign information, Aurora engine only. Not present in *KotOR*. |
| VDS           | 0x0839  | Registry placeholder type with no current documented BioWare usage. |
| BIN           | 0x083A  | Registry placeholder type with no current documented BioWare usage. |
| WOB           | 0x083B  | Registry placeholder type with no current documented BioWare usage. |
| API           | 0x083C  | Registry placeholder type with no current documented BioWare usage. |
| Properties    | 0x083D  | Registry placeholder type for the `.properties` extension, with no current documented BioWare usage. |
| [PNG](https://en.wikipedia.org/wiki/Portable_Network_Graphics)           | 0x083E  | PNG image. Odyssey and Eclipse engine support. |
| [ERF](Container-Formats#erf)           | 0x270D  | [Encapsulated Resource File](Container-Formats#erf) (see [ERF File Format](Container-Formats#erf))                      |
| [BIF](Container-Formats#bif)           | 0x270E  | [Bioware Index File](Container-Formats#bif) (container, see [BIF File Format](Container-Formats#bif))                    |
| [KEY](Container-Formats#key)           | 0x270F  | [KEY](Container-Formats#key) table ([BIF](Container-Formats#bif) index, see [KEY File Format](Container-Formats#key))                          |

For KotOR specifically, do not stop reading at `0x270F`: the Odyssey-only `3000+` block above is part of the real resource landscape and includes some of the most important room/layout/visibility/model-sidecar types in the games [[`LYT` through `BIP`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/type.py#L411-L479)].

## File format index

### File formats

- **[MDL/MDX File Format](MDL-MDX-File-Format)** ← Complete reference for 3D [model](MDL-MDX-File-Format) files
- **[2DA File Format](2DA-File-Format)** ← Complete reference for Two-Dimensional array format (see also [Official Bioware 2DA Documentation](Bioware-Aurora-Core-Formats#2da)). All individual 2DA file documentation has been inlined into this document.
  - **K1 and TSL**
    - [acbonus.2da](2DA-File-Format#acbonus2da)
    - [ambientmusic.2da](2DA-File-Format#ambientmusic2da)
    - [ambientsound.2da](2DA-File-Format#ambientsound2da)
    - [ammunitiontypes.2da](2DA-File-Format#ammunitiontypes2da)
    - [animations.2da](2DA-File-Format#animations2da)
    - [appearance.2da](2DA-File-Format#appearance2da)
    - [appearancesndset.2da](2DA-File-Format#appearancesndset2da)
    - [baseitems.2da](2DA-File-Format#baseitems2da)
    - [bindablekeys.2da](2DA-File-Format#bindablekeys2da)
    - [bodybag.2da](2DA-File-Format#bodybag2da)
    - [camerastyle.2da](2DA-File-Format#camerastyle2da)
    - [classes.2da](2DA-File-Format#classes2da)
    - [classpowergain.2da](2DA-File-Format#classpowergain2da)
    - [combatanimations.2da](2DA-File-Format#combatanimations2da)
    - [creaturespeed.2da](2DA-File-Format#creaturespeed2da)
    - [cursors.2da](2DA-File-Format#cursors2da)
    - [dialoganimations.2da](2DA-File-Format#dialoganimations2da)
    - [difficultyopt.2da](2DA-File-Format#difficultyopt2da)
    - [disease.2da](2DA-File-Format#disease2da)
    - [doortypes.2da](2DA-File-Format#doortypes2da)
    - [droiddischarge.2da](2DA-File-Format#droiddischarge2da)
    - [effecticon.2da](2DA-File-Format#effecticon2da)
    - [encdifficulty.2da](2DA-File-Format#encdifficulty2da)
    - [exptable.2da](2DA-File-Format#exptable2da)
    - [feat.2da](2DA-File-Format#feat2da)
    - [featgain.2da](2DA-File-Format#featgain2da)
    - [feedbacktext.2da](2DA-File-Format#feedbacktext2da)
    - [footstepsounds.2da](2DA-File-Format#footstepsounds2da)
    - [forceshields.2da](2DA-File-Format#forceshields2da)
    - [fractionalcr.2da](2DA-File-Format#fractionalcr2da)
    - [gender.2da](2DA-File-Format#gender2da)
    - [genericdoors.2da](2DA-File-Format#genericdoors2da)
    - [globalcat.2da](2DA-File-Format#globalcat2da)
    - [grenadesnd.2da](2DA-File-Format#grenadesnd2da)
    - [guisounds.2da](2DA-File-Format#guisounds2da)
    - [heads.2da](2DA-File-Format#heads2da)
    - [inventorysnds.2da](2DA-File-Format#inventorysnds2da)
    - [iprp_abilities.2da](2DA-File-Format#iprp_abilities2da)
    - [iprp_acmodtype.2da](2DA-File-Format#iprp_acmodtype2da)
    - [iprp_aligngrp.2da](2DA-File-Format#iprp_aligngrp2da)
    - [iprp_ammotype.2da](2DA-File-Format#iprp_ammotype2da)
    - [iprp_combatdam.2da](2DA-File-Format#iprp_combatdam2da)
    - [iprp_costtable.2da](2DA-File-Format#iprp_costtable2da)
    - [iprp_damagecost.2da](2DA-File-Format#iprp_damagecost2da)
    - [iprp_damagetype.2da](2DA-File-Format#iprp_damagetype2da)
    - [iprp_immunity.2da](2DA-File-Format#iprp_immunity2da)
    - [iprp_lightcol.2da](2DA-File-Format#iprp_lightcol2da)
    - [iprp_monstdam.2da](2DA-File-Format#iprp_monstdam2da)
    - [iprp_mosterhit.2da](2DA-File-Format#iprp_mosterhit2da)
    - [iprp_onhit.2da](2DA-File-Format#iprp_onhit2da)
    - [iprp_paramtable.2da](2DA-File-Format#iprp_paramtable2da)
    - [iprp_protection.2da](2DA-File-Format#iprp_protection2da)
    - [iprp_saveelement.2da](2DA-File-Format#iprp_saveelement2da)
    - [iprp_savingthrow.2da](2DA-File-Format#iprp_savingthrow2da)
    - [iprp_walk.2da](2DA-File-Format#iprp_walk2da)
    - [itempropdef.2da](2DA-File-Format#itempropdef2da)
    - [itemprops.2da](2DA-File-Format#itemprops2da)
    - [keymap.2da](2DA-File-Format#keymap2da)
    - [loadscreenhints.2da](2DA-File-Format#loadscreenhints2da)
    - [loadscreens.2da](2DA-File-Format#loadscreens2da)
    - [masterfeats.2da](2DA-File-Format#masterfeats2da)
    - [modulesave.2da](2DA-File-Format#modulesave2da)
    - [movies.2da](2DA-File-Format#movies2da)
    - [placeableobjsnds.2da](2DA-File-Format#placeableobjsnds2da)
    - [placeables.2da](2DA-File-Format#placeables2da)
    - [planetary.2da](2DA-File-Format#planetary2da)
    - [plot.2da](2DA-File-Format#plot2da)
    - [poison.2da](2DA-File-Format#poison2da)
    - [portraits.2da](2DA-File-Format#portraits2da)
    - [prioritygroups.2da](2DA-File-Format#prioritygroups2da)
    - [racialtypes.2da](2DA-File-Format#racialtypes2da)
    - [ranges.2da](2DA-File-Format#ranges2da)
    - [regeneration.2da](2DA-File-Format#regeneration2da)
    - [repute.2da](2DA-File-Format#repute2da)
    - [skills.2da](2DA-File-Format#skills2da)
    - [spells.2da](2DA-File-Format#spells2da)
    - [stringtokens.2da](2DA-File-Format#stringtokens2da)
    - [surfacemat.2da](2DA-File-Format#surfacemat2da)
    - [texpacks.2da](2DA-File-Format#texpacks2da)
    - [traps.2da](2DA-File-Format#traps2da)
    - [tutorial.2da](2DA-File-Format#tutorial2da)
    - [upgrade.2da](2DA-File-Format#upgrade2da)
    - [videoeffects.2da](2DA-File-Format#videoeffects2da)
    - [visualeffects.2da](2DA-File-Format#visualeffects2da)
    - [weaponsounds.2da](2DA-File-Format#weaponsounds2da)
    - [xptable.2da](2DA-File-Format#xptable2da)
  - **TSL only**
    - [emotion.2da](2DA-File-Format#emotion2da)
    - [facialanim.2da](2DA-File-Format#facialanim2da)
    - [pazaakdecks.2da](2DA-File-Format#pazaakdecks2da)
    - [soundset.2da](2DA-File-Format#soundset2da)
    - [subrace.2da](2DA-File-Format#subrace2da)
    - [upcrystals.2da](2DA-File-Format#upcrystals2da)
- **[TLK File Format](Audio-and-Localization-Formats#tlk)** ← Complete reference for [Talk Table](Audio-and-Localization-Formats#tlk) format
- [BIF File Format](Container-Formats#bif) ← BioWare Infinity format
- [KEY File Format](Container-Formats#key) ← [KEY](Container-Formats#key) file format
- **[BWM File Format](Level-Layout-Formats#bwm)** ← Complete reference for Binary [walkmesh](Level-Layout-Formats#bwm) format
- **[GUI File Format](GFF-GUI)** ← Complete reference for Graphical User Interface format
- [ERF File Format](Container-Formats#erf) ← Encapsulated Resource format (MOD, SAV, HAK; [RIM comparison](Container-Formats#rim-versus-erf))
- **[Kit Structure Documentation](Kit-Structure-Documentation)** ← Complete reference for indoor kit structure and generation
- [GFF File Format](GFF-File-Format) ← Generic file Format (see also [Official Bioware GFF Documentation](Bioware-Aurora-Core-Formats#gff))
  - [ARE (Area)](GFF-Module-and-Area#are)
  - [DLG (Dialogue)](GFF-Creature-and-Dialogue#dlg)
  - [GIT (Game Instance Template)](GFF-Module-and-Area#git)
  - [GUI (Graphical User Interface)](GFF-GUI)
  - [IFO (Module Info)](GFF-Module-and-Area#ifo)
  - [JRL (Journal)](GFF-Items-and-Economy#jrl)
  - [PTH (Path)](GFF-Spatial-Objects#pth)
  - [UTC (Creature)](GFF-Creature-and-Dialogue#utc)
  - [UTD (Door)](GFF-Spatial-Objects#utd)
  - [UTE (Encounter)](GFF-Spatial-Objects#ute)
  - [UTI (Item)](GFF-Items-and-Economy#uti)
  - [UTM (Merchant)](GFF-Items-and-Economy#utm)
  - [UTP (Placeable)](GFF-Spatial-Objects#utp)
  - [UTS (Sound)](GFF-Spatial-Objects#uts)
  - [UTT (Trigger)](GFF-Spatial-Objects#utt)
  - [UTW (Waypoint)](GFF-Spatial-Objects#utw)
- [DDS File Format](Texture-Formats#dds) ← DirectDraw Surface texture format
- [LIP File Format](Audio-and-Localization-Formats#lip) ← [LIP](Audio-and-Localization-Formats#lip) sync format
- [LTR File Format](LTR-File-Format) ← [Letter](LTR-File-Format) format
- [LYT File Format](Level-Layout-Formats#lyt) ← [Layout](Level-Layout-Formats#lyt) format
- [NCS File Format](NCS-File-Format) ← [NwScript Compiled Script](NCS-File-Format) format
- [NSS File Format](NSS-File-Format) ← [NwScript Source](NSS-File-Format) format (*nwscript.nss*, function/constant definitions)
- [RIM File Format](Container-Formats#rim) ← [Resource Image](Container-Formats#rim) format
- [SSF File Format](Audio-and-Localization-Formats#ssf) ← [Sound Set Files](Audio-and-Localization-Formats#ssf) format
- [TPC File Format](Texture-Formats#tpc) ← [Texture Pack Container](Texture-Formats#tpc) format
- [TXI File Format](Texture-Formats#txi) ← [Texture Info](Texture-Formats#txi) format
- [VIS File Format](Level-Layout-Formats#vis) ← [Visibility](Level-Layout-Formats#vis) format
- [WAV File Format](Audio-and-Localization-Formats#wav) ← [Wave](Audio-and-Localization-Formats#wav) audio format

### See also

- [Concepts](Concepts) — Override, BIF/KEY, MOD/ERF/RIM, GFF, 2DA, language IDs
- [Container-Formats#key](Container-Formats#key) — KEY binary layout and index role
- [Mod-Creation-Best-Practices](Mod-Creation-Best-Practices#file-priority-and-where-to-put-your-files) — Where to install files
- [Home](Home) — Wiki hub
- [Reverse Engineering Findings — Resource Management System](reverse_engineering_findings#resource-management-system) — Engine `CExoResMan` / resource loading (conceptual)
