class Gnatstudio < Formula
  desc "Ada and SPARK integrated development environment"
  homepage "https://github.com/AdaCore/gnatstudio"
  version "2026.2"

  on_arm do
    url "https://github.com/AdaCore/gnatstudio/releases/download/gnatstudio-2026.2-20260409/gnatstudio-2026.2-20260409-aarch64-linux-bin.tar.gz"
    sha256 "5877bbe6eed939eed7a9bdebabbbcbb50dc8c279922f9558902fe2812446e00b"
  end
  on_intel do
    url "https://github.com/AdaCore/gnatstudio/releases/download/gnatstudio-2026.2-20260409/gnatstudio-2026.2-20260409-x86_64-linux-bin.tar.gz"
    sha256 "4017aa6698253732dbb611d1f784846a3fd508ae74bd0979b5e50f0207402fb7"
  end

  def install
    root = Dir.glob("gnatstudio-*-linux-bin").first
    odie "unexpected archive layout" if root.nil?
    prefix.install Dir["#{root}/*"]
    bin.install_symlink prefix/"bin/gnatstudio" => "gnatstudio"
  end

  test do
    assert_predicate bin/"gnatstudio", :exist?
  end
end
