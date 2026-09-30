"""
Keyboard Presser View card component.
Provides interactive single-key binding for the target key and toggle hotkey.
"""

from typing import Callable
import customtkinter as ctk
from vortex.config.theme import (
    COLOR_TEXT, COLOR_TEXT_MUTED, COLOR_SURFACE_LIGHT,
    COLOR_BORDER, COLOR_ACCENT, COLOR_ACCENT_HOVER, COLOR_BG, FONT_FAMILY
)

class PresserView(ctk.CTkFrame):
    def __init__(
        self, 
        master, 
        on_target_bind_clicked: Callable[[], None],
        on_hotkey_bind_clicked: Callable[[], None]
    ):
        super().__init__(master, fg_color="transparent")
        self._on_target_bind_clicked = on_target_bind_clicked
        self._on_hotkey_bind_clicked = on_hotkey_bind_clicked

        # Row 1: Target Key (Single Key Selector)
        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 14))

        lbl1 = ctk.CTkLabel(row1, text="Target Key", font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), text_color=COLOR_TEXT)
        lbl1.pack(side="left")

        desc1 = ctk.CTkLabel(row1, text="(Click to set key)", font=ctk.CTkFont(size=11), text_color=COLOR_TEXT_MUTED)
        desc1.pack(side="left", padx=(6, 0))

        self.btn_target = ctk.CTkButton(
            row1, text="[ E ]", width=90, height=36,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            fg_color=COLOR_SURFACE_LIGHT, text_color=COLOR_ACCENT,
            border_width=1, border_color=COLOR_BORDER, hover_color=COLOR_BORDER,
            corner_radius=8, command=self._on_target_bind_clicked
        )
        self.btn_target.pack(side="right")

        # Row 2: Mode Selector
        row2 = ctk.CTkFrame(self, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 14))

        lbl2 = ctk.CTkLabel(row2, text="Press Mode", font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), text_color=COLOR_TEXT)
        lbl2.pack(side="left")

        self.mode_var = ctk.StringVar(value="repeat")

        mode_box = ctk.CTkFrame(row2, fg_color=COLOR_SURFACE_LIGHT, corner_radius=8, height=36)
        mode_box.pack(side="right")

        self.btn_mode_repeat = ctk.CTkButton(
            mode_box, text="Repeat", width=70, height=28, corner_radius=6,
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            fg_color=COLOR_ACCENT, text_color=COLOR_BG, hover_color=COLOR_ACCENT_HOVER,
            command=lambda: self.set_mode("repeat")
        )
        self.btn_mode_repeat.pack(side="left", padx=3, pady=3)

        self.btn_mode_hold = ctk.CTkButton(
            mode_box, text="Hold Key", width=70, height=28, corner_radius=6,
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            fg_color="transparent", text_color=COLOR_TEXT_MUTED, hover_color=COLOR_BORDER,
            command=lambda: self.set_mode("hold")
        )
        self.btn_mode_hold.pack(side="left", padx=(0, 3), pady=3)

        # Row 3: Interval Slider
        self.delay_container = ctk.CTkFrame(self, fg_color="transparent")
        self.delay_container.pack(fill="x", pady=(0, 14))

        delay_header = ctk.CTkFrame(self.delay_container, fg_color="transparent")
        delay_header.pack(fill="x", pady=(0, 6))

        lbl3 = ctk.CTkLabel(delay_header, text="Click Interval", font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), text_color=COLOR_TEXT)
        lbl3.pack(side="left")

        self.delay_val_lbl = ctk.CTkLabel(
            delay_header, text="1.00s",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=COLOR_ACCENT
        )
        self.delay_val_lbl.pack(side="right")

        self.delay_var = ctk.DoubleVar(value=1.0)
        self.delay_slider = ctk.CTkSlider(
            self.delay_container, from_=0.05, to=5.0, number_of_steps=99,
            variable=self.delay_var, height=18,
            fg_color=COLOR_SURFACE_LIGHT, progress_color=COLOR_ACCENT,
            button_color=COLOR_ACCENT, button_hover_color=COLOR_ACCENT_HOVER,
            command=lambda v: self.delay_val_lbl.configure(text=f"{v:.2f}s")
        )
        self.delay_slider.pack(fill="x")

        # Row 4: Toggle Hotkey
        row4 = ctk.CTkFrame(self, fg_color="transparent")
        row4.pack(fill="x", pady=(8, 0))

        lbl4 = ctk.CTkLabel(row4, text="Toggle Hotkey", font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), text_color=COLOR_TEXT)
        lbl4.pack(side="left")

        self.btn_hotkey = ctk.CTkButton(
            row4, text="[ F7 ]", width=90, height=34,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            fg_color=COLOR_SURFACE_LIGHT, text_color=COLOR_ACCENT,
            border_width=1, border_color=COLOR_BORDER, hover_color=COLOR_BORDER,
            corner_radius=8, command=self._on_hotkey_bind_clicked
        )
        self.btn_hotkey.pack(side="right")

    def set_mode(self, mode: str) -> None:
        self.mode_var.set(mode)
        if mode == "repeat":
            self.btn_mode_repeat.configure(fg_color=COLOR_ACCENT, text_color=COLOR_BG, font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"))
            self.btn_mode_hold.configure(fg_color="transparent", text_color=COLOR_TEXT_MUTED, font=ctk.CTkFont(family=FONT_FAMILY, size=11))
            self.delay_slider.configure(state="normal")
            self.delay_val_lbl.configure(text_color=COLOR_ACCENT)
        else:
            self.btn_mode_hold.configure(fg_color=COLOR_ACCENT, text_color=COLOR_BG, font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"))
            self.btn_mode_repeat.configure(fg_color="transparent", text_color=COLOR_TEXT_MUTED, font=ctk.CTkFont(family=FONT_FAMILY, size=11))
            self.delay_slider.configure(state="disabled")
            self.delay_val_lbl.configure(text_color=COLOR_TEXT_MUTED)

    # Target Key UI State Methods
    def set_target_key_text(self, text: str) -> None:
        self.btn_target.configure(text=text, text_color=COLOR_ACCENT)

    def set_target_binding_prompt(self) -> None:
        self.btn_target.configure(text="Press key...", text_color="#FBBF24")

    # Hotkey UI State Methods
    def set_hotkey_text(self, text: str) -> None:
        self.btn_hotkey.configure(text=text, text_color=COLOR_ACCENT)

    def set_hotkey_binding_prompt(self) -> None:
        self.btn_hotkey.configure(text="Press key...", text_color="#FBBF24")
