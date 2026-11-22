cask "gnatstudio" do
  version "2026.2a,20260625"
  sha256 "6dd3ec401cba4d7beea28537aa9f7f394bbd76049790c8783a9477e8acf6f27f"

  url "https://downloads.sourceforge.net/project/gnuada/GNAT_GPL%20Mac%20OS%20X/2026-ventura/20260625-Applications-GNATStudio.dmg"
  name "GNAT Studio"
  desc "Ada and SPARK integrated development environment"
  homepage "https://github.com/AdaCore/gnatstudio"
  # upstream owner: gnuada SourceForge project
  depends_on macos: ">= :monterey"

  app "GNATStudio.app"

  caveats do
    requires_rosetta
  end

  livecheck do
    skip "Versioned SourceForge directory; the daily workflow updates this cask"
  end
end
