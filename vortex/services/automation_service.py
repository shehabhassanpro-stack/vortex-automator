"""
Automation Service managing execution worker threads, timing loops, and state machines.
"""

import threading
import time
from typing import Callable, Optional
from vortex.core.direct_input import DirectInputEngine
from vortex.core.scan_codes import resolve_scan_code
from vortex.services.sound_service import SoundService

class AutomationService:
    def __init__(self, on_state_changed: Optional[Callable[[bool], None]] = None):
        self._is_running = False
        self._on_state_changed = on_state_changed
        self._worker_thread: Optional[threading.Thread] = None
        self._held_key_info: Optional[tuple[int, bool]] = None

    @property
    def is_running(self) -> bool:
        return self._is_running

    def start_keyboard(self, key_str: str, mode: str, interval: float) -> bool:
        """Starts keyboard automation. Returns False if key cannot be resolved."""
        scan, extended = resolve_scan_code(key_str)
        if scan is None:
            return False

        self._is_running = True
        SoundService.play_start()
        
        if self._on_state_changed:
            self._on_state_changed(True)

        self._worker_thread = threading.Thread(
            target=self._run_keyboard_loop,
            args=(scan, extended, mode, interval),
            daemon=True
        )
        self._worker_thread.start()
        return True

    def start_mouse(self, button: str, interval: float) -> None:
        """Starts mouse click automation."""
        self._is_running = True
        SoundService.play_start()

        if self._on_state_changed:
            self._on_state_changed(True)

        self._worker_thread = threading.Thread(
            target=self._run_mouse_loop,
            args=(button, interval),
            daemon=True
        )
        self._worker_thread.start()

    def stop(self) -> None:
        """Gracefully halts automation and releases held keys."""
        if not self._is_running:
            return

        self._is_running = False
        SoundService.play_stop()

        # Immediate release of any held down keys
        if self._held_key_info:
            scan, extended = self._held_key_info
            DirectInputEngine.send_key_up(scan, extended)
            self._held_key_info = None

        if self._on_state_changed:
            self._on_state_changed(False)

    def _run_keyboard_loop(self, scan: int, extended: bool, mode: str, interval: float) -> None:
        if mode == "hold":
            self._held_key_info = (scan, extended)
            DirectInputEngine.send_key_down(scan, extended)
            while self._is_running:
                time.sleep(0.08)
            DirectInputEngine.send_key_up(scan, extended)
            self._held_key_info = None
        else:
            while self._is_running:
                DirectInputEngine.send_key_down(scan, extended)
                time.sleep(0.04)
                DirectInputEngine.send_key_up(scan, extended)
                time.sleep(max(0.01, interval))

    def _run_mouse_loop(self, button: str, interval: float) -> None:
        while self._is_running:
            DirectInputEngine.send_mouse_click(button)
            time.sleep(max(0.01, interval))
