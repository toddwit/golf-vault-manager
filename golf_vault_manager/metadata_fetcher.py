from __future__ import annotations

from dataclasses import dataclass

import yt_dlp


class MetadataError(Exception):
    """Raised when video metadata cannot be retrieved."""


@dataclass(frozen=True)
class VideoMetadata:
    title: str
    instructor: str


def fetch_video_metadata(url: str) -> VideoMetadata:
    """Retrieve video title and instructor without downloading the video."""

    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as exc:
        raise MetadataError(str(exc)) from exc

    if not info:
        raise MetadataError("No metadata was returned for this URL.")

    title = str(info.get("title") or "").strip()

    instructor = str(
        info.get("channel")
        or info.get("uploader")
        or info.get("creator")
        or ""
    ).strip()

    if not title:
        raise MetadataError("The video title could not be determined.")

    if not instructor:
        raise MetadataError("The instructor or channel could not be determined.")

    return VideoMetadata(
        title=title,
        instructor=instructor,
    )