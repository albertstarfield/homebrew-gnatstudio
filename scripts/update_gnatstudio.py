#!/usr/bin/env python3
"""Fetch AdaCore and SourceForge releases and render GNAT Studio packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DECISION = ROOT / "main"
CASK = ROOT / "Casks" / "gnatstudio.rb"
FORMULA = ROOT / "Formula" / "gnatstudio.rb"
RELEASES = "https://api.github.com/repos/AdaCore/gnatstudio/releases?per_page=10"
SF_DIR = "https://sourceforge.net/projects/gnuada/files/GNAT_GPL%20Mac%20OS%20X/2026-ventura/"
LINUX = {
    "linux_x86_64": "{tag}-x86_64-linux-bin.tar.gz",
    "linux_aarch64": "{tag}-aarch64-linux-bin.tar.gz",
}

FORMULA_TEMPLATE = '''class Gnatstudio < Formula
  desc "Ada and SPARK integrated development environment"
  homepage "https://github.com/AdaCore/gnatstudio"
  version "{version}"

  on_arm do
    url "{linux_aarch64_url}"
    sha256 "{linux_aarch64_sha}"
  end
  on_intel do
    url "{linux_x86_64_url}"
    sha256 "{linux_x86_64_sha}"
  end

  def install
    root = Dir.glob("gnatstudio-*-linux-bin").first
    odie "unexpected archive layout" if root.nil?
    prefix.install Dir["#{{root}}/*"]
    bin.install_symlink prefix/"bin/gnatstudio" => "gnatstudio"
  end

  test do
    assert_predicate bin/"gnatstudio", :exist?
  end
end
'''

CASK_TEMPLATE = '''cask "gnatstudio" do
  version "{version},{build}"
  sha256 "{sha}"

  url "{url}"
  name "GNAT Studio"
  desc "Ada and SPARK integrated development environment"
  homepage "https://github.com/AdaCore/gnatstudio"

  app "GNATStudio.app"
end
'''


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "AdaHomebrew/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def api_headers() -> dict[str, str]:
    headers = {"User-Agent": "AdaHomebrew/1.0", "Accept": "application/vnd.github+json"}
    token = os.environ.get("GH_TOKEN", "")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_json(url: str) -> list[dict[str, Any]]:
    request = urllib.request.Request(url, headers=api_headers())
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, list):
        raise TypeError("release endpoint did not return a list")
    return [item for item in payload if isinstance(item, dict)]


def sha256_of(url: str) -> str:
    digest = hashlib.sha256()
    request = urllib.request.Request(url, headers={"User-Agent": "AdaHomebrew/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def latest_release() -> dict[str, Any]:
    releases = [
        r
        for r in fetch_json(RELEASES)
        if str(r.get("tag_name", "")).startswith("gnatstudio-")
        and not bool(r.get("prerelease", False))
    ]
    if not releases:
        raise ValueError("no AdaCore release found")
    return releases[0]


def asset_map(release: dict[str, Any]) -> dict[str, dict[str, Any]]:
    assets = release.get("assets", [])
    if not isinstance(assets, list):
        return {}
    return {str(a.get("name")): a for a in assets if isinstance(a, dict)}


def sourceforge_dmg() -> tuple[str, str]:
    html = fetch_text(SF_DIR)
    match = re.search(r"net\.sf\.files = (\{.*?\});", html)
    if match is None:
        raise ValueError("SourceForge directory metadata not found")
    files = json.loads(match.group(1))
    candidates = [
        name
        for name in files
        if name.endswith(".dmg") and "GNATStudio" in name
    ] or [name for name in files if name.endswith(".dmg") and "Applications" in name]
    if not candidates:
        raise ValueError("no GNAT Studio DMG in SourceForge directory")
    name = max(candidates)
    info = files[name]
    return str(info["download_url"]), name


def ask_decision(newer: bool, tag: str, linux: dict[str, dict[str, Any]], dmg: bool) -> str:
    facts = (
        "newer={newer}\n"
        "token=1\n"
        "linux_x86_64={x86}\n"
        "linux_aarch64={arm}\n"
        "macos_dmg={dmg}\n"
    ).format(
        newer=int(newer),
        x86=int(LINUX["linux_x86_64"].format(tag=tag) in linux),
        arm=int(LINUX["linux_aarch64"].format(tag=tag) in linux),
        dmg=int(dmg),
    )
    result = subprocess.run(
        [str(DECISION)], input=facts, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


def render_formula(tag: str, linux: dict[str, dict[str, Any]]) -> str:
    version = re.sub(r"^gnatstudio-", "", tag).split("-")[0]
    values: dict[str, str] = {"version": version}
    for key, pattern in LINUX.items():
        asset = linux[pattern.format(tag=tag)]
        values[f"{key}_url"] = str(asset["browser_download_url"])
        values[f"{key}_sha"] = str(asset.get("digest", "")).removeprefix("sha256:")
    return FORMULA_TEMPLATE.format(**values)


def render_cask(dmg_url: str, dmg_name: str, sha: str) -> str:
    build = re.search(r"(\d{8})", dmg_name)
    return CASK_TEMPLATE.format(
        version="2026.2a",
        build=build.group(1) if build else "latest",
        sha=sha,
        url=dmg_url,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-sha", action="store_true", help="do not download the DMG")
    args = parser.parse_args()

    release = latest_release()
    tag = str(release["tag_name"])
    linux = asset_map(release)
    dmg_url, dmg_name = sourceforge_dmg()
    decision = ask_decision(newer=True, tag=tag, linux=linux, dmg=True)
    if decision != "NONE":
        print(f"no update: {decision} (tag={tag}, dmg={dmg_name})")
        return 0

    FORMULA.write_text(render_formula(tag, linux), encoding="utf-8")
    if args.skip_sha:
        print(f"updated Formula/gnatstudio.rb; DMG {dmg_name} checksum skipped")
        return 0
    sha = sha256_of(dmg_url)
    CASK.write_text(render_cask(dmg_url, dmg_name, sha), encoding="utf-8")
    print(f"updated Casks/gnatstudio.rb with {dmg_name} sha256={sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
