# GNAT Studio tap

This tap is maintained by `albertstarfield` as a redistribution convenience. The upstream owner is `AdaCore/gnatstudio`; the macOS DMG comes from the `gnuada` project on SourceForge. On macOS the tap installs that DMG as a cask. On Linux it installs the tarball from the AdaCore GitHub release as a formula. The two sources are separate because the AdaCore release currently has Linux and Windows binaries only; the macOS build lives in the SourceForge directories.

## One-line install

macOS:

```
brew tap albertstarfield/gnatstudio && brew install --cask gnatstudio
```

Linux:

```
brew tap albertstarfield/gnatstudio && brew install gnatstudio
```

## Add the tap

```
brew tap albertstarfield/gnatstudio
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
brew untap albertstarfield/gnatstudio
```

## FAQ

**Why does Homebrew say the tap is untrusted?**

Run `brew trust albertstarfield/gnatstudio`. Homebrew will not load packages from a new tap until you trust it.

**Why does `brew audit Casks/gnatstudio.rb` fail?**

Newer Homebrew versions want a token, not a path. Tap the checkout, trust it, then audit by name: `brew audit --strict --online --cask albertstarfield/gnatstudio/gnatstudio`.

**Why does macOS refuse to open GNAT Studio?**

The cask removes the quarantine attribute automatically after install, so the app should open without a manual step. If an older install still carries it, run `xattr -r -d com.apple.quarantine /Applications/GNATStudio.app` and open it again.

**Why can't Apple Silicon run the current macOS build?**

The SourceForge readme targets macOS 13 on x86_64 and does not provide an arm64 DMG. Use Rosetta, or install an older cask such as `gnatstudio@2025` if that build works for you. The Linux formula does have an aarch64 asset.

**Why did the daily job fail with HTTP 403 "rate limit exceeded"?**

The GitHub API rejects unauthenticated calls from shared runner IPs. The workflow sends `GH_TOKEN` as a bearer token. Export it if you run `scripts/update_gnatstudio.py` by hand.

**Why did no pull request appear after a release?**

The SPARK check needs both Linux assets and the macOS DMG. Check the log for `MISSING_LINUX_AARCH64` or `MISSING_MACOS_DMG`. Older AdaCore tags only ship x86_64 Linux, so they are skipped on purpose.

**Why does the cask checksum differ from the one on SourceForge?**

The 2025 and 2026 SourceForge directory metadata has no published SHA-256. The updater downloads the DMG and computes it. If the file was replaced upstream, rerun the update job and reopen the cask.

**Why did the scheduled workflow stop running?**

GitHub disables schedules in public repos after 60 days without activity and can drop runs near the top of the hour. The cron time is off-hour; a small commit or `workflow_dispatch` run reactivates it.

## Upstream owner

The tap owner is `albertstarfield`. That is just the Homebrew channel. The software owner is `AdaCore/gnatstudio`, with release assets in `evidence/gnatstudio-releases.json`. The macOS DMG is published by the separate `gnuada` project on SourceForge; its directory metadata is in `evidence/sf-2026-ventura.html`. This tap redistributes those binaries and does not build or sign them.

## Layout

- `Casks/gnatstudio.rb` - macOS DMG cask
- `Formula/gnatstudio.rb` - Linux tarball formula
- `docs/versions.md` - SourceForge directory map and versioned cask rules
- `src/updater.ads`, `src/updater.adb`, `src/main.adb` - SPARK decision code and its I/O boundary
- `scripts/update_gnatstudio.py` - fetches both upstreams and renders the files
- `.github/workflows/update.yml`, `.github/workflows/ci.yml` - daily check and validation
- `evidence/` - raw release JSON, SourceForge HTML and the copied Homebrew docs

The owner is `albertstarfield`.
