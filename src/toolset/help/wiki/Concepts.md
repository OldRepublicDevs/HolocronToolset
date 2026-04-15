# Concepts

This page is limited to concepts that can be stated directly from PyKotor source and from recovered Odyssey-family engine routines in three binaries: KotOR I, KotOR II, and Aurora `nwmain.exe`. [[PyKotor `SearchLocation`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/installation.py#L67-L104), [PyKotor `ResRef`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/common/misc.py#L24-L55), [PyKotor `LocalizedString`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/common/language.py#L624-L775)]

## Resource identity and lookup

Odyssey lookups are keyed by a resource identity, not by an arbitrary filesystem path: the request is a **ResRef plus resource type**, and PyKotor normalizes user-facing queries into that pair before dispatching them through its installation search API. [[PyKotor `ResRef`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/common/misc.py#L24-L55), [PyKotor `location()` normalization](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/installation.py#L1727-L1794)]

PyKotor exposes the effective lookup layers as `OVERRIDE`, `MODULES`, and `CHITIN`, and its CHITIN handler explicitly checks `self._chitin` and `self._patch_erf` in the same fallback branch. [[PyKotor `SearchLocation`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/installation.py#L67-L104), [PyKotor CHITIN fallback lambda](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/installation.py#L1976-L1985)]

The recovered engine code matches the same broad design while exposing different amounts of naming detail. `CExoResMan::Exists @ (/K1/k1_win_gog_swkotor.exe @ 0x00408bc0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x0061b830, /Other BioWare Engines/Aurora/nwmain.exe @ 0x14018f590)` is the public existence probe in all three binaries, and `CExoKeyTable::RebuildTable @ (/K1/k1_win_gog_swkotor.exe @ 0x00410260, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x006304a0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x14018ccf0)` shows that keyed archive data is maintained as resident lookup tables rather than reopened raw on every request.

The main discrepancy is symbol visibility, not behavior. Aurora preserves the override probe by name inside `CExoResMan::Exists` via `GetOverride` followed by per-table `FindKey` calls, while K1 and TSL recover shorter x86 front ends that hide more of the same table walk behind unnamed or less descriptive helpers. `CExoResMan::Exists @ (/K1/k1_win_gog_swkotor.exe @ 0x00408bc0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x0061b830, /Other BioWare Engines/Aurora/nwmain.exe @ 0x14018f590)`

The current three-binary pass does not recover a separately named module-capsule probe with the same clarity as Aurora's `GetOverride`, so the exact **override -> modules -> CHITIN** ordering on this page is stated from PyKotor's explicit search model, while the reverse-engineered evidence here directly anchors the override and keyed-table portions of the chain. [[PyKotor `SearchLocation`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/installation.py#L67-L104), [PyKotor `locations()` dispatch](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/installation.py#L1976-L2009)] `CExoResMan::Exists @ (/K1/k1_win_gog_swkotor.exe @ 0x00408bc0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x0061b830, /Other BioWare Engines/Aurora/nwmain.exe @ 0x14018f590)`

## ResRef

A **ResRef** is the resource stem: PyKotor treats it as ASCII, compares it case-insensitively, trims whitespace, and caps it at 16 characters. [[PyKotor `ResRef`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/common/misc.py#L24-L55)]

The binary GFF read path shows the same concept at storage level. `CResGFF::ReadFieldCResRef @ (/K1/k1_win_gog_swkotor.exe @ 0x00411e10, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00624fa0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a12d0)` checks for field type `0xb`, validates the field payload, reads a leading byte length, and then initializes a `CResRef` from the following bytes.

The implementation differences are mechanical rather than semantic. K1 and TSL inline most of the byte-count checks in x86 and then hand the payload to a `CResRef` constructor, while Aurora's x64 build performs the same type and bounds checks but reaches a named terminal routine, `InitFromCharArray`, before returning the decoded `CResRef`. `CResGFF::ReadFieldCResRef @ (/K1/k1_win_gog_swkotor.exe @ 0x00411e10, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00624fa0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a12d0)`

That is why override conflicts are collisions on **ResRef + type**, not just on extension text. The engine-side existence probe and the GFF-side ResRef reader both operate on that paired identity rather than on free-form filenames. [[PyKotor `location()` normalization](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/installation.py#L1727-L1794)] `CExoResMan::Exists @ (/K1/k1_win_gog_swkotor.exe @ 0x00408bc0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x0061b830, /Other BioWare Engines/Aurora/nwmain.exe @ 0x14018f590)` `CResGFF::ReadFieldCResRef @ (/K1/k1_win_gog_swkotor.exe @ 0x00411e10, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00624fa0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a12d0)`

## Localized strings

PyKotor models a localized string as a `stringref` plus zero or more inline substrings keyed by `substring_id = language * 2 + gender`, with `substring_pair()` performing the inverse mapping during reads. [[PyKotor `LocalizedString` mapping](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/common/language.py#L624-L775), [PyKotor `read_locstring()`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/utility/common/stream.py#L822-L840), [PyKotor `write_locstring()`](https://github.com/OpenKotOR/PyKotor/blob/master/Libraries/PyKotor/src/utility/common/stream.py#L1728-L1738)]

The recovered GFF readers follow the same counted structure in all three binaries. `CResGFF::ReadFieldCExoLocString @ (/K1/k1_win_gog_swkotor.exe @ 0x00411fd0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00625240, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a0f80)` constructs a `CExoLocString`, reads the serialized record set, and appends substrings one entry at a time.

The main binary difference is again visibility. K1 and Aurora expose `AddString` directly in the recovered call graph for `CResGFF::ReadFieldCExoLocString`, while TSL keeps the same loop shape inside a larger x86 routine with fewer recovered helper names. `CResGFF::ReadFieldCExoLocString @ (/K1/k1_win_gog_swkotor.exe @ 0x00411fd0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x00625240, /Other BioWare Engines/Aurora/nwmain.exe @ 0x1401a0f80)`

Selection of text from a localized string also stays structurally consistent across binaries. `CExoLocString::GetString @ (/K1/k1_win_gog_swkotor.exe @ 0x005ea130, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x006077c0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x140169920)` first attempts a direct substring lookup from the computed string id and then takes a fallback path when inline text is missing.

Aurora's recovered signature exposes that fallback path more clearly than the KotOR builds: its named const overload includes an extra boolean parameter, while the K1 and TSL x86 variants recover temporary `CExoString` and `CResRef` setup around the same failure-handling path. `CExoLocString::GetString @ (/K1/k1_win_gog_swkotor.exe @ 0x005ea130, /TSL/k2_win_gog_aspyr_swkotor2.exe @ 0x006077c0, /Other BioWare Engines/Aurora/nwmain.exe @ 0x140169920)`

## See also

- [Resource-Formats-and-Resolution](Resource-Formats-and-Resolution) -- resource-type table and broader format index
- [Container-Formats](Container-Formats) -- KEY, BIF, ERF, MOD, RIM, and capsule details
- [GFF-File-Format](GFF-File-Format) -- field types, structs, lists, and file families
- [Audio-and-Localization-Formats](Audio-and-Localization-Formats) -- TLK, SSF, LIP, and localization containers
- [Installing-Mods-with-HoloPatcher](Installing-Mods-with-HoloPatcher) -- player-facing installation workflow
