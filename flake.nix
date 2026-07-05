{
  description = "Python Devshell";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "aarch64-darwin"
        "aarch64-linux"
        "x86_64-darwin"
        "x86_64-linux"
      ];

      perSystem =
        { pkgs, lib, ... }:
        {
          devShells.default =
            let
              # When bumping, also update
              # - .python-version
              # - pyproject.toml `requires-python`
              python = pkgs.python314;
            in
            pkgs.mkShell {
              packages = with pkgs; [
                python
                # When bumping nixpkgs, also bump
                # - pyproject.toml `tools.uv.required-version`
                uv

                # Shell/github action linters used in CI
                shellcheck
                zizmor
              ];

              env = {
                UV_PYTHON = lib.getExe python;
                UV_PYTHON_DOWNLOADS = "never";
              };

              shellHook = "uv sync";
            };
        };
    };
}
