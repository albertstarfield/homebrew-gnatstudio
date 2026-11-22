# GNAT Studio tap

This tap ships GNAT Studio in two pieces. On macOS it installs the DMG published by the gnuada project on SourceForge as a cask. On Linux it installs the tarball from the AdaCore GitHub release as a formula. The two sources are separate because the AdaCore release currently has Linux and Windows binaries only; the macOS build lives in the SourceForge directories.

## Add the tap

```
brew tap <you>/gnatstudio
```

The repository is named `homebrew-gnatstudio`, so the short tap name is `gnatstudio`.

## Install on macOS

```
brew install --cask gnatstudio
```

The cask downloads `20260625-Applications-GNATStudio.dmg` from `GNAT_GPL Mac OS X/2026-ventura`, verifies the SHA-256 recorded in `Casks/gnatstudio.rb`, and copies `GNATStudio.app` into `/Applications`. The DMG is not codesigned. macOS may refuse to open the app the first time; the upstream readme suggests:

```
xattr -r -d com.apple.quarantine /Applications/GNATStudio.app
```

The upstream readme also says this build targets macOS 13 or newer on x86_64. It does not provide an arm64 DMG, so Apple Silicon users need Rosetta or a different build.

## Install on Linux

```
brew install gnatstudio
```

The formula downloads the `x86_64-linux-bin.tar.gz` or `aarch64-linux-bin.tar.gz` asset from the matching AdaCore release. The tarball has a top-level directory named after the release, with `bin/gnatstudio` inside. Release tags, asset names and digests are kept in `evidence/gnatstudio-releases.json`.

## Older versions

SourceForge keeps directories for several years: `2026-ventura`, `2025-ventura`, `2024-ventura`, `2023-ventura`, `2022-monterey` and older. Each directory that contains a DMG can get a versioned cask named `Casks/gnatstudio@2025.rb`, `Casks/gnatstudio@2024.rb` and so on. Homebrew uses the `@version` suffix for parallel installs; see `docs/versions.md` and `evidence/sf-macosx-parent.html`.

```
brew install --cask gnatstudio@2025
```

The 2025 and 2026 SourceForge directory metadata has no published SHA-256 for the DMG, so the daily job computes it when the file changes. Older casks use `sha256 :no_check` when no checksum can be obtained.

## Upgrade

```
brew update
brew upgrade --cask gnatstudio   # macOS
brew upgrade gnatstudio          # Linux
```

The daily workflow checks AdaCore's GitHub releases for a newer tag and the SourceForge directory for a newer DMG. A pull request is opened only when the Linux x86_64 and aarch64 assets and the macOS DMG are all present. The decision is in the SPARK package `src/updater.ads`; missing assets are named blockers, not an implicit assumption that every release is complete.

To check the logic locally:

```
gprbuild -P updater.gpr
gnatprove --mode=all --level=4 -j0 -P updater.gpr
```

## Remove

```
brew uninstall --cask gnatstudio
brew uninstall gnatstudio
brew untap <you>/gnatstudio
```

## Layout

- `Casks/gnatstudio.rb` - macOS DMG cask
- `Formula/gnatstudio.rb` - Linux tarball formula
- `docs/versions.md` - SourceForge directory map and versioned cask rules
- `src/updater.ads`, `src/updater.adb`, `src/main.adb` - SPARK decision code and its I/O boundary
- `scripts/update_gnatstudio.py` - fetches both upstreams and renders the files
- `.github/workflows/update.yml`, `.github/workflows/ci.yml` - daily check and validation
- `evidence/` - raw release JSON, SourceForge HTML and the copied Homebrew docs

Replace `<you>` with your GitHub owner or organisation name before publishing.
