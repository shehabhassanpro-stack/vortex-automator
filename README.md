<div align="center">

# ⚡ Vortex Automator
### Universal High-Performance Key Presser & Auto Clicker for Windows

[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![UI](https://img.shields.io/badge/UI-CustomTkinter-D4AF37?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20Layered-22C55E?style=for-the-badge)](SYSTEM.md)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

**Vortex Automator** is a modern, minimalist, enterprise-grade automation utility for Windows. Built using hardware-level **DirectInput ScanCodes** (`SendInput`), it reliably works across all desktop applications, full-screen games (DirectX, GTA/FiveM, Unity, Unreal Engine), and web environments without being affected by system keyboard language layouts.

</div>

---

## ✨ Features

- 🎮 **Hardware DirectInput Engine:** Injects raw physical scan codes via the Windows `user32.dll` API. Bypasses standard virtual-key limitations and works across all DirectX/OpenGL full-screen games.
- 🎨 **Minimalist 3-Color Design System:** Designed following modern UI/UX engineering standards (60-30-10 palette: Obsidian Black, Card Slate, Champagne Gold) for maximum visual elegance and eye comfort.
- ⌨ **Dual Keyboard Modes:**
  - **Repeat Mode:** Continuously pulses keys at custom time intervals (from 0.05s to 5.00s).
  - **Hold Key Mode:** Holds down a key continuously until toggled off (ideal for long-press game interactions like *"Hold E"*).
- 🖱 **Auto Clicker:** Supports Left, Right, and Middle mouse button automation with sub-second interval adjustments.
- 🎯 **Global Hotkeys:** Fully customizable toggle hotkeys (default: `F7` for Presser, `F6` for Clicker) with real-time audio confirmation beeps.
- 🌐 **Layout Independent:** Native support for both English (QWERTY) and Arabic keyboard input layouts mapped directly to physical key positions.
- 🛡 **UAC Admin Embedded:** Built with elevated administrator manifests to ensure input delivery even to games running with administrator rights.

---

## 🏛 Clean Architecture & Project Structure

The project strictly follows Clean Architecture and SOLID design principles, dividing the code into decoupled layers:

```
Auto presser/
├── vortex/
│   ├── config/
│   │   └── theme.py               # 60-30-10 Design tokens and typography
│   ├── core/
│   │   ├── win32_structures.py    # Win32 ctypes C-structs & unions
│   │   ├── scan_codes.py          # DirectInput hardware scan code mappings
│   │   └── direct_input.py        # Raw SendInput & mouse_event engine
│   ├── services/
│   │   ├── automation_service.py  # Threaded worker loops & state machine
│   │   ├── hotkey_service.py      # Low-level Windows keyboard hook service
│   │   └── sound_service.py       # Asynchronous non-blocking audio cues
│   └── ui/
│       ├── components/
│       │   └── header.py          # Brand typography & status capsule
│       ├── views/
│       │   ├── presser_view.py    # Keyboard presser card component
│       │   └── clicker_view.py    # Mouse clicker card component
│       └── main_window.py         # Main UI orchestration window
├── main.py                        # Minimalist bootstrap entry point
├── SYSTEM.md                      # Comprehensive systems architecture specification
├── AUDIT_REPORT.md                # Engineering audit & quality analysis report
└── requirements.txt               # Lightweight dependency manifest
```

For an in-depth breakdown of the Win32 input pipeline, threading synchronization, and state diagrams, read [SYSTEM.md](SYSTEM.md). For the code quality review, read [AUDIT_REPORT.md](AUDIT_REPORT.md).

---

## 🚀 Quick Start (Pre-built Executable)

1. Grab **`Vortex.exe`** from the root or Releases section.
2. Double-click **`Vortex.exe`** (it will automatically request Administrator privileges to interact with elevated game windows).
3. Select your desired key/button and mode, then press the hotkey to activate!

---

## 🛠 Running from Source

### Prerequisites
- Python 3.10 or newer
- Windows 10 / 11 (64-bit)

### Installation
```bash
# Clone the repository
git clone https://github.com/your-username/vortex-automator.git
cd vortex-automator

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 📦 Building Standalone Executable (.exe)

You can package Vortex into a single, self-contained Windows `.exe` using PyInstaller:

```bash
python -m PyInstaller --noconsole --onefile --uac-admin --collect-all customtkinter main.py --name "Vortex"
```

The output will be placed in the `dist/` directory as `Vortex.exe`.

---

## 📐 Design Philosophy

| Layer | Color | Purpose |
| :--- | :--- | :--- |
| **Primary (60%)** | `#0B0D11` | Obsidian black canvas for deep contrast and eye comfort |
| **Secondary (30%)** | `#161920` | Slate surface cards and panels for clear visual hierarchy |
| **Accent (10%)** | `#D4AF37` | Champagne Gold for active states, CTA buttons, and indicators |

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
