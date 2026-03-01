"""
Browser Virtual Cursor Adapter

Responsible for:
- Capturing the current virtual cursor / text selection
- Supporting non-interactive content (headings, paragraphs, etc.)
- Converting selection into an Anchor

This works with screen readers in browse mode,
since they update DOM selection/caret position.
"""

from typing import Dict, Any, Optional

from accessibility_inspector.selection.anchor import Anchor, AnchorSource
from accessibility_inspector.engine.models import Platform, ElementType


class BrowserVirtualCursorAdapter:
    """
    Converts browser text selection into an Anchor.
    """

    def __init__(self, js_bridge):
        """
        js_bridge: Executes JavaScript inside active browser tab.
        """
        self.js_bridge = js_bridge

    # -------------------------------------------------
    # PUBLIC METHOD
    # -------------------------------------------------

    def capture_virtual_cursor_anchor(self) -> Optional[Anchor]:
        """
        Captures the current DOM selection (browse mode position)
        and converts it into an Anchor.
        """

        selection_data = self._get_selection_data()

        if not selection_data:
            return None

        return self._build_anchor_from_selection(selection_data)

    # -------------------------------------------------
    # INTERNAL: GET DOM SELECTION
    # -------------------------------------------------

    def _get_selection_data(self) -> Optional[Dict[str, Any]]:
        """
        Uses JavaScript to capture current selection / caret.
        """

        script = """
        (function() {
            const selection = window.getSelection();
            if (!selection || selection.rangeCount === 0) {
                return null;
            }

            const range = selection.getRangeAt(0);
            const rect = range.getBoundingClientRect();

            function getXPath(element) {
                if (!element) return null;
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

            const container = range.startContainer.nodeType === 3
                ? range.startContainer.parentElement
                : range.startContainer;

            return {
                xpath: getXPath(container),
                textStart: range.startOffset,
                textEnd: range.endOffset,
                rect: {
                    x: rect.left,
                    y: rect.top,
                    width: rect.width,
                    height: rect.height
                },
                tag: container.tagName ? container.tagName.toLowerCase() : "text"
            };
        })();
        """

        return self.js_bridge.execute(script)

    # -------------------------------------------------
    # BUILD ANCHOR
    # -------------------------------------------------

    def _build_anchor_from_selection(self, data: Dict[str, Any]) -> Anchor:
        """
        Converts selection metadata into Anchor model.
        """

        return Anchor(
            platform=Platform.BROWSER,
            source=AnchorSource.VIRTUAL_CURSOR,
            element_type=ElementType.NON_INTERACTIVE,
            xpath=data.get("xpath"),
            bounding_rect={
                "x": int(data["rect"]["x"]),
                "y": int(data["rect"]["y"]),
                "width": int(data["rect"]["width"]),
                "height": int(data["rect"]["height"]),
            },
            text_offset_start=data.get("textStart"),
            text_offset_end=data.get("textEnd"),
            description=f"Virtual cursor at <{data.get('tag')}>"
        )