# 🏛️ Vortex Automator - System Architecture & Technical Specification

**Author:** Vortex Core Engineering Team  
**Specification Level:** High-Performance Windows Systems Engineering  
**Version:** 2.0.0  
**Target Environment:** Windows 10 / Windows 11 (x86_64)

---

## 1. Architectural Philosophy

Vortex Automator is engineered under the principle that **automation utilities must behave identically to physical peripherals** while imposing virtually zero host overhead. Traditional scripting tools often rely on high-level synthetic window messages (`WM_CHAR`, `WM_KEYDOWN`) or virtual key codes (`VK_*`). In modern environments—particularly DirectX/Vulkan game loops and hardware-accelerated browsers—these synthetic inputs are either ignored or dropped.

Vortex bridges this gap by decoupling the application into a **Kernel-Adjacent Core**, an **Asynchronous Service Layer**, and a **Constrained Presentation Boundary**.

```
+-------------------------------------------------------------------------+
|                           Presentation Layer                            |
|             CustomTkinter 60-30-10 Design System (Obsidian/Gold)        |
|     [MainWindow] <--> [PresserView / ClickerView] <--> [HeaderBadge]     |
+-------------------------------------------------------------------------+
                                    |
                         High-Level Domain Events
                                    |
                                    v
+-------------------------------------------------------------------------+
|                              Service Layer                              |
|   - AutomationService (Isolated Thread Daemon / Precision Sleeper)      |
|   - HotkeyService (Global Low-Level Windows Hook / Key Matching)        |
|   - SoundService (Asynchronous Non-Blocking WinSound Worker)            |
+-------------------------------------------------------------------------+
                                    |
                           Driver & Win32 Calls
                                    |
                                    v
+-------------------------------------------------------------------------+
|                               Core Layer                                |
|   - DirectInputEngine (Raw user32.dll SendInput & mouse_event)          |
|   - ScanCode Resolver (Hardware Scancode Matrix & Dynamic API Fallback) |
|   - Win32 C-Structures (KeyBdInput, MouseInput, Input Unions)           |
+-------------------------------------------------------------------------+
                                    |
                           DirectInput Protocol
                                    |
                                    v
+-------------------------------------------------------------------------+
|                         Windows OS Subsystem                            |
|           System Input Queue / RawInput / DirectX Message Loop          |
+-------------------------------------------------------------------------+
```

---

## 2. Low-Level Input Injection Mechanics

### 2.1 Virtual Keys (VK) vs. DirectInput Scan Codes
The Windows input pipeline processes keyboard events in two distinct stages:

1. **Hardware Scan Code (Make/Break Code):** Emitted directly by the keyboard hardware controller or USB HID driver when a key is physically depressed or released.
2. **Virtual Key Translation:** The OS keyboard driver maps the hardware scan code to a virtual key code (`VK_E`, `VK_SPACE`) based on the active software keyboard layout (e.g., US QWERTY vs. Arabic 101).

```
Physical Key Depressed
        │
        ▼
[Hardware Scan Code (e.g., 0x12)] ───► Games / DirectX / RawInput Listen Here
        │
        ▼
[Active Layout Translation]
        │
        ▼
[Virtual Key Code (VK)] ─────────────► Standard Win32 Text Boxes / Notepad
```

**Why Standard Auto-Clickers Fail in Games:**  
Standard tools simulate input at the virtual key layer using `KEYEVENTF_UNICODE` or `wVk`. However:
- Games running DirectInput or polling hardware devices directly inspect the `wScan` field. If `KEYEVENTF_SCANCODE` is missing, the game assumes no physical switch was pressed.
- When a user switches their system layout to Arabic, `VkKeyScanW` fails to map ASCII `'e'`, causing input simulation to silently drop.

**The Vortex Solution:**  
Vortex constructs explicit `INPUT` unions with the `KEYEVENTF_SCANCODE` flag (flag `0x0008`). It bypasses the software layout translation layer entirely, transmitting the raw physical hardware code (e.g., `0x12` for `E`/`ث`) straight to the system input queue.

### 2.2 C-Compatible Structure Memory Layout
Vortex defines 64-bit alignment-safe ctypes structures matching Windows SDK `winuser.h`:

```c
typedef struct tagINPUT {
  DWORD type; // 4 bytes (INPUT_KEYBOARD = 1)
  union {
    MOUSEINPUT    mi;
    KEYBDINPUT    ki;
    HARDWAREINPUT hi;
  } DUMMYUNIONNAME;
} INPUT, *PINPUT;
```

When invoking `user32.SendInput`, the buffer pointer and `sizeof(INPUT)` are verified against Windows x64 ABI standards to prevent memory corruption or stack misalignments.

---

## 3. Concurrency & State Machine

### 3.1 Worker Thread Lifecycle
The application strictly enforces thread boundaries:
- **UI Main Thread:** Dedicated exclusively to the Tkinter rendering loop and UI dispatch.
- **Worker Daemon Thread:** Spawned on demand by `AutomationService`. It runs autonomously as a daemon thread, ensuring that closing the window instantly terminates background loops without zombie threads.

### 3.2 State Transition Model
```
            +------------------------+
            |        STANDBY         |
            +------------------------+
                        |
            [Hotkey / Start Clicked]
                        |
                        v
            +------------------------+
            |      VALIDATION        |
            +------------------------+
               /                  \
   [Valid Key]                     [Invalid Key]
      /                                   \
     v                                     v
+------------------------+        +------------------------+
|      INITIALIZE        |        |    REVERT TO STANDBY   |
| (Audio High-Pitch Cue) |        |   (Orange Error Badge) |
+------------------------+        +------------------------+
            |
            +--------------------+
            |                    |
            v                    v
+-----------------------+ +-----------------------+
|      REPEAT MODE      | |       HOLD MODE       |
|  - Send ScanCode Down | |  - Send ScanCode Down |
|  - 40ms Pulse Hold    | |  - Retain Held State  |
|  - Send ScanCode Up   | |  - Wait for Stop Cue  |
|  - Sleep(Interval)    | |  - Send ScanCode Up   |
+-----------------------+ +-----------------------+
            \                    /
             \                  /
            [Hotkey / Stop Clicked]
                        │
                        ▼
            +------------------------+
            |       TEARDOWN         |
            | - Explicit Key-Up Call |
            | - Clear Held Memory    |
            | - Audio Low-Pitch Cue  |
            +------------------------+
                        │
                        ▼
            +------------------------+
            |        STANDBY         |
            +------------------------+
```

---

## 4. Windows Security & Privilege Model (UIPI)

Windows implements **User Interface Privilege Isolation (UIPI)** as part of User Account Control (UAC). Under UIPI:
- A lower-integrity process **cannot** send Windows messages or synthetic `SendInput` events to a higher-integrity process.
- Most competitive games and gaming platforms run with Administrator privileges (`High Integrity Level`).

If an automation tool runs at standard user level (`Medium Integrity Level`), Windows silently drops all simulated keystrokes intended for the game window.

**Vortex Mitigation:**  
Vortex embeds an execution manifest specifying `requireAdministrator`:
```xml
<requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
```
This forces Windows to invoke UAC elevation upon launch, guaranteeing that `Vortex.exe` runs at `High Integrity Level` and can deliver input to any application across the entire desktop session.

---

## 5. UI/UX Design System Specification

The user interface follows a strict **60-30-10 Design Ratio** to optimize contrast, minimize ocular fatigue during extended sessions, and ensure visual clarity:

```
[ Canvas: 60% (#0B0D11 Obsidian) ]
   └── [ Cards: 30% (#161920 Slate + 1px #252A36 Stroke) ]
          └── [ Accents: 10% (#D4AF37 Gold Highlights & CTAs) ]
```

### Geometric Capsule Calculus
To prevent canvas clipping artifacts in Tkinter:
$$\text{Corner Radius} = \frac{\text{Widget Height}}{2}$$
For the Status Pill Badge ($H = 28\text{px}$), the radius is mathematically constrained to $R = 14\text{px}$. The internal layout relies on absolute center anchoring (`relx=0.5, rely=0.5`) to eliminate pixel rounding drift across different Windows display scaling factors (100%, 125%, 150% DPI).
