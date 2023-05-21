import customtkinter as ctk

from . import panel
from .registry import ComponentRegistry
from .tile import Tile
from .table import ScrollableTable
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
        self.setup_user_panel(component_registry)
        self.setup_testing_panel(component_registry)

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

    def setup_user_panel(self, component_registry: ComponentRegistry) -> None:
        controls_frame = ctk.CTkFrame(self.user_panel.content_frame)
        controls_frame.pack(fill="x", padx=10, pady=10)
        refresh_btn = component_registry.make_button(
            "refresh_button",
            controls_frame,
            text="Refresh",
            font=("Roboto", 16),
        )
        refresh_btn.pack(side="right", padx=10, pady=10)

        tiles_grid = ctk.CTkFrame(self.user_panel.content_frame)
        tiles_grid.pack(fill="both", expand=True)
        tiles_grid.columnconfigure(0, weight=1)
        tiles_grid.columnconfigure(1, weight=1)
        tiles_grid.rowconfigure(0, weight=1)
        tiles_grid.rowconfigure(1, weight=1)

        make_reservation_tile = Tile(
            tiles_grid,
            title="Make Reservation",
            component_registry=component_registry,
        )
        make_reservation_tile.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        mr_user_combo_box = component_registry.make_combo_box(
            "mr_user_combo_box",
            make_reservation_tile.content_grid,
            values=["Select User"],
            font=("Roboto", 16),
        )
        mr_user_combo_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        mr_property_combo_box = component_registry.make_combo_box(
            "mr_property_combo_box",
            make_reservation_tile.content_grid,
            values=["Select Property"],
            font=("Roboto", 16),
        )
        mr_property_combo_box.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        mr_start_date_entry = component_registry.make_entry(
            "mr_start_date_entry",
            make_reservation_tile.content_grid,
            placeholder_text="Start Date",
            font=("Roboto", 16),
        )
        mr_start_date_entry.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        mr_end_date_entry = component_registry.make_entry(
            "mr_end_date_entry",
            make_reservation_tile.content_grid,
            placeholder_text="End Date",
            font=("Roboto", 16),
        )
        mr_end_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        mr_submit_button = component_registry.make_button(
            "mr_submit_button",
            make_reservation_tile.content_grid,
            text="Submit",
            font=("Roboto", 16),
        )
        mr_submit_button.grid(row=2, columnspan=2, padx=10, pady=10, sticky="nsew")
        make_reservation_tile.content_grid

        view_reservations_tile = Tile(
            tiles_grid,
            title="View Reservations",
            component_registry=component_registry,
        )
        view_reservations_tile.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        vr_user_combo_box = component_registry.make_combo_box(
            "v_user_combo_box",
            view_reservations_tile.content_grid,
            values=["Select User"],
            font=("Roboto", 16),
        )
        vr_user_combo_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        vr_property_combo_box = component_registry.make_combo_box(
            "v_property_combo_box",
            view_reservations_tile.content_grid,
            values=["Select Property"],
            font=("Roboto", 16),
        )
        vr_property_combo_box.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.vr_table = ScrollableTable(
            view_reservations_tile.content_grid,
            headers=["Property", "Start Date", "End Date"],
            entries=[],
        )
        self.vr_table.grid(row=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        vr_submit_button = component_registry.make_button(
            "v_submit_button",
            view_reservations_tile.content_grid,
            text="Submit",
            font=("Roboto", 16),
        )
        vr_submit_button.grid(row=2, columnspan=2, padx=10, pady=10, sticky="nsew")

        cancel_reservation_tile = Tile(
            tiles_grid,
            title="Cancel Reservation",
            component_registry=component_registry,
        )
        cancel_reservation_tile.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        c_user_combo_box = component_registry.make_combo_box(
            "c_user_combo_box",
            cancel_reservation_tile.content_grid,
            values=["Select User"],
            font=("Roboto", 16),
        )
        c_user_combo_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        c_property_combo_box = component_registry.make_combo_box(
            "c_property_combo_box",
            cancel_reservation_tile.content_grid,
            values=["Select Property"],
            font=("Roboto", 16),
        )
        c_property_combo_box.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        c_submit_button = component_registry.make_button(
            "c_submit_button",
            cancel_reservation_tile.content_grid,
            text="Submit",
            font=("Roboto", 16),
        )
        c_submit_button.grid(row=2, columnspan=2, padx=10, pady=10, sticky="nsew")

        update_reservation_tile = Tile(
            tiles_grid,
            title="Update Reservation",
            component_registry=component_registry,
        )
        update_reservation_tile.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        u_user_combo_box = component_registry.make_combo_box(
            "u_user_combo_box",
            update_reservation_tile.content_grid,
            values=["Select User"],
            font=("Roboto", 16),
        )
        u_user_combo_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        u_property_combo_box = component_registry.make_combo_box(
            "u_property_combo_box",
            update_reservation_tile.content_grid,
            values=["Select Property"],
            font=("Roboto", 16),
        )
        u_property_combo_box.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        u_start_date_entry = component_registry.make_entry(
            "u_start_date_entry",
            update_reservation_tile.content_grid,
            placeholder_text="Start Date",
            font=("Roboto", 16),
        )
        u_start_date_entry.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        u_end_date_entry = component_registry.make_entry(
            "u_end_date_entry",
            update_reservation_tile.content_grid,
            placeholder_text="End Date",
            font=("Roboto", 16),
        )
        u_end_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        u_submit_button = component_registry.make_button(
            "u_submit_button",
            update_reservation_tile.content_grid,
            text="Submit",
            font=("Roboto", 16),
        )
        u_submit_button.grid(row=2, columnspan=2, padx=10, pady=10, sticky="nsew")

    def setup_testing_panel(self, component_registry: ComponentRegistry) -> None:
        result_grid = ctk.CTkFrame(self.testing_panel.right_frame)
        result_grid.grid(padx=10, pady=10, sticky="nsew")
        result_grid.columnconfigure(0, weight=1)
        result_grid.columnconfigure(1, weight=1)

        successful_label = ctk.CTkLabel(
            result_grid,
            text="Successful Processes",
            font=("Roboto", 16, "bold"),
            justify="left",
        )
        successful_label.grid(row=0, column=0, padx=30, pady=10, sticky="nsw")

        successful_value = component_registry.make_label(
            "successful_processes",
            result_grid,
            text="0/0",
            font=("Roboto", 16),
        )

        successful_value.grid(row=0, column=1, padx=30, pady=10, sticky="nse")
