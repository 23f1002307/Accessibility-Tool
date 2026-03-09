// content/overlay.js

/*
Overlay

Responsible for visually highlighting the selected region
on the webpage.
*/

class Overlay {

    static overlayElement = null;

    // -----------------------------
    // Draw Selection Box
    // -----------------------------
    static drawSelection(selection) {

        // Remove old overlay if it exists
        Overlay.remove();

        const rect = selection.rect;

        const overlay = document.createElement("div");
        overlay.id = "accessibility-inspector-overlay";

        overlay.style.position = "absolute";
        overlay.style.left = rect.x + "px";
        overlay.style.top = rect.y + "px";
        overlay.style.width = rect.width + "px";
        overlay.style.height = rect.height + "px";

        overlay.style.border = "3px solid red";
        overlay.style.backgroundColor = "rgba(255,0,0,0.1)";
        overlay.style.zIndex = "999999";

        document.body.appendChild(overlay);

        Overlay.overlayElement = overlay;

        console.log("Overlay drawn:", rect);
    }

    // -----------------------------
    // Remove Overlay
    // -----------------------------
    static remove() {

        if (Overlay.overlayElement) {
            Overlay.overlayElement.remove();
            Overlay.overlayElement = null;
        }
    }

}