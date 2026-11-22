cask "gnatstudio" do
  version "2026.2a,20260625"
  sha256 "6dd3ec401cba4d7beea28537aa9f7f394bbd76049790c8783a9477e8acf6f27f"

  url "https://sourceforge.net/projects/gnuada/files/GNAT_GPL%20Mac%20OS%20X/2026-ventura/20260625-Applications-GNATStudio.dmg/download"
  name "GNAT Studio"
  desc "Ada and SPARK integrated development environment"
  homepage "https://github.com/AdaCore/gnatstudio"
  # upstream owner: gnuada SourceForge project
  app "GNATStudio.app"
end
