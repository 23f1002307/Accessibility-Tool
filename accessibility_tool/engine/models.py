"""
Core data models for the Accessibility Inspector.

These models represent:
- UI / DOM elements
- Accessibility issues detected on them
- Anchors and selection metadata references
- Scan results

All models are intentionally explicit and strongly typed
to avoid ambiguity and make debugging easier.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime

from pydantic import BaseModel, Field


# -------------------------------------------------
# ENUMS
# -------------------------------------------------

class Platform(str, Enum):
    WINDOWS = "windows"
    BROWSER = "browser"


class ElementType(str, Enum):
    INTERACTIVE = "interactive"
    NON_INTERACTIVE = "non_interactive"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# -------------------------------------------------
# ACCESSIBILITY ISSUE MODEL
# -------------------------------------------------

class AccessibilityIssue(BaseModel):
    """
    Represents a single accessibility issue detected
    on a UI or DOM element.
    """

    rule_id: str = Field(
        ..., description="Unique identifier for the accessibility rule"
    )
    description: str = Field(
        ..., description="Human-readable explanation of the issue"
    )
    severity: Severity = Field(
        ..., description="Severity level of the issue"
    )
    recommendation: Optional[str] = Field(
        None, description="Suggested fix for the issue"
    )


# -------------------------------------------------
# UI / DOM ELEMENT MODEL
# -------------------------------------------------

class UIElement(BaseModel):
    """
    Represents a single UI element (Windows UIA or Browser DOM).
    """

    element_id: str = Field(
        ..., description="Stable internal identifier for the element"
    )

    platform: Platform = Field(
        ..., description="Origin platform of the element"
    )

    element_type: ElementType = Field(
        ..., description="Interactive or non-interactive"
    )

    # Accessibility / semantic properties
    role: Optional[str] = Field(
        None, description="ARIA role or UI Automation control type"
    )

    name: Optional[str] = Field(
        None, description="Accessible name announced by screen readers"
    )

    is_focusable: bool = Field(
        False, description="Whether the element can receive keyboard focus"
    )

    is_enabled: bool = Field(
        True, description="Whether the element is enabled"
    )

    # Geometry (screen coordinates)
    bounding_rect: Optional[Dict[str, int]] = Field(
        None,
        description="Bounding rectangle: {x, y, width, height}"
    )

    # DOM-specific fields (browser only)
    html: Optional[str] = None
    css_selector: Optional[str] = None
    xpath: Optional[str] = None

    # UIA-specific fields (Windows only)
    automation_id: Optional[str] = None
    class_name: Optional[str] = None

    # Detected accessibility issues
    issues: List[AccessibilityIssue] = Field(default_factory=list)


# -------------------------------------------------
# SCAN RESULT MODEL
# -------------------------------------------------

class ScanResult(BaseModel):
    """
    Represents a single scan execution.
    """

    scan_id: str = Field(
        ..., description="Unique scan identifier"
    )

    platform: Platform = Field(
        ..., description="Platform scanned"
    )

    started_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    completed_at: Optional[datetime] = None

    elements: List[UIElement] = Field(
        default_factory=list
    )

    summary: Optional[Dict[str, Any]] = Field(
        None, description="Aggregated statistics for the scan"
    )
