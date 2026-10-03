{
  description = "Python Devshell";

  inputs = {
    nixpkgs.url = "https://channels.nixos.org/nixpkgs-unstable/nixexprs.tar.zst";
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
              # - .python-version (this is what uv installs in CI)
              # - pyproject.toml `requires-python` (if i use features from newer python)
              python = pkgs.python314;
            in
            pkgs.mkShellNoCC {
              packages = with pkgs; [
                python
                # When bumping nixpkgs, also bump
                # - action.yml `.runs.steps[0].with.version` (pinned for deterministic CI)
                # - pyproject.toml ".tool.uv.'required-version'" if new minor version
                uv

                # Shell/github action linters used in CI
                shellcheck
                zizmor

                # command runner
                just
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
