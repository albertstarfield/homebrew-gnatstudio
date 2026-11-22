# Self-install sweep log

Whole-work sweep against the three recorded steps.

1. Remote tap manifests were checked against local workdir files. Fresh `gh api` reads show `albertstarfield/homebrew-alire` and `albertstarfield/homebrew-gnatstudio` on `main`; local heads match remote heads exactly: Alire `67e7ee5fa4073a009232b74ccb51eaa2ee77cc04`, GNAT Studio `bd13a4e90538008b9aa3da13cc2e00ddb9356de9`. See `~/.hermes/logs/audit/adahomebrew-sweep-20261122.log:1-8`.
2. Brew blockers found and handled: stale local taps pointing at the workdir (fixed by retapping GitHub), untrusted taps (fixed by `brew trust`), PATH shadowing of `alr` by `/usr/local/bin/alr` (documented in the README, not deleted), and a SIGTERM during the 344 MB DMG download (fixed by a background retry). Each blocker has command output in `~/.hermes/logs/audit/adahomebrew-install-20261122.log:39-77,64-70,81,109-110`.
3. The briefing citations in the chat answer were checked line by line. Two defects were found and corrected here: the Lean citation for the shadowed-PATH counterexample needed range `:13-20` rather than `:13-17`, and the claim that a missing macOS DMG blocks a PR belongs to `GNATStudio/src/updater.ads:6-27`, not to the install-readiness proof. All other cited log and README lines matched their claims.

No placeholder, TODO, or stub marker exists in shipped files. The only `stub` strings are upstream GNAT Studio filenames inside `evidence/gnatstudio-tree.json`. Lean and Rocq were rerun during the sweep and both exited 0 (`install-proof-checks.log:1-3`). Installs remain present: `alr 2.1.1` and `gnatstudio 2026.2a,20260625` (`adahomebrew-sweep-20261122.log:9-12`).
