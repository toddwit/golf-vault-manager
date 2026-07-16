import unittest

from golf_vault_manager.validation import (
    ValidationError,
    sanitize_filename_part,
    validate_form,
)


class ValidationTests(unittest.TestCase):
    def test_valid_form_builds_expected_base_name(self) -> None:
        resource = validate_form(
            url="https://www.youtube.com/watch?v=example",
            instructor="Golf NBS",
            title="Two Grip Mistakes",
            topics=["Grip", "Clubface Control"],
            rating=4,
        )

        self.assertEqual(
            resource.base_name,
            "Golf NBS - Two Grip Mistakes",
        )

    def test_requires_at_least_one_topic(self) -> None:
        with self.assertRaises(ValidationError):
            validate_form(
                url="https://example.com/video",
                instructor="Instructor",
                title="Title",
                topics=[],
                rating=3,
            )

    def test_requires_complete_web_url(self) -> None:
        with self.assertRaises(ValidationError):
            validate_form(
                url="youtube.com/video",
                instructor="Instructor",
                title="Title",
                topics=["Grip"],
                rating=3,
            )

    def test_filename_characters_are_replaced(self) -> None:
        self.assertEqual(
            sanitize_filename_part('Grip: "Simple/Strong?"'),
            "Grip- -Simple-Strong--",
        )


if __name__ == "__main__":
    unittest.main()
