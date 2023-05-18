import customtkinter as ctk


class LoadingBox(ctk.CTk):
    def __init__(self, title: str = "Loading..."):
        super().__init__()
        self.title(title)
        self.geometry("400x150")
        self.resizable(False, False)
        self.base_frame = ctk.CTkFrame(self)
        self.base_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.status_label = ctk.CTkLabel(self.base_frame, text="0%")
        self.status_label.pack(fill="both", expand=True, padx=10, pady=10)

        self.progress_bar = ctk.CTkProgressBar(self.base_frame)
        self.progress_bar.pack(fill="both", expand=True, padx=10, pady=20)

    def set_progress(self, progress: float, status: str = ""):
        self.progress_bar.set(progress)
        self.status_label.configure(text=f"{progress * 100:.0f}% {status}")

    def start(self):
        self.focus_force()
        self.mainloop()
