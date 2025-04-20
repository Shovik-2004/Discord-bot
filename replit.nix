{pkgs}: {
  deps = [
    pkgs.cacert
    pkgs.xsimd
    pkgs.rustc
    pkgs.openssl
    pkgs.libxcrypt
    pkgs.libiconv
    pkgs.cargo
    pkgs.pkg-config
    pkgs.libffi
    pkgs.nano
    pkgs.glibcLocales
  ];
}
