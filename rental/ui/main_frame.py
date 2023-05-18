import customtkinter as ctk

from . import panel
from .registry import ComponentRegistry
from ..util import name_to_tag


class MainFrame(ctk.CTkFrame):
    def __init__(
        self,
        *args,
        component_registry: ComponentRegistry,
        model_names: list[str],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.pack(fill="both", expand=True)
        self.current_index = None
        self.admin_panel = panel.DualPanel(
            self,
            title="Application Admin",
            button_texts=["Clear Database", "Repopulate Database"],
            component_registry=component_registry,
        )
        self.user_panel = panel.Panel(
            self,
            title="User Panel",
            button_texts=[],
            component_registry=component_registry,
        )
        self.testing_panel = panel.DualPanel(
            self,
            title="Testing",
            button_texts=[f"Stress Test {i+1}" for i in range(4)],
            component_registry=component_registry,
        )

        self.panels = [
            self.admin_panel,
            self.user_panel,
            self.testing_panel,
        ]

        self.setup_admin_panel(component_registry, model_names)

        self.show_panel(0)

    def show_panel(self, panel_index: int) -> None:
        if panel_index == self.current_index:
            return
        if self.current_index is not None:
            self.panels[self.current_index].pack_forget()
        self.current_index = panel_index
        self.panels[panel_index].pack(fill="both", expand=True)

    def setup_admin_panel(
        self, component_registry: ComponentRegistry, model_names: list[str]
    ) -> None:
        self.admin_panel.right_frame.columnconfigure(0, weight=1)
        admin_stat_frame = ctk.CTkFrame(self.admin_panel.right_frame)
        admin_stat_frame.grid(padx=10, pady=10, sticky="nsew")
        admin_stat_frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(
            admin_stat_frame,
            text="Model Instance Counts",
            font=("Roboto", 20),
        ).grid(row=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        desc_labels = [
            ctk.CTkLabel(
                admin_stat_frame,
                text=name,
                font=("Roboto", 16, "bold"),
                justify="left",
            )
            for name in model_names
        ]
        for i, label in enumerate(desc_labels):
            label.grid(row=i + 1, column=0, padx=30, pady=10, sticky="nsw")

        count_labels = [
            component_registry.make_label(
                f"{name_to_tag(name)}_count",
                admin_stat_frame,
                text="0",
                font=("Roboto", 16),
            )
            for name in model_names
        ]
        for i, label in enumerate(count_labels):
            label.grid(row=i + 1, column=1, padx=30, pady=10, sticky="nse")
