"""
Overlay Service

Responsible for:
- Drawing bounding boxes on screenshots
- Highlighting selected regions
- Adding simple labels

Uses Pillow for lightweight image annotation.
"""

from typing import Dict, Optional
from PIL import Image, ImageDraw, ImageFont


class OverlayService:
    """
    Draws overlays on screenshots.
    """

    def __init__(self):
        # Default colors (can be extended later)
        self.selection_color = (255, 0, 0)      # Red
        self.border_width = 3

    # -------------------------------------------------
    # PUBLIC METHOD
    # -------------------------------------------------

    def highlight_selection(
        self,
        image_path: str,
        bounding_rect: Dict[str, int],
        label: Optional[str] = None
    ) -> str:
        """
        Draws a bounding box around the selection.

        image_path: path to saved screenshot
        bounding_rect: {x, y, width, height}
        label: optional label text
        """

        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)

        x = bounding_rect["x"]
        y = bounding_rect["y"]
        w = bounding_rect["width"]
        h = bounding_rect["height"]

        # Draw rectangle
        for i in range(self.border_width):
            draw.rectangle(
                [x - i, y - i, x + w + i, y + h + i],
                outline=self.selection_color
            )

        # Optional label
        if label:
            try:
                font = ImageFont.load_default()
                text_position = (x, y - 15 if y > 20 else y + 5)
                draw.text(text_position, label, fill=self.selection_color, font=font)
            except Exception:
                # Fail gracefully if font loading fails
                pass

        img.save(image_path)

        return image_path