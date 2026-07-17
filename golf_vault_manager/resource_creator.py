from __future__ import annotations

from pathlib import Path

from .config import VAULT_PATH
from .markdown_writer import build_markdown
from .models import ResourceFormData


def create_resource(
    resource: ResourceFormData,
    vault_path: Path = VAULT_PATH,
) -> tuple[Path, Path]:
    """
    Create the Markdown note and Windows URL shortcut.

    Returns:
        (markdown_path, url_path)
    """

    resources_folder = vault_path / "Resources"
    media_folder = vault_path / "Media"

    resources_folder.mkdir(parents=True, exist_ok=True)
    media_folder.mkdir(parents=True, exist_ok=True)

    markdown_path = resources_folder / f"{resource.base_name}.md"
    url_path = media_folder / f"{resource.base_name}.url"

    # Don't overwrite anything.
    if markdown_path.exists():
        raise FileExistsError(markdown_path)

    if url_path.exists():
        raise FileExistsError(url_path)

    markdown = build_markdown(resource)

    with markdown_path.open("x", encoding="utf-8", newline="\n") as file:
        file.write(markdown)

    with url_path.open("x", encoding="utf-8", newline="\n") as file:
        file.write(
            "[InternetShortcut]\n"
            f"URL={resource.url}\n"
        )

    return markdown_path, url_path