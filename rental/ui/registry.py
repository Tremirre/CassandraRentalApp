import customtkinter as ctk

from dataclasses import dataclass, field


@dataclass
class ComponentRegistry:
    button_registry: dict[str, ctk.CTkButton] = field(default_factory=dict)
    label_registry: dict[str, ctk.CTkLabel] = field(default_factory=dict)
    entry_registry: dict[str, ctk.CTkEntry] = field(default_factory=dict)
    combo_box_registry: dict[str, ctk.CTkComboBox] = field(default_factory=dict)

    def make_button(self, tag: str, *args, **kwargs) -> ctk.CTkButton:
        button = ctk.CTkButton(*args, **kwargs)
        self.button_registry[tag] = button
        return button

    def make_label(self, tag: str, *args, **kwargs) -> ctk.CTkLabel:
        label = ctk.CTkLabel(*args, **kwargs)
        self.label_registry[tag] = label
        return label

    def make_entry(self, tag: str, *args, **kwargs) -> ctk.CTkEntry:
        entry = ctk.CTkEntry(*args, **kwargs)
        self.entry_registry[tag] = entry
        return entry

    def make_combo_box(self, tag: str, *args, **kwargs) -> ctk.CTkComboBox:
        combo_box = ctk.CTkComboBox(*args, **kwargs)
        self.combo_box_registry[tag] = combo_box
        return combo_box

    def get_combo_box(self, tag: str) -> ctk.CTkComboBox:
        return self.combo_box_registry[tag]

    def get_button(self, tag: str) -> ctk.CTkButton:
        return self.button_registry[tag]

    def get_label(self, tag: str) -> ctk.CTkLabel:
        return self.label_registry[tag]

    def get_entry(self, tag: str) -> ctk.CTkEntry:
        return self.entry_registry[tag]
