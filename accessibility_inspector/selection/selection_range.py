"""
SelectionRange combines START and END anchors into a single
virtual selection.

It is responsible for:
- Validating anchors
- Ordering anchors correctly
- Computing the final bounding rectangle
- Providing selection metadata for screenshot or inspection
"""

from typing import Dict
from pydantic import BaseModel, Field, model_validator

from accessibility_inspector.selection.anchor import Anchor
from accessibility_inspector.engine.models import Platform


class SelectionRange(BaseModel):
    """
    Represents a virtual selection between two anchors.
    """

    start_anchor: Anchor = Field(
        ..., description="Selection start anchor"
    )

    end_anchor: Anchor = Field(
        ..., description="Selection end anchor"
    )

    platform: Platform = Field(
        ..., description="Platform on which selection was made"
    )

    bounding_rect: Dict[str, int] = Field(
        ..., description="Union bounding rectangle of the selection"
    )

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------

    @model_validator(mode="after")
    def validate_selection(self):
        """
        Ensures selection is valid and consistent.
        """

        if self.start_anchor.platform != self.end_anchor.platform:
            raise ValueError("Start and end anchors must be on the same platform")

        if self.start_anchor.platform != self.platform:
            raise ValueError("Selection platform mismatch")

        return self

    # -------------------------------------------------
    # FACTORY METHOD
    # -------------------------------------------------

    @classmethod
    def from_anchors(cls, start: Anchor, end: Anchor) -> "SelectionRange":
        """
        Create a SelectionRange from two anchors.

        Computes the union bounding rectangle automatically.
        """

        rect = cls._compute_union_rect(
            start.bounding_rect,
            end.bounding_rect
        )

        return cls(
            start_anchor=start,
            end_anchor=end,
            platform=start.platform,
            bounding_rect=rect
        )

    # -------------------------------------------------
    # GEOMETRY
    # -------------------------------------------------

    @staticmethod
    def _compute_union_rect(
        rect1: Dict[str, int],
        rect2: Dict[str, int]
    ) -> Dict[str, int]:
        """
        Computes the smallest rectangle that contains both rect1 and rect2.
        """

        x1 = min(rect1["x"], rect2["x"])
        y1 = min(rect1["y"], rect2["y"])

        x2 = max(
            rect1["x"] + rect1["width"],
            rect2["x"] + rect2["width"]
        )

        y2 = max(
            rect1["y"] + rect1["height"],
            rect2["y"] + rect2["height"]
        )

        return {
            "x": x1,
            "y": y1,
            "width": x2 - x1,
            "height": y2 - y1
        }

    # -------------------------------------------------
    # HELPERS
    # -------------------------------------------------

    def is_text_based(self) -> bool:
        """
        Returns True if either anchor is text-based
        (virtual cursor selection).
        """
        return (
            self.start_anchor.is_text_anchor()
            or self.end_anchor.is_text_anchor()
        )

    def summary(self) -> Dict[str, str]:
        """
        Returns a short summary useful for logs and UI.
        """
        return {
            "platform": self.platform.value,
            "start_source": self.start_anchor.source.value,
            "end_source": self.end_anchor.source.value,
        }