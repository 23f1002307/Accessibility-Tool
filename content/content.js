// content/content.js

console.log("Accessibility Inspector content script loaded.");

const selectionManager = new SelectionManager();

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
// START ANCHOR
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


// -----------------------------
// END ANCHOR
// -----------------------------
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


// -----------------------------
// INSPECT SELECTION
// -----------------------------
function handleInspect() {

    const selection = selectionManager.getSelection();

    if (!selection) {
        console.warn("No selection available.");
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

    // Save data for inspector page
    chrome.storage.local.set({
        inspectionData: inspectionData
    }, () => {

        console.log("Inspection data saved.");

        // Open inspector page
        chrome.runtime.sendMessage({
            action: "open_inspector_page"
        });

    });
}