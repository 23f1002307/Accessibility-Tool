// content/content.js

console.log("Accessibility Inspector content script loaded.");

const selectionManager = new SelectionManager();


// ----------------------------------
// SCREEN READER ANNOUNCEMENT
// ----------------------------------

function announce(message) {

    const liveRegion = document.createElement("div");

    liveRegion.setAttribute("aria-live", "assertive");
    liveRegion.setAttribute("role", "alert");

    liveRegion.style.position = "absolute";
    liveRegion.style.left = "-9999px";
    liveRegion.style.height = "1px";
    liveRegion.style.width = "1px";
    liveRegion.style.overflow = "hidden";

    liveRegion.textContent = message;

    document.body.appendChild(liveRegion);

    setTimeout(() => {
        if (liveRegion.parentNode) {
            liveRegion.parentNode.removeChild(liveRegion);
        }
    }, 1000);
}


// ----------------------------------
// LISTEN FOR COMMANDS
// ----------------------------------

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

    if (!message || !message.action) return;

    console.log("Content script received action:", message.action);

    switch (message.action) {

        case "mark_start":
            handleMarkStart();
            break;

        case "mark_end":
            handleMarkEnd();
            break;

        case "inspect_selection":
            handleInspect();
            break;

        case "take_screenshot":
            handleScreenshot();
            break;

        default:
            console.warn("Unknown action:", message.action);
    }

});


// ----------------------------------
// START ANCHOR
// ----------------------------------

function handleMarkStart() {

    const anchor = Anchor.createFromCurrentPosition();

    if (!anchor) {
        console.warn("Could not detect anchor.");
        announce("Could not detect start element");
        return;
    }

    selectionManager.setStart(anchor);

    console.log("Start anchor marked:", anchor);

    announce("Start of selection marked");
}


// ----------------------------------
// END ANCHOR
// ----------------------------------

function handleMarkEnd() {

    const anchor = Anchor.createFromCurrentPosition();

    if (!anchor) {
        console.warn("Could not detect anchor.");
        announce("Could not detect end element");
        return;
    }

    selectionManager.setEnd(anchor);

    console.log("End anchor marked:", anchor);

    const selection = selectionManager.getSelection();

    if (selection) {

        Overlay.drawSelection(selection);

        announce("Selection completed");
    }
}


// ----------------------------------
// INSPECT SELECTION
// ----------------------------------

function handleInspect() {

    const selection = selectionManager.getSelection();

    if (!selection) {
        console.warn("No selection available.");
        announce("No selection available to inspect");
        return;
    }

    const element = selection.start.element;

    const info = DomUtils.extractElementInfo(element);

    const inspectionData = {
        xpath: selection.start.xpath,
        tag: info.tag,
        text: info.text,
        html: info.html,
        attributes: info.attributes,
        interactive: info.interactive
    };

    chrome.storage.local.set({
        inspectionData: inspectionData
    }, () => {

        console.log("Inspection data saved.");

        announce("Opening inspector");

        chrome.runtime.sendMessage({
            action: "open_inspector_page"
        });

    });

}


// ----------------------------------
// SCREENSHOT FEATURE
// ----------------------------------

function handleScreenshot() {

    const selection = selectionManager.getSelection();

    if (!selection) {
        announce("No selection available for screenshot");
        return;
    }

    chrome.runtime.sendMessage({
        action: "capture_screenshot",
        rect: selection.rect
    });

    announce("Capturing screenshot of selected region");
}