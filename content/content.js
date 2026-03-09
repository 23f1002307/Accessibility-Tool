// content/content.js

/*
Main entry point for the content script.

Responsibilities:
- Receive commands from the background service worker
- Trigger selection actions
- Communicate with SelectionManager
*/

console.log("Accessibility Inspector content script loaded.");

// Initialize selection manager
const selectionManager = new SelectionManager();

// Listen for messages from service worker
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

        default:
            console.warn("Unknown action:", message.action);
    }
});


// -----------------------------
// Handlers
// -----------------------------

function handleMarkStart() {

    const anchor = Anchor.createFromCurrentPosition();

    if (!anchor) {
        console.warn("Could not detect anchor.");
        return;
    }

    selectionManager.setStart(anchor);

    console.log("Start anchor marked:", anchor);
}


function handleMarkEnd() {

    const anchor = Anchor.createFromCurrentPosition();

    if (!anchor) {
        console.warn("Could not detect anchor.");
        return;
    }

    selectionManager.setEnd(anchor);

    console.log("End anchor marked:", anchor);

    const selection = selectionManager.getSelection();

    if (selection) {
        Overlay.drawSelection(selection);
    }
}


function handleInspect() {

    const selection = selectionManager.getSelection();

    if (!selection) {
        console.warn("No selection available.");
        return;
    }

    console.log("Inspecting selection:", selection);

    // Open inspector page
    chrome.runtime.sendMessage({
        action: "open_inspector",
        selection: selection
    });
}