"""
Header component with brand typography and geometric status capsule.
"""

import customtkinter as ctk
from vortex.config.theme import (
    COLOR_BG, COLOR_SURFACE, COLOR_BORDER, COLOR_TEXT,
    COLOR_TEXT_MUTED, COLOR_ACTIVE, COLOR_INACTIVE, FONT_FAMILY
)

class HeaderComponent(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_BG)
        self.pack(fill="x", padx=28, pady=(24, 16))

        # Title Block
        title_box = ctk.CTkFrame(self, fg_color="transparent")
        title_box.pack(side="left")

        title_lbl = ctk.CTkLabel(
            title_box, text="VORTEX AUTOMATOR",
            font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"),
            text_color=COLOR_TEXT
        )
        title_lbl.pack(anchor="w")

        sub_lbl = ctk.CTkLabel(
            title_box, text="Universal Key Presser & Auto Clicker",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLOR_TEXT_MUTED
        )
        sub_lbl.pack(anchor="w")

        # Mathematically Perfect Status Pill Capsule
        self.status_badge = ctk.CTkFrame(
            self, fg_color=COLOR_SURFACE, bg_color=COLOR_BG,
            corner_radius=14, height=28, width=105,
            border_width=1, border_color=COLOR_BORDER
        )
        self.status_badge.pack(side="right")
        self.status_badge.pack_propagate(False)

        badge_inner = ctk.CTkFrame(self.status_badge, fg_color=COLOR_SURFACE, bg_color=COLOR_SURFACE)
        badge_inner.place(relx=0.5, rely=0.5, anchor="center")

        self.status_dot = ctk.CTkLabel(
            badge_inner, text="●",
            font=ctk.CTkFont(size=10), text_color=COLOR_INACTIVE, width=12
        )
        self.status_dot.pack(side="left", padx=(0, 4))

        self.status_text = ctk.CTkLabel(
            badge_inner, text="STANDBY",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            text_color=COLOR_TEXT_MUTED
        )
        self.status_text.pack(side="left")

    def set_running(self, running: bool) -> None:
        """Updates the status pill badge visually."""
        if running:
            self.status_dot.configure(text_color=COLOR_ACTIVE)
            self.status_text.configure(text="RUNNING", text_color=COLOR_ACTIVE)
            self.status_badge.configure(border_color=COLOR_ACTIVE)
        else:
            self.status_dot.configure(text_color=COLOR_INACTIVE)
            self.status_text.configure(text="STANDBY", text_color=COLOR_TEXT_MUTED)
            self.status_badge.configure(border_color=COLOR_BORDER)
