{
  description = "Tang Primer 20K case release generation environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/597283ad8aa0b331c788e97c4c262d58877074ef";

  outputs =
    { nixpkgs, ... }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          python = pkgs.python312.withPackages (pythonPackages: [
            pythonPackages.pypdf
            pythonPackages.reportlab
          ]);
        in
        {
          default = pkgs.mkShellNoCC {
            name = "tang-primer-20k-case";
            packages = [
              python
              pkgs.dejavu_fonts
              pkgs.gnumake
            ];
            env = {
              DEJAVU_FONT_PATH = "${pkgs.dejavu_fonts}/share/fonts/truetype/DejaVuSans.ttf";
              LC_ALL = "C.UTF-8";
            };
          };
        }
      );

      formatter = forAllSystems (system: nixpkgs.legacyPackages.${system}.nixfmt);
    };
}
