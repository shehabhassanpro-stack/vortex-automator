"""
Hardware DirectInput Scan Code mappings.
Ensures layout-independent physical key mapping (supporting English QWERTY and Arabic layouts).
"""

import ctypes

user32 = ctypes.windll.user32

HARDWARE_SCAN_CODES = {
    # Latin Characters (QWERTY layout physical codes)
    'a': 0x1E, 'b': 0x30, 'c': 0x2E, 'd': 0x20, 'e': 0x12, 'f': 0x21,
    'g': 0x22, 'h': 0x23, 'i': 0x17, 'j': 0x24, 'k': 0x25, 'l': 0x26,
    'm': 0x32, 'n': 0x31, 'o': 0x18, 'p': 0x19, 'q': 0x10, 'r': 0x13,
    's': 0x1F, 't': 0x14, 'u': 0x16, 'v': 0x2F, 'w': 0x11, 'x': 0x2D,
    'y': 0x15, 'z': 0x2C,

    # Arabic Physical Key Layout Equivalents
    'ض': 0x10, 'ص': 0x11, 'ث': 0x12, 'ق': 0x13, 'ف': 0x14, 'غ': 0x15,
    'ع': 0x16, 'ه': 0x17, 'خ': 0x18, 'ح': 0x19, 'ج': 0x1A, 'د': 0x1B,
    'ش': 0x1E, 'س': 0x1F, 'ي': 0x20, 'ب': 0x21, 'ل': 0x22, 'ا': 0x23,
    'ت': 0x24, 'ن': 0x25, 'م': 0x26, 'ك': 0x27, 'ط': 0x28, 'ئ': 0x2C,
    'ء': 0x2D, 'ؤ': 0x2E, 'ر': 0x2F, 'لا': 0x30, 'ى': 0x31, 'ة': 0x32,
    'و': 0x33, 'ز': 0x34, 'ظ': 0x35,

    # Top Row Numbers
    '1': 0x02, '2': 0x03, '3': 0x04, '4': 0x05, '5': 0x06,
    '6': 0x07, '7': 0x08, '8': 0x09, '9': 0x0A, '0': 0x0B,

    # Modifier & Control Keys
    'space': 0x39, 'spc': 0x39, 'مسافة': 0x39,
    'enter': 0x1C, 'return': 0x1C, 'انتر': 0x1C,
    'tab': 0x0F,
    'esc': 0x01, 'escape': 0x01,
    'backspace': 0x0E,
    'shift': 0x2A, 'lshift': 0x2A, 'rshift': 0x36,
    'ctrl': 0x1D, 'lctrl': 0x1D,
    'alt': 0x38, 'lalt': 0x38,
    'capslock': 0x3A,

    # Directional Arrows (requires extended key flag)
    'up': (0x48, True), 'down': (0x50, True),
    'left': (0x4B, True), 'right': (0x4D, True),

    # Function Keys
    'f1': 0x3B, 'f2': 0x3C, 'f3': 0x3D, 'f4': 0x3E,
    'f5': 0x3F, 'f6': 0x40, 'f7': 0x41, 'f8': 0x42,
    'f9': 0x43, 'f10': 0x44, 'f11': 0x57, 'f12': 0x58,
}

def resolve_scan_code(key_str: str) -> tuple[int | None, bool]:
    """
    Resolves an input string to its hardware scan code and extended key status.
    Returns: (scan_code, is_extended)
    """
    clean_key = key_str.strip().lower()
    
    if clean_key in HARDWARE_SCAN_CODES:
        val = HARDWARE_SCAN_CODES[clean_key]
        if isinstance(val, tuple):
            return val
        return val, False

    # Dynamic fallback to Windows API
    if len(clean_key) == 1:
        vk = user32.VkKeyScanW(ord(clean_key)) & 0xFF
        if vk != 0xFF:
            scan = user32.MapVirtualKeyW(vk, 0)
            if scan != 0:
                return scan, False

    return None, False
