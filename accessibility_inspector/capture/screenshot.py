"""
Screenshot Service

Responsible for:
- Capturing screen content
- Cropping to bounding rectangle
- Saving image to disk

Uses:
- mss (fast screen capture)
- Pillow (image processing)
"""

import os
from datetime import datetime
from typing import Dict

import mss
from PIL import Image


class ScreenshotService:
    """
    Handles screenshot capture and saving.
    """

    def __init__(self, output_dir: str = "screenshots"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # -------------------------------------------------
    # PUBLIC METHOD
    # -------------------------------------------------

    def capture(self, bounding_rect: Dict[str, int]) -> str:
        """
        Captures a screenshot of the specified bounding rectangle.

        bounding_rect:
        {
            "x": int,
            "y": int,
            "width": int,
            "height": int
        }
        """

        filename = self._generate_filename()
        filepath = os.path.join(self.output_dir, filename)

        with mss.mss() as sct:
            monitor = {
                "left": bounding_rect["x"],
                "top": bounding_rect["y"],
                "width": bounding_rect["width"],
                "height": bounding_rect["height"],
            }

            screenshot = sct.grab(monitor)

            # Convert raw screenshot to Pillow Image
            img = Image.frombytes(
                "RGB",
                screenshot.size,
                screenshot.rgb
            )

            img.save(filepath)

        return filepath

    # -------------------------------------------------
    # INTERNAL UTIL
    # -------------------------------------------------

    def _generate_filename(self) -> str:
        """
        Generates timestamp-based filename.
        """

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return f"selection_{timestamp}.png"