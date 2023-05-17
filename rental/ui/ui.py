import customtkinter as ctk

from typing import Callable

from .registry import ComponentRegistry
from .main_frame import MainFrame
from .side_frame import SideFrame


class UI:
    def __init__(
        self,
        root_app: ctk.CTk,
        model_names: list[str],
    ) -> None:
        self.component_registry = ComponentRegistry()
        self.base_frame = ctk.CTkFrame(root_app)
        self.base_frame.pack(fill="both", expand=True)

        self.side_frame = SideFrame(
            self.base_frame, component_registry=self.component_registry
        )
        self.main_frame = MainFrame(
            self.base_frame,
            component_registry=self.component_registry,
            model_names=model_names,
        )

        self._setup_base_btn_commands()

    def add_btn_command(self, tag: str, command: Callable) -> None:
        self.component_registry.get_button(tag).configure(command=command)

    def set_label_text(self, tag: str, text: str) -> None:
        self.component_registry.get_label(tag).configure(text=text)

    def _setup_base_btn_commands(self):
        self.add_btn_command("admin", lambda: self.main_frame.show_panel(0))
        self.add_btn_command("user", lambda: self.main_frame.show_panel(1))
        self.add_btn_command("testing", lambda: self.main_frame.show_panel(2))
