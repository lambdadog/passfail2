{ pkgs ? import <nixpkgs> {} }:

with pkgs;

let
  ankiAddonFilter = name: _:
    lib.hasSuffix ".py" name ||
    lib.hasSuffix ".json" name;
in stdenvNoCC.mkDerivation {
  pname = "passfail2";
  version = "0.1.0";

  src = builtins.filterSource ankiAddonFilter ./.;

  phases = [ "unpackPhase" "buildPhase" ];

  buildPhase = ''
  mkdir -p $out
  ${zip}/bin/zip -r $out/passfail2.ankiaddon *
  '';
}
