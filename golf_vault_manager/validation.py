from __future__ import annotations

import re
from urllib.parse import urlparse

from .config import MAX_RATING, MIN_RATING
from .models import ResourceFormData

INVALID_FILENAME_CHARACTERS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
WHITESPACE = re.compile(r"\s+")


class ValidationError(ValueError):
    """Raised when form data is invalid."""


def normalize_text(value: str) -> str:
    return WHITESPACE.sub(" ", value).strip()


def is_valid_web_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme.lower() in {"http", "https"} and bool(parsed.netloc)


def sanitize_filename_part(value: str) -> str:
    cleaned = normalize_text(value)
    cleaned = INVALID_FILENAME_CHARACTERS.sub("-", cleaned)
    cleaned = WHITESPACE.sub(" ", cleaned).strip(" .")

    if not cleaned:
        raise ValidationError("The instructor and title must contain usable characters.")

    return cleaned


def validate_form(
    *,
    url: str,
    instructor: str,
    title: str,
    topics: list[str],
    rating: int,
) -> ResourceFormData:
    normalized_url = normalize_text(url)
    normalized_instructor = normalize_text(instructor)
    normalized_title = normalize_text(title)
    normalized_topics = tuple(sorted({normalize_text(topic) for topic in topics if normalize_text(topic)}))

    errors: list[str] = []

    if not normalized_url:
        errors.append("Enter a video URL.")
    elif not is_valid_web_url(normalized_url):
        errors.append("Enter a complete URL beginning with http:// or https://.")

    if not normalized_instructor:
        errors.append("Enter the instructor or source.")

    if not normalized_title:
        errors.append("Enter a short descriptive title.")

    if not normalized_topics:
        errors.append("Choose at least one topic.")

    if not MIN_RATING <= rating <= MAX_RATING:
        errors.append(f"Choose a rating from {MIN_RATING} to {MAX_RATING}.")

    if errors:
        raise ValidationError("\n".join(errors))

    safe_instructor = sanitize_filename_part(normalized_instructor)
    safe_title = sanitize_filename_part(normalized_title)

    return ResourceFormData(
        url=normalized_url,
        instructor=safe_instructor,
        title=safe_title,
        topics=normalized_topics,
        rating=rating,
    )
