"""
DirectInput Engine for low-level hardware input simulation.
Interacts with Windows user32.dll using SendInput and mouse_event.
"""

import ctypes
import time
from vortex.core.win32_structures import (
    user32, Input, Input_I, KeyBdInput,
    KEYEVENTF_SCANCODE, KEYEVENTF_KEYUP, KEYEVENTF_EXTENDEDKEY,
    MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP,
    MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP,
    MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP
)

class DirectInputEngine:
    @staticmethod
    def send_key_down(scan_code: int, extended: bool = False) -> None:
        """Sends a hardware key-down event."""
        extra = ctypes.c_ulong(0)
        flags = KEYEVENTF_SCANCODE
        if extended:
            flags |= KEYEVENTF_EXTENDEDKEY
            
        ii = Input_I()
        ii.ki = KeyBdInput(0, scan_code, flags, 0, ctypes.pointer(extra))
        input_event = Input(1, ii)
        user32.SendInput(1, ctypes.pointer(input_event), ctypes.sizeof(input_event))

    @staticmethod
    def send_key_up(scan_code: int, extended: bool = False) -> None:
        """Sends a hardware key-up event."""
        extra = ctypes.c_ulong(0)
        flags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP
        if extended:
            flags |= KEYEVENTF_EXTENDEDKEY
            
        ii = Input_I()
        ii.ki = KeyBdInput(0, scan_code, flags, 0, ctypes.pointer(extra))
        input_event = Input(1, ii)
        user32.SendInput(1, ctypes.pointer(input_event), ctypes.sizeof(input_event))

    @staticmethod
    def send_mouse_click(button: str = 'Left', hold_duration: float = 0.04) -> None:
        """Sends a hardware mouse click event."""
        btn_lower = button.strip().lower()
        
        if btn_lower == 'left':
            down_flag, up_flag = MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
        elif btn_lower == 'right':
            down_flag, up_flag = MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP
        elif btn_lower == 'middle':
            down_flag, up_flag = MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP
        else:
            down_flag, up_flag = MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP

        user32.mouse_event(down_flag, 0, 0, 0, 0)
        time.sleep(hold_duration)
        user32.mouse_event(up_flag, 0, 0, 0, 0)
