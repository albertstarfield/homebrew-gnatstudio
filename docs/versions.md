# GNAT Studio version directories

The macOS binaries are not on the AdaCore GitHub release. They are published by the gnuada project on SourceForge, one directory per release generation. The parent listing is copied at `../evidence/sf-macosx-parent.html:2151`.

| SourceForge directory | DMG found in that directory | Cask file to create |
|---|---|---|
| `2026-ventura` | `20260625-Applications-GNATStudio.dmg` | `Casks/gnatstudio.rb` (current) |
| `2025-ventura` | `20250802-Applications.dmg` | `Casks/gnatstudio@2025.rb` |
| `2024-ventura` | `20240623-Applications-GNATStudio.dmg` | `Casks/gnatstudio@2024.rb` |
| `2023-ventura` | `20230713-Applications.dmg` | `Casks/gnatstudio@2023.rb` |
| `2022-monterey` | `20221119-Applications-GNATStudio.dmg` and `20221011-Applications.dmg` | `Casks/gnatstudio@2022.rb` |
| `2021-monterey`, `2020-catalina` and older | No GNAT Studio DMG seen; compiler packages or readmes only | none yet |

The SourceForge JSON blob embedded in each directory page is in `../evidence/sf-*.html`. The 2026 file is at `../evidence/sf-2026-ventura.html:1866`; its checksum was computed locally after download and is recorded in `../evidence/MANIFEST.md`.

Homebrew's versioned naming convention is `foo@1.2.rb`; `keg_only :versioned_formula` lets old and current versions coexist. See `../evidence/brew-versions.html:63,77,82`.

The Linux side follows AdaCore tags: `gnatstudio-2026.2-20260409` is the current one, with both `aarch64-linux` and `x86_64-linux` tarballs (`../evidence/gnatstudio-releases.json:30,44,80`). Older tags such as `gnatstudio-cr-20250417` only carry `x86_64-linux`, so the daily job reports `MISSING_LINUX_AARCH64` instead of shipping a half-complete release.
