{ pkgs ? import <nixpkgs> {} }:

with pkgs;

let
  ankiAddonFilter = name: _:
    lib.hasSuffix ".py" name ||
    lib.hasSuffix ".json" name;
in stdenvNoCC.mkDerivation rec {
  pname = "passfail2";
  version = "0.1.1";

  src = builtins.filterSource ankiAddonFilter ./.;

  phases = [ "unpackPhase" "buildPhase" ];

  buildPhase = ''
  mkdir -p $out
  ${zip}/bin/zip -r $out/passfail2-v${version}.ankiaddon *
  '';
}
