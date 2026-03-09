// background/service_worker.js

/*
This service worker listens for keyboard shortcut commands
defined in manifest.json and forwards them to the active tab.

Commands handled:
Ctrl + Alt + S → mark_start
Ctrl + Alt + E → mark_end
Ctrl + Alt + C → inspect_selection
*/

chrome.commands.onCommand.addListener((command) => {
    console.log("Command received:", command);

    // Get the currently active tab
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (!tabs || tabs.length === 0) {
            console.warn("No active tab found");
            return;
        }

        const activeTabId = tabs[0].id;

        // Send message to content script
        chrome.tabs.sendMessage(activeTabId, {
            action: command
        });
    });
});