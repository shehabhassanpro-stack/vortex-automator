"""
Audio feedback service using Windows winsound.
Provides non-blocking audio cues for execution status changes.
"""

import threading
import winsound

class SoundService:
    @staticmethod
    def play_start() -> None:
        """Plays high-pitch cue on execution start (async)."""
        threading.Thread(target=SoundService._beep, args=(1200, 70), daemon=True).start()

    @staticmethod
    def play_stop() -> None:
        """Plays lower-pitch cue on execution stop (async)."""
        threading.Thread(target=SoundService._beep, args=(700, 70), daemon=True).start()

    @staticmethod
    def _beep(freq: int, duration: int) -> None:
        try:
            winsound.Beep(freq, duration)
        except Exception:
            pass
