import customtkinter as ctk

from ..util import name_to_tag
from .registry import ComponentRegistry


class SideFrame(ctk.CTkFrame):
    def __init__(
        self,
        *args,
        component_registry: ComponentRegistry,
        width=200,
        app_title: str = "RentApp",
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.pack(fill="y", side="left", ipadx=10, ipady=10)
        self.app_title_label = ctk.CTkLabel(
            self,
            text=app_title,
            width=width,
            font=("Roboto", 32),
        )
        self.app_title_label.pack(fill="x", padx=10, pady=10)
        for text in ("Admin", "User", "Testing"):
            button = component_registry.make_button(
                name_to_tag(text),
                self,
                text=text,
                width=width,
                font=("Roboto", 16),
            )
            button.pack(fill="x", padx=10, pady=10)
