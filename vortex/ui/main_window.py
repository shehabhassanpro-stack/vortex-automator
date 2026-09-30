"""
Main Application Window orchestrating views, services, and state.
"""

from typing import Any, Optional
import customtkinter as ctk
from pynput import keyboard

from vortex.config.theme import (
    COLOR_BG, COLOR_SURFACE, COLOR_SURFACE_LIGHT, COLOR_BORDER,
    COLOR_ACCENT, COLOR_ACCENT_HOVER, COLOR_INACTIVE, COLOR_TEXT_MUTED, FONT_FAMILY
)
from vortex.services.automation_service import AutomationService
from vortex.services.hotkey_service import HotkeyService
from vortex.ui.components.header import HeaderComponent
from vortex.ui.views.presser_view import PresserView
from vortex.ui.views.clicker_view import ClickerView

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.title("Vortex - Auto Presser & Clicker")
        self.geometry("480x560")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)

        # Core Services
        self._automation = AutomationService(on_state_changed=self._on_automation_state_changed)
        self._hotkeys = HotkeyService(on_hotkey_pressed=self._on_global_hotkey)

        # State
        self._current_tab = "presser"  # "presser" | "clicker"
        self._target_key_name = "e"
        self._presser_hotkey = keyboard.Key.f7
        self._clicker_hotkey = keyboard.Key.f6
        self._binding_target: Optional[str] = None

        self._build_ui()

    def _build_ui(self) -> None:
        # 1. Header Bar with Status Pill
        self.header = HeaderComponent(self)

        # 2. Segmented Navigation Switcher
        nav_frame = ctk.CTkFrame(self, fg_color=COLOR_SURFACE, corner_radius=12, height=44)
        nav_frame.pack(fill="x", padx=28, pady=(0, 16))
        nav_frame.pack_propagate(False)

        self.btn_nav_presser = ctk.CTkButton(
            nav_frame, text="Keyboard Presser",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            fg_color=COLOR_ACCENT, text_color=COLOR_BG, hover_color=COLOR_ACCENT_HOVER,
            corner_radius=10, command=lambda: self._switch_tab("presser")
        )
        self.btn_nav_presser.pack(side="left", fill="both", expand=True, padx=4, pady=4)

        self.btn_nav_clicker = ctk.CTkButton(
            nav_frame, text="Mouse Clicker",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color="transparent", text_color=COLOR_TEXT_MUTED, hover_color=COLOR_SURFACE_LIGHT,
            corner_radius=10, command=lambda: self._switch_tab("clicker")
        )
        self.btn_nav_clicker.pack(side="left", fill="both", expand=True, padx=4, pady=4)

        # 3. Main Card Container
        self.card = ctk.CTkFrame(
            self, fg_color=COLOR_SURFACE, corner_radius=16,
            border_width=1, border_color=COLOR_BORDER
        )
        self.card.pack(fill="both", expand=True, padx=28, pady=(0, 20))

        self.content_container = ctk.CTkFrame(self.card, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Initialize Views
        self.presser_view = PresserView(
            self.content_container,
            on_target_bind_clicked=lambda: self._start_binding("target_key"),
            on_hotkey_bind_clicked=lambda: self._start_binding("presser_hotkey")
        )
        self.clicker_view = ClickerView(
            self.content_container,
            on_bind_clicked=lambda: self._start_binding("clicker_hotkey")
        )

        # 4. Big Action Button
        self.btn_action = ctk.CTkButton(
            self, text="START (F7)",
            font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold"),
            fg_color=COLOR_ACCENT, text_color=COLOR_BG,
            hover_color=COLOR_ACCENT_HOVER, corner_radius=12, height=52,
            command=self._toggle_execution
        )
        self.btn_action.pack(fill="x", padx=28, pady=(0, 24))

        # Show default view
        self._switch_tab("presser")

    def _switch_tab(self, tab: str) -> None:
        if self._automation.is_running:
            self._automation.stop()

        self._current_tab = tab
        if tab == "presser":
            self.clicker_view.pack_forget()
            self.presser_view.pack(fill="both", expand=True)

            self.btn_nav_presser.configure(fg_color=COLOR_ACCENT, text_color=COLOR_BG, font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"))
            self.btn_nav_clicker.configure(fg_color="transparent", text_color=COLOR_TEXT_MUTED, font=ctk.CTkFont(family=FONT_FAMILY, size=13))
            
            key_name = HotkeyService.format_key_name(self._presser_hotkey)
            self.btn_action.configure(text=f"START ({key_name})")
        else:
            self.presser_view.pack_forget()
            self.clicker_view.pack(fill="both", expand=True)

            self.btn_nav_clicker.configure(fg_color=COLOR_ACCENT, text_color=COLOR_BG, font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"))
            self.btn_nav_presser.configure(fg_color="transparent", text_color=COLOR_TEXT_MUTED, font=ctk.CTkFont(family=FONT_FAMILY, size=13))
            
            key_name = HotkeyService.format_key_name(self._clicker_hotkey)
            self.btn_action.configure(text=f"START ({key_name})")

    def _toggle_execution(self) -> None:
        if self._automation.is_running:
            self._automation.stop()
        else:
            if self._current_tab == "presser":
                mode = self.presser_view.mode_var.get()
                interval = self.presser_view.delay_var.get()
                success = self._automation.start_keyboard(self._target_key_name, mode, interval)
                if not success:
                    return
            else:
                button = self.clicker_view.mouse_btn_var.get()
                interval = self.clicker_view.delay_var.get()
                self._automation.start_mouse(button, interval)

    def _on_automation_state_changed(self, running: bool) -> None:
        self.header.set_running(running)
        active_key = HotkeyService.format_key_name(
            self._presser_hotkey if self._current_tab == "presser" else self._clicker_hotkey
        )

        if running:
            self.btn_action.configure(
                text=f"STOP ({active_key})",
                fg_color=COLOR_INACTIVE, hover_color="#DC2626", text_color="#FFFFFF"
            )
        else:
            self.btn_action.configure(
                text=f"START ({active_key})",
                fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color=COLOR_BG
            )

    def _start_binding(self, target: str) -> None:
        self._binding_target = target
        if target == "target_key":
            self.presser_view.set_target_binding_prompt()
        elif target == "presser_hotkey":
            self.presser_view.set_hotkey_binding_prompt()
        else:
            self.clicker_view.set_binding_prompt()

    def _on_global_hotkey(self, key: Any) -> None:
        # Handle Interactive Key Binding
        if self._binding_target:
            key_name = HotkeyService.format_key_name(key)
            if self._binding_target == "target_key":
                self._target_key_name = key_name
                self.presser_view.set_target_key_text(f"[ {key_name} ]")
            elif self._binding_target == "presser_hotkey":
                self._presser_hotkey = key
                self.presser_view.set_hotkey_text(f"[ {key_name} ]")
                if self._current_tab == "presser" and not self._automation.is_running:
                    self.btn_action.configure(text=f"START ({key_name})")
            elif self._binding_target == "clicker_hotkey":
                self._clicker_hotkey = key
                self.clicker_view.set_hotkey_text(f"[ {key_name} ]")
                if self._current_tab == "clicker" and not self._automation.is_running:
                    self.btn_action.configure(text=f"START ({key_name})")
            self._binding_target = None
            return

        # Handle Execution Trigger
        active_hotkey = self._presser_hotkey if self._current_tab == "presser" else self._clicker_hotkey
        if HotkeyService.matches(key, active_hotkey):
            self._toggle_execution()
