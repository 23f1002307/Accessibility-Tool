"""
SelectionManager controls the lifecycle of a virtual selection.

Flow:
    IDLE
      ↓ (mark start)
    START_MARKED
      ↓ (mark end)
    COMPLETE
      ↓ (reset after action)
"""

from enum import Enum
from typing import Optional

from accessibility_inspector.selection.anchor import Anchor
from accessibility_inspector.selection.selection_range import SelectionRange


class SelectionState(str, Enum):
    IDLE = "idle"
    START_MARKED = "start_marked"
    COMPLETE = "complete"


class SelectionManager:
    """
    Handles start/end anchor logic and selection state.
    """

    def __init__(self):
        self._state: SelectionState = SelectionState.IDLE
        self._start_anchor: Optional[Anchor] = None
        self._end_anchor: Optional[Anchor] = None
        self._selection: Optional[SelectionRange] = None

    @property
    def state(self) -> SelectionState:
        return self._state

    @property
    def selection(self) -> Optional[SelectionRange]:
        return self._selection

    def mark_start(self, anchor: Anchor) -> None:
        """
        Marks the start anchor and resets any previous selection.
        """
        self._start_anchor = anchor
        self._end_anchor = None
        self._selection = None
        self._state = SelectionState.START_MARKED

    def mark_end(self, anchor: Anchor) -> SelectionRange:
        """
        Marks the end anchor and finalizes the selection.
        """

        if self._state != SelectionState.START_MARKED:
            raise RuntimeError("Start anchor must be marked before marking end.")

        self._end_anchor = anchor

        self._selection = SelectionRange.from_anchors(
            self._start_anchor,
            self._end_anchor
        )

        self._state = SelectionState.COMPLETE
        return self._selection

    def reset(self) -> None:
        """
        Clears selection and returns to IDLE state.
        """
        self._start_anchor = None
        self._end_anchor = None
        self._selection = None
        self._state = SelectionState.IDLE

    def has_active_selection(self) -> bool:
        """
        Returns True if a complete selection exists.
        """
        return (
            self._state == SelectionState.COMPLETE
            and self._selection is not None
        )