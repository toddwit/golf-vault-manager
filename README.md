# Golf Vault Manager — Small Version 1

This first version contains:

- A Windows desktop interface built with Python 3 and Tkinter
- Fields for URL, instructor/source, short descriptive title, topics, and rating
- Multi-topic selection
- Basic form validation
- Windows-safe resource naming
- A live preview using the format:

  `Instructor - Short Descriptive Title`

This version does **not** download videos or create vault files yet.

## Project structure

```text
golf-vault-manager-v1/
├── app.py
├── golf_vault_manager/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── ui.py
│   └── validation.py
├── tests/
│   └── test_validation.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Configured Obsidian vault

```text
C:\00 Personal\Golf Vault
```

The path is stored in:

```text
golf_vault_manager\config.py
```

## Run the application

Open Command Prompt in the project folder and run:

```bat
py app.py
```

If the `py` launcher is unavailable:

```bat
python app.py
```

This version does not require PowerShell or any third-party Python packages.

## Run the tests

From the project folder:

```bat
py -m unittest discover -s tests
```

## Current validation rules

The form requires:

- A complete `http://` or `https://` URL
- An instructor or source
- A short descriptive title
- At least one selected topic
- A rating from 1 through 5

The instructor and title are cleaned so the future shared base filename will not contain characters that Windows forbids.

## Suggested first test

Enter:

```text
URL:
https://www.youtube.com/watch?v=example

Instructor / Source:
Golf NBS

Short Descriptive Title:
Two Grip Mistakes

Topics:
Grip
Clubface Control

Rating:
4
```

Expected resource name:

```text
Golf NBS - Two Grip Mistakes
```

## Next development step

After the form behavior is satisfactory, add a save workflow that creates a Markdown resource note and `.url` file without downloading the video. This keeps each new capability independently testable before yt-dlp and FFmpeg are introduced.
