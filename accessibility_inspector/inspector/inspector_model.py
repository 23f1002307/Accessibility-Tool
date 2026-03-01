"""
Inspector Model

Responsible for:
- Preparing structured inspection data
- Converting SelectionRange into UI-friendly format
- Organizing HTML, CSS, XPath and accessibility hints

This module does NOT:
- Perform DOM execution
- Render UI
"""

from typing import Dict, Any, List

from accessibility_inspector.selection.selection_range import SelectionRange


class InspectorModel:
    """
    Converts a SelectionRange into structured inspection data.
    """

    def build_inspection_data(self, selection: SelectionRange) -> Dict[str, Any]:
        """
        Creates a structured dictionary that can be rendered
        in the inspector popup UI.
        """

        return {
            "platform": selection.platform.value,
            "start_anchor": self._anchor_data(selection.start_anchor),
            "end_anchor": self._anchor_data(selection.end_anchor),
            "bounding_rect": selection.bounding_rect,
            "summary": selection.summary(),
        }

    # -------------------------------------------------
    # INTERNAL
    # -------------------------------------------------

    def _anchor_data(self, anchor) -> Dict[str, Any]:
        """
        Extract structured data from an Anchor.
        """

        return {
            "source": anchor.source.value,
            "element_type": anchor.element_type.value,
            "xpath": anchor.xpath,
            "automation_id": anchor.automation_id,
            "bounding_rect": anchor.bounding_rect,
            "text_offsets": {
                "start": anchor.text_offset_start,
                "end": anchor.text_offset_end,
            },
            "description": anchor.description,
        }