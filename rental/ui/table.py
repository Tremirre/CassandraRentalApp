import customtkinter as ctk

from tkinter import ttk


class ScrollableTable(ctk.CTkFrame):
    def __init__(self, parent, entries, headers):
        super().__init__(parent)
        self.entries = entries
        self.headers = headers

        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True)

        self.setup_table()

    def setup_table(self):
        # Create a treeview widget
        self.treeview = ttk.Treeview(
            self.table_frame, columns=self.headers, show="headings"
        )

        # Configure columns
        for header in self.headers:
            self.treeview.heading(header, text=header)
            self.treeview.column(header, stretch=True, width=100)

        # Add entries to the table
        self.update_entries()

        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(
            self.table_frame, orient="vertical", command=self.treeview.yview
        )
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # Pack the treeview and scrollbar
        self.treeview.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_entries(self):
        # Clear existing entries
        self.treeview.delete(*self.treeview.get_children())

        # Add new entries to the table
        for entry in self.entries:
            self.treeview.insert("", "end", values=entry)
