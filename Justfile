uv := "uv run --locked"
ci := env("GITHUB_ACTIONS", "false")

output_flags := if ci == "true" { "--output-format github" } else {""}
ruff_format_output_flags := if ci == "true" { "--check --output-format github" } else {"--diff"}

check: check-python check-shell

check-shell:
    find . -type f -name "*.sh" -exec shellcheck {} +

check-python:
    {{uv}} ruff format {{ruff_format_output_flags}}
    {{uv}} ruff check {{output_flags}}
    {{uv}} pyrefly coverage check {{output_flags}}
    {{uv}} pyrefly check {{output_flags}}

fix:
    {{uv}} ruff format
    {{uv}} ruff check --fix
