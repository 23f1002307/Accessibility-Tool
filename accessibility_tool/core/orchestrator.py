"""
Application Orchestrator

This module wires together:
- Hotkeys
- SelectionManager
- Browser adapters
- Screenshot logic
- Inspection logic

It acts as the central coordinator of the system.
"""

from typing import Optional

from accessibility_inspector.selection.selection_manager import SelectionManager
from accessibility_inspector.adapters.browser_focus import BrowserFocusAdapter
from accessibility_inspector.adapters.browser_virtual_cursor import (
    BrowserVirtualCursorAdapter,
)
from accessibility_inspector.shortcuts.hotkeys import HotkeyManager


class Orchestrator:
    """
    Central coordinator for the Accessibility Inspector.
    """

    def __init__(self, js_bridge, screenshot_service, inspector_service):
        """
        js_bridge: Executes JavaScript inside active browser tab
        screenshot_service: Handles screenshot capturing
        inspector_service: Handles code inspection UI
        """

        self.selection_manager = SelectionManager()

        self.focus_adapter = BrowserFocusAdapter(js_bridge)
        self.virtual_cursor_adapter = BrowserVirtualCursorAdapter(js_bridge)

        self.screenshot_service = screenshot_service
        self.inspector_service = inspector_service

        self.hotkeys = HotkeyManager(
            on_mark_start=self.mark_start,
            on_mark_end=self.mark_end,
            on_screenshot=self.take_screenshot,
            on_inspect=self.inspect_selection,
        )

    # -------------------------------------------------
    # START SYSTEM
    # -------------------------------------------------

    def start(self):
        """
        Starts hotkey listener.
        """
        self.hotkeys.start()

    # -------------------------------------------------
    # MARK START
    # -------------------------------------------------

    def mark_start(self):
        """
        Captures current anchor (focus or virtual cursor)
        and marks it as selection start.
        """

        anchor = self._capture_current_anchor()

        if anchor:
            self.selection_manager.mark_start(anchor)
            print("Start anchor marked.")

    # -------------------------------------------------
    # MARK END
    # -------------------------------------------------

    def mark_end(self):
        """
        Captures current anchor and finalizes selection.
        """

        anchor = self._capture_current_anchor()

        if anchor:
            selection = self.selection_manager.mark_end(anchor)
            print("Selection completed:", selection.summary())

    # -------------------------------------------------
    # SCREENSHOT
    # -------------------------------------------------

    def take_screenshot(self):
        """
        Takes screenshot of selected area.
        """

        if not self.selection_manager.has_active_selection():
            print("No active selection.")
            return

        selection = self.selection_manager.selection
        self.screenshot_service.capture(selection.bounding_rect)
        print("Screenshot captured.")

        self.selection_manager.reset()

    # -------------------------------------------------
    # INSPECT
    # -------------------------------------------------

    def inspect_selection(self):
        """
        Opens inspector popup for selected range.
        """

        if not self.selection_manager.has_active_selection():
            print("No active selection.")
            return

        selection = self.selection_manager.selection
        self.inspector_service.inspect(selection)
        print("Inspector opened.")

        self.selection_manager.reset()

    # -------------------------------------------------
    # INTERNAL: ANCHOR CAPTURE
    # -------------------------------------------------

    def _capture_current_anchor(self):
        """
        Attempts to capture focus-based anchor first.
        Falls back to virtual cursor anchor.
        """

        anchor = self.focus_adapter.capture_focus_anchor()

        if anchor:
            return anchor

        return self.virtual_cursor_adapter.capture_virtual_cursor_anchor()