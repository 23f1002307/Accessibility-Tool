"""
Anchor model used to mark START and END points for virtual selection.

An Anchor represents a semantic position in the DOM / accessibility tree.
It can originate from:
- Keyboard focus (interactive elements)
- Screen reader virtual cursor (non-interactive elements)

Anchors are platform-agnostic and later consumed by SelectionRange.
"""

from enum import Enum
from typing import Optional, Dict

from pydantic import BaseModel, Field

from accessibility_inspector.engine.models import Platform, ElementType


# -------------------------------------------------
# ENUMS
# -------------------------------------------------

class AnchorSource(str, Enum):
    """
    Describes how the anchor was created.
    """
    FOCUS = "focus"                  # Interactive element focus
    VIRTUAL_CURSOR = "virtual_cursor"  # Screen reader browse mode
    PROGRAMMATIC = "programmatic"    # Future / internal use


# -------------------------------------------------
# ANCHOR MODEL
# -------------------------------------------------

class Anchor(BaseModel):
    """
    Represents a single anchor point in a page or UI.

    This model is intentionally lightweight and immutable once created.
    """

    platform: Platform = Field(
        ..., description="Platform where the anchor was captured"
    )

    source: AnchorSource = Field(
        ..., description="How the anchor was obtained"
    )

    element_type: ElementType = Field(
        ..., description="Interactive or non-interactive element"
    )

    # --- DOM / UI identification ---
    xpath: Optional[str] = Field(
        None, description="XPath to uniquely identify the element (browser)"
    )

    dom_node_id: Optional[str] = Field(
        None, description="Internal DOM node identifier if available"
    )

    automation_id: Optional[str] = Field(
        None, description="UI Automation ID (Windows apps)"
    )

    # --- Geometry ---
    bounding_rect: Dict[str, int] = Field(
        ..., description="Bounding rectangle: {x, y, width, height}"
    )

    # --- Text-level precision (for non-interactive content) ---
    text_offset_start: Optional[int] = Field(
        None, description="Text offset start (virtual cursor)"
    )

    text_offset_end: Optional[int] = Field(
        None, description="Text offset end (virtual cursor)"
    )

    # --- Metadata ---
    description: Optional[str] = Field(
        None, description="Human-readable description of the anchor"
    )

    def is_text_anchor(self) -> bool:
        """
        Returns True if this anchor represents text-level selection
        (typically from a virtual cursor).
        """
        return self.text_offset_start is not None

    def is_focus_anchor(self) -> bool:
        """
        Returns True if this anchor originated from keyboard focus.
        """
        return self.source == AnchorSource.FOCUS
