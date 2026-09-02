check: check-python check-shell

check-shell:
    find . -type f -name "*.sh" -exec shellcheck {} +

check-python:
    uv run --locked ruff format --diff
    uv run --locked ruff check
    uv run --locked pyrefly coverage check
    uv run --locked pyrefly check

fix:
    uv run --locked ruff format
    uv run --locked ruff check --fix
