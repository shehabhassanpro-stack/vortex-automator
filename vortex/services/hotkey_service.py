"""
Hotkey Service managing global keyboard hooks and hotkey resolution.
"""

from typing import Callable, Any
from pynput import keyboard

ARABIC_TO_ENGLISH_KEY = {
    'ض': 'Q', 'ص': 'W', 'ث': 'E', 'ق': 'R', 'ف': 'T', 'غ': 'Y',
    'ع': 'U', 'ه': 'I', 'خ': 'O', 'ح': 'P', 'ج': '[', 'د': ']',
    'ش': 'A', 'س': 'S', 'ي': 'D', 'ب': 'F', 'ل': 'G', 'ا': 'H',
    'ت': 'J', 'ن': 'K', 'م': 'L', 'ك': ';', 'ط': "'",
    'ئ': 'Z', 'ء': 'X', 'ؤ': 'C', 'ر': 'V', 'لا': 'B', 'ى': 'N',
    'ة': 'M', 'و': ',', 'ز': '.', 'ظ': '/',
}

class HotkeyService:
    def __init__(self, on_hotkey_pressed: Callable[[Any], None]):
        self._callback = on_hotkey_pressed
        self._listener = keyboard.Listener(on_press=self._handle_press)
        self._listener.start()

    def _handle_press(self, key: Any) -> None:
        if self._callback:
            self._callback(key)

    @staticmethod
    def format_key_name(key: Any) -> str:
        """Standardizes a key object into a human-readable display string, normalizing Arabic layout to physical key."""
        if hasattr(key, 'name') and key.name:
            return key.name.upper()
        if hasattr(key, 'char') and key.char:
            char = key.char
            if char in ARABIC_TO_ENGLISH_KEY:
                return ARABIC_TO_ENGLISH_KEY[char]
            return char.upper()
        return str(key).replace("'", "").upper()

    @staticmethod
    def matches(event_key: Any, target_key: Any) -> bool:
        """Determines if a triggered key event matches a target key binding."""
        if event_key == target_key:
            return True
        if hasattr(event_key, 'name') and hasattr(target_key, 'name'):
            if event_key.name and target_key.name and event_key.name.lower() == target_key.name.lower():
                return True
        if hasattr(event_key, 'vk') and hasattr(target_key, 'vk'):
            if event_key.vk and target_key.vk and event_key.vk == target_key.vk:
                return True
        if hasattr(event_key, 'char') and hasattr(target_key, 'char'):
            if event_key.char and target_key.char and event_key.char.lower() == target_key.char.lower():
                return True
        return False
