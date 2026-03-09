// content/selectionManager.js

/*
SelectionManager

Handles:
- Start anchor
- End anchor
- Selection state
- Returning current selection
*/

class SelectionManager {

    constructor() {
        this.startAnchor = null;
        this.endAnchor = null;
    }

    // -----------------------------
    // Set Start Anchor
    // -----------------------------
    setStart(anchor) {

        this.startAnchor = anchor;
        this.endAnchor = null;

        console.log("Selection start set:", anchor);
    }

    // -----------------------------
    // Set End Anchor
    // -----------------------------
    setEnd(anchor) {

        if (!this.startAnchor) {
            console.warn("Start anchor not set yet.");
            return;
        }

        this.endAnchor = anchor;

        console.log("Selection end set:", anchor);
    }

    // -----------------------------
    // Get Selection
    // -----------------------------
    getSelection() {

        if (!this.startAnchor || !this.endAnchor) {
            return null;
        }

        const startRect = this.startAnchor.rect;
        const endRect = this.endAnchor.rect;

        const x = Math.min(startRect.x, endRect.x);
        const y = Math.min(startRect.y, endRect.y);

        const width =
            Math.max(startRect.x + startRect.width, endRect.x + endRect.width) - x;

        const height =
            Math.max(startRect.y + startRect.height, endRect.y + endRect.height) - y;

        return {
            start: this.startAnchor,
            end: this.endAnchor,
            rect: {
                x,
                y,
                width,
                height
            }
        };
    }

    // -----------------------------
    // Reset Selection
    // -----------------------------
    reset() {
        this.startAnchor = null;
        this.endAnchor = null;
    }

}