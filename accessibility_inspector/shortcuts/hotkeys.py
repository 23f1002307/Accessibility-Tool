"""
Global Hotkey Manager

Responsible for:
- Registering keyboard shortcuts
- Connecting them to selection actions
- Triggering screenshot and inspection workflows

This module does NOT:
- Capture anchors directly
- Perform screenshot logic
- Perform inspection logic

It delegates those responsibilities.
"""

from pynput import keyboard
from typing import Callable


class HotkeyManager:
    """
    Registers and manages global keyboard shortcuts.
    """

    def __init__(
        self,
        on_mark_start: Callable[[], None],
        on_mark_end: Callable[[], None],
        on_screenshot: Callable[[], None],
        on_inspect: Callable[[], None],
    ):
        """
        Callbacks are injected from orchestrator.
        """

        self.on_mark_start = on_mark_start
        self.on_mark_end = on_mark_end
        self.on_screenshot = on_screenshot
        self.on_inspect = on_inspect

        self._listener = None

        # Define key combinations here
        self.shortcuts = {
            "<ctrl>+<alt>+s": self.on_mark_start,
            "<ctrl>+<alt>+e": self.on_mark_end,
            "<ctrl>+<alt>+p": self.on_screenshot,
            "<ctrl>+<alt>+c": self.on_inspect,
        }

    # -------------------------------------------------
    # START LISTENER
    # -------------------------------------------------

    def start(self):
        """
        Starts listening for global hotkeys.
        """

        self._listener = keyboard.GlobalHotKeys(self.shortcuts)
        self._listener.start()

    # -------------------------------------------------
    # STOP LISTENER
    # -------------------------------------------------

    def stop(self):
        """
        Stops the hotkey listener.
        """

        if self._listener:
            self._listener.stop()
            self._listener = None