import customtkinter as ctk

from .util import name_to_tag
from .registry import ComponentRegistry


class Panel(ctk.CTkFrame):
    def __init__(
        self,
        *args,
        title: str,
        button_texts: list[str],
        component_registry: ComponentRegistry,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            width=200,
            font=("Roboto", 24),
        )
        self.title_label.pack(fill="x", padx=10, pady=10)
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.pack(fill="both", expand=True)
        self.setup_additional_components(component_registry)
        self.register_buttons(button_texts, component_registry)

    def setup_additional_components(self, component_registry: ComponentRegistry):
        ...

    def register_buttons(
        self, button_texts: list[str], component_registry: ComponentRegistry
    ):
        for text in button_texts:
            button = component_registry.make_button(
                name_to_tag(text),
                self.get_button_frame(),
                text=text,
                width=200,
                font=("Roboto", 16),
            )
            button.pack(fill="x", padx=10, pady=10)

    def get_button_frame(self) -> ctk.CTkFrame:
        return self.content_frame


class DualPanel(Panel):
    def setup_additional_components(self, component_registry: ComponentRegistry):
        self.left_frame = ctk.CTkFrame(self.content_frame)
        self.right_frame = ctk.CTkFrame(self.content_frame)
        self.left_frame.pack(fill="both", expand=True, side="left", padx=10, pady=10)
        self.right_frame.pack(fill="both", expand=True, side="right", padx=10, pady=10)

    def get_button_frame(self) -> ctk.CTkFrame:
        return self.left_frame
