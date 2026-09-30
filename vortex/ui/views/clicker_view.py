"""
Mouse Clicker View card component.
"""

from typing import Callable
import customtkinter as ctk
from vortex.config.theme import (
    COLOR_TEXT, COLOR_TEXT_MUTED, COLOR_SURFACE, COLOR_SURFACE_LIGHT,
    COLOR_BORDER, COLOR_ACCENT, COLOR_ACCENT_HOVER, FONT_FAMILY
)

class ClickerView(ctk.CTkFrame):
    def __init__(self, master, on_bind_clicked: Callable[[], None]):
        super().__init__(master, fg_color="transparent")
        self._on_bind_clicked = on_bind_clicked

        # Row 1: Mouse Button
        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 14))

        lbl1 = ctk.CTkLabel(row1, text="Mouse Button", font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), text_color=COLOR_TEXT)
        lbl1.pack(side="left")

        self.mouse_btn_var = ctk.StringVar(value="Left")
        self.mouse_menu = ctk.CTkOptionMenu(
            row1, values=["Left", "Right", "Middle"], variable=self.mouse_btn_var,
            width=110, height=36, corner_radius=8,
            fg_color=COLOR_SURFACE_LIGHT, button_color=COLOR_ACCENT,
            button_hover_color=COLOR_ACCENT_HOVER, dropdown_fg_color=COLOR_SURFACE,
            dropdown_hover_color=COLOR_BORDER, font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            dropdown_font=ctk.CTkFont(family=FONT_FAMILY, size=12)
        )
        self.mouse_menu.pack(side="right")

        # Row 2: Interval Slider
        delay_container = ctk.CTkFrame(self, fg_color="transparent")
        delay_container.pack(fill="x", pady=(0, 14))

        delay_header = ctk.CTkFrame(delay_container, fg_color="transparent")
        delay_header.pack(fill="x", pady=(0, 6))

        lbl2 = ctk.CTkLabel(delay_header, text="Click Interval", font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), text_color=COLOR_TEXT)
        lbl2.pack(side="left")

        self.delay_val_lbl = ctk.CTkLabel(
            delay_header, text="1.00s",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=COLOR_ACCENT
        )
        self.delay_val_lbl.pack(side="right")

        self.delay_var = ctk.DoubleVar(value=1.0)
        self.delay_slider = ctk.CTkSlider(
            delay_container, from_=0.05, to=5.0, number_of_steps=99,
            variable=self.delay_var, height=18,
            fg_color=COLOR_SURFACE_LIGHT, progress_color=COLOR_ACCENT,
            button_color=COLOR_ACCENT, button_hover_color=COLOR_ACCENT_HOVER,
            command=lambda v: self.delay_val_lbl.configure(text=f"{v:.2f}s")
        )
        self.delay_slider.pack(fill="x")

        # Row 3: Hotkey
        row3 = ctk.CTkFrame(self, fg_color="transparent")
        row3.pack(fill="x", pady=(8, 0))

        lbl3 = ctk.CTkLabel(row3, text="Toggle Hotkey", font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), text_color=COLOR_TEXT)
        lbl3.pack(side="left")

        self.btn_bind = ctk.CTkButton(
            row3, text="[ F6 ]", width=90, height=34,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            fg_color=COLOR_SURFACE_LIGHT, text_color=COLOR_ACCENT,
            border_width=1, border_color=COLOR_BORDER, hover_color=COLOR_BORDER,
            corner_radius=8, command=self._on_bind_clicked
        )
        self.btn_bind.pack(side="right")

    def set_hotkey_text(self, text: str) -> None:
        self.btn_bind.configure(text=text, text_color=COLOR_ACCENT)

    def set_binding_prompt(self) -> None:
        self.btn_bind.configure(text="Press key...", text_color="#FBBF24")
