{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    python39Packages.virtualenv
    python39
  ];

  shellHook = ''
    source venv/bin/activate
    source venv/bin/activate.fish
  '';
}