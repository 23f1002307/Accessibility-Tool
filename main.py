"""
Accessibility Inspector - Entry Point

Bootstraps:
- JS bridge (stub for now)
- Screenshot service
- Overlay service
- Inspector UI
- Orchestrator
- Hotkeys

Run this file to start the application.
"""

import time
from accessibility_inspector.core.orchestrator import Orchestrator
from accessibility_inspector.capture.screenshot import ScreenshotService
from accessibility_inspector.capture.overlay import OverlayService
from accessibility_inspector.inspector.inspector_model import InspectorModel
from accessibility_inspector.inspector.popup_ui import PopupUI


# -------------------------------------------------
# JS BRIDGE (Stub Implementation)
# -------------------------------------------------

class JSBridgeStub:
    """
    Temporary stub for executing JavaScript.

    Later this will be replaced with:
    - Browser extension messaging
    - Chrome DevTools Protocol
    - Remote debugging connection
    """

    def execute(self, script: str):
        print("JS execution requested. Replace JSBridgeStub with real implementation.")
        return None


# -------------------------------------------------
# INSPECTOR SERVICE WRAPPER
# -------------------------------------------------

class InspectorService:
    """
    Wraps InspectorModel + PopupUI
    """

    def __init__(self):
        self.model = InspectorModel()
        self.ui = PopupUI()

    def inspect(self, selection):
        inspection_data = self.model.build_inspection_data(selection)
        self.ui.inspect(inspection_data)


# -------------------------------------------------
# APPLICATION BOOTSTRAP
# -------------------------------------------------

def main():
    print("Starting Accessibility Inspector...")

    # Initialize core services
    js_bridge = JSBridgeStub()
    screenshot_service = ScreenshotService()
    overlay_service = OverlayService()
    inspector_service = InspectorService()

    # Initialize orchestrator
    orchestrator = Orchestrator(
        js_bridge=js_bridge,
        screenshot_service=screenshot_service,
        inspector_service=inspector_service,
    )

    # Start system
    orchestrator.start()

    print("Accessibility Inspector is running.")
    print("Use Ctrl+Alt+S (start), Ctrl+Alt+E (end), Ctrl+Alt+P (screenshot), Ctrl+Alt+C (inspect)")

    # Keep application alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")


if __name__ == "__main__":
    main()