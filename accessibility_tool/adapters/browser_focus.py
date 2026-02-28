"""
Browser Focus Adapter

Responsible for:
- Capturing the currently focused DOM element
- Extracting its metadata
- Converting it into an Anchor model

NOTE:
This module assumes that a JavaScript bridge is available
to fetch DOM information from the browser.

The actual JS execution mechanism (extension or DevTools)
will be integrated later.
"""

from typing import Dict, Any, Optional

from accessibility_inspector.selection.anchor import Anchor, AnchorSource
from accessibility_inspector.engine.models import Platform, ElementType


class BrowserFocusAdapter:
    """
    Adapter that converts browser focus information
    into an Anchor object.
    """

    def __init__(self, js_bridge):
        """
        js_bridge: an object capable of executing JavaScript
        in the active browser tab and returning JSON results.
        """
        self.js_bridge = js_bridge

    # -------------------------------------------------
    # PUBLIC METHOD
    # -------------------------------------------------

    def capture_focus_anchor(self) -> Optional[Anchor]:
        """
        Captures the currently focused DOM element
        and converts it into an Anchor.
        """

        element_data = self._get_focused_element_data()

        if not element_data:
            return None

        return self._build_anchor_from_dom(element_data)

    # -------------------------------------------------
    # INTERNAL LOGIC
    # -------------------------------------------------

    def _get_focused_element_data(self) -> Optional[Dict[str, Any]]:
        """
        Executes JavaScript to fetch activeElement metadata.
        """

        script = """
        (function() {
            const el = document.activeElement;
            if (!el) return null;

            const rect = el.getBoundingClientRect();

            function getXPath(element) {
                if (element.id !== '')
                    return '//*[@id="' + element.id + '"]';
                if (element === document.body)
                    return '/html/body';

                let ix = 0;
                const siblings = element.parentNode.childNodes;
                for (let i = 0; i < siblings.length; i++) {
                    const sibling = siblings[i];
                    if (sibling === element)
                        return getXPath(element.parentNode) +
                            '/' + element.tagName.toLowerCase() +
                            '[' + (ix + 1) + ']';
                    if (sibling.nodeType === 1 &&
                        sibling.tagName === element.tagName) {
                        ix++;
                    }
                }
            }

            return {
                tag: el.tagName.toLowerCase(),
                role: el.getAttribute('role'),
                id: el.id,
                className: el.className,
                xpath: getXPath(el),
                rect: {
                    x: rect.left,
                    y: rect.top,
                    width: rect.width,
                    height: rect.height
                },
                isFocusable: el.tabIndex >= 0
            };
        })();
        """

        return self.js_bridge.execute(script)

    # -------------------------------------------------
    # BUILD ANCHOR
    # -------------------------------------------------

    def _build_anchor_from_dom(self, data: Dict[str, Any]) -> Anchor:
        """
        Converts raw DOM metadata into Anchor model.
        """

        element_type = (
            ElementType.INTERACTIVE
            if data.get("isFocusable")
            else ElementType.NON_INTERACTIVE
        )

        return Anchor(
            platform=Platform.BROWSER,
            source=AnchorSource.FOCUS,
            element_type=element_type,
            xpath=data.get("xpath"),
            dom_node_id=data.get("id"),
            bounding_rect={
                "x": int(data["rect"]["x"]),
                "y": int(data["rect"]["y"]),
                "width": int(data["rect"]["width"]),
                "height": int(data["rect"]["height"]),
            },
            description=f"Focused element: <{data.get('tag')}>"
        )