from __future__ import annotations

import json
from datetime import date

from .models import ResourceFormData


def build_markdown(resource: ResourceFormData) -> str:
    """Build the complete Markdown resource note."""

    quoted_title = json.dumps(resource.base_name)
    quoted_instructor = json.dumps(resource.instructor)
    quoted_source = json.dumps(resource.url)

    topic_lines = "\n".join(
        f"  - {json.dumps(topic)}"
        for topic in resource.topics
    )

    return f"""---
title: {quoted_title}
instructor: {quoted_instructor}
topics:
{topic_lines}
source: {quoted_source}
video: ""
thumbnail: ""
rating: {resource.rating}
status: unreviewed
created: {date.today().isoformat()}
tags:
  - golf
  - resource
---

# {resource.base_name}

## Preview

## Video

## Original Source

{resource.url}

## Why I Saved It

## Key Takeaways

- 

## My Notes

- 

## Related Topics

"""