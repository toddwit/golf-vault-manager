from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .config import DEFAULT_RATING, DEFAULT_TOPICS, MAX_RATING, MIN_RATING, VAULT_PATH
from .resource_creator import create_markdown_resource
from .validation import ValidationError, validate_form

class GolfVaultManagerApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Golf Vault Manager")
        self.root.geometry("700x690")
        self.root.minsize(620, 620)

        self.url_var = tk.StringVar()
        self.instructor_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.rating_var = tk.IntVar(value=DEFAULT_RATING)
        self.status_var = tk.StringVar(value="Ready")
        self.preview_var = tk.StringVar(value="Resource name preview will appear here.")

        self.topic_vars = {
            topic: tk.BooleanVar(value=False)
            for topic in DEFAULT_TOPICS
        }

        self._configure_style()
        self._build_window()
        self._bind_preview_updates()

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        style.configure("Heading.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Subheading.TLabel", font=("Segoe UI", 9))
        style.configure("Preview.TLabel", font=("Segoe UI", 10, "bold"))

    def _build_window(self) -> None:
        outer = ttk.Frame(self.root, padding=20)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)

        ttk.Label(
            outer,
            text="Golf Vault Manager",
            style="Heading.TLabel",
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            outer,
            text=f"Obsidian vault: {VAULT_PATH}",
            style="Subheading.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(2, 18))

        form = ttk.LabelFrame(outer, text="New Golf Resource", padding=16)
        form.grid(row=2, column=0, sticky="nsew")
        form.columnconfigure(0, weight=1)

        self._add_entry(
            form,
            row=0,
            label="Video URL",
            variable=self.url_var,
        )
        self._add_entry(
            form,
            row=2,
            label="Instructor / Source",
            variable=self.instructor_var,
        )
        self._add_entry(
            form,
            row=4,
            label="Short Descriptive Title",
            variable=self.title_var,
        )

        ttk.Label(form, text="Topics").grid(
            row=6, column=0, sticky="w", pady=(12, 6)
        )

        topics_frame = ttk.Frame(form)
        topics_frame.grid(row=7, column=0, sticky="ew")
        topics_frame.columnconfigure(0, weight=1)
        topics_frame.columnconfigure(1, weight=1)

        for index, topic in enumerate(DEFAULT_TOPICS):
            row = index // 2
            column = index % 2
            ttk.Checkbutton(
                topics_frame,
                text=topic,
                variable=self.topic_vars[topic],
            ).grid(row=row, column=column, sticky="w", padx=(0, 24), pady=3)

        ttk.Label(form, text="Rating").grid(
            row=8, column=0, sticky="w", pady=(16, 6)
        )

        rating_frame = ttk.Frame(form)
        rating_frame.grid(row=9, column=0, sticky="w")

        for rating in range(MIN_RATING, MAX_RATING + 1):
            ttk.Radiobutton(
                rating_frame,
                text=str(rating),
                variable=self.rating_var,
                value=rating,
            ).pack(side="left", padx=(0, 12))

        preview_frame = ttk.LabelFrame(
            outer,
            text="Resource Name Preview",
            padding=12,
        )
        preview_frame.grid(row=3, column=0, sticky="ew", pady=(14, 0))
        preview_frame.columnconfigure(0, weight=1)

        ttk.Label(
            preview_frame,
            textvariable=self.preview_var,
            style="Preview.TLabel",
            wraplength=620,
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            preview_frame,
            text="Future .md, .mp4, .jpg, and .url files will all use this base name.",
            style="Subheading.TLabel",
            wraplength=620,
        ).grid(row=1, column=0, sticky="w", pady=(5, 0))

        actions = ttk.Frame(outer)
        actions.grid(row=4, column=0, sticky="ew", pady=(18, 0))
        actions.columnconfigure(0, weight=1)

        ttk.Label(
            actions,
            textvariable=self.status_var,
        ).grid(row=0, column=0, sticky="w")

        ttk.Button(
            actions,
            text="Create Resource",
            command=self._create_resource,
        ).grid(row=0, column=1, padx=(12, 0))

        ttk.Button(
            actions,
            text="Clear Form",
            command=self._clear_form,
        ).grid(row=0, column=2, padx=(8, 0))

        self.url_entry.focus_set()

    def _add_entry(
        self,
        parent: ttk.LabelFrame,
        *,
        row: int,
        label: str,
        variable: tk.StringVar,
    ) -> None:
        ttk.Label(parent, text=label).grid(
            row=row, column=0, sticky="w", pady=(0, 6)
        )

        entry = ttk.Entry(parent, textvariable=variable)
        entry.grid(row=row + 1, column=0, sticky="ew")

        if variable is self.url_var:
            self.url_entry = entry

    def _bind_preview_updates(self) -> None:
        self.instructor_var.trace_add("write", self._update_preview)
        self.title_var.trace_add("write", self._update_preview)

    def _update_preview(self, *_args: object) -> None:
        instructor = self.instructor_var.get().strip()
        title = self.title_var.get().strip()

        if instructor and title:
            self.preview_var.set(f"{instructor} - {title}")
        else:
            self.preview_var.set("Resource name preview will appear here.")

    def _selected_topics(self) -> list[str]:
        return [
            topic
            for topic, variable in self.topic_vars.items()
            if variable.get()
        ]

    def _create_resource(self) -> None:
        try:
            resource = validate_form(
                url=self.url_var.get(),
                instructor=self.instructor_var.get(),
                title=self.title_var.get(),
                topics=self._selected_topics(),
                rating=self.rating_var.get(),
            )
        except ValidationError as exc:
            self.status_var.set("Validation failed")
            messagebox.showerror("Please Correct the Form", str(exc))
            return

        self.preview_var.set(resource.base_name)
        self.status_var.set("Creating Markdown note...")

        try:
            note_path = create_markdown_resource(resource)
        except FileExistsError:
            self.status_var.set("Resource already exists")
            messagebox.showerror(
                "Resource Already Exists",
                (
                    "A Markdown note already exists for this resource:\n\n"
                    f"{resource.base_name}.md\n\n"
                    "No existing file was changed."
                ),
            )
            return
        except OSError as exc:
            self.status_var.set("Could not create resource")
            messagebox.showerror(
                "Could Not Create Resource",
                (
                    "The Markdown note could not be created.\n\n"
                    f"{exc}"
                ),
            )
            return

        self.status_var.set("Markdown note created")

        messagebox.showinfo(
            "Resource Created",
            (
                "The Markdown resource note was created successfully.\n\n"
                f"{note_path}\n\n"
                "The video and URL shortcut have not been created yet."
            ),
        )
        
    def _clear_form(self) -> None:
        self.url_var.set("")
        self.instructor_var.set("")
        self.title_var.set("")
        self.rating_var.set(DEFAULT_RATING)

        for variable in self.topic_vars.values():
            variable.set(False)

        self.status_var.set("Ready")
        self.preview_var.set("Resource name preview will appear here.")
        self.url_entry.focus_set()

    def run(self) -> None:
        self.root.mainloop()
