from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceFormData:
    url: str
    instructor: str
    title: str
    topics: tuple[str, ...]
    rating: int

    @property
    def base_name(self) -> str:
        return f"{self.instructor} - {self.title}"
