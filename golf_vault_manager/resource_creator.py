from __future__ import annotations

from pathlib import Path

from .config import VAULT_PATH
from .markdown_writer import build_markdown
from .models import ResourceFormData


def create_markdown_resource(
    resource: ResourceFormData,
    vault_path: Path = VAULT_PATH,
) -> Path:
    """Create the Markdown note and return its full path."""

    resources_folder = vault_path / "Resources"
    resources_folder.mkdir(parents=True, exist_ok=True)

    note_path = resources_folder / f"{resource.base_name}.md"
    markdown = build_markdown(resource)

    # Mode "x" creates a new file but refuses to overwrite an existing one.
    with note_path.open("x", encoding="utf-8", newline="\n") as note_file:
        note_file.write(markdown)

    return note_path