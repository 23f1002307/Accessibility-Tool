// background/service_worker.js

/*
Service Worker

Responsibilities:
1. Listen for keyboard shortcut commands
2. Forward commands to the active tab
3. Open the inspector page when requested
*/


// ----------------------------------
// Handle Keyboard Shortcuts
// ----------------------------------

chrome.commands.onCommand.addListener((command) => {

    console.log("Command received:", command);

    // Find active tab
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {

        if (!tabs || tabs.length === 0) {
            console.warn("No active tab found.");
            return;
        }

        const activeTabId = tabs[0].id;

        // Send command to content script
        chrome.tabs.sendMessage(activeTabId, {
            action: command
        });

    });

});


// ----------------------------------
// Handle Messages from Content Script
// ----------------------------------

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

    if (!message || !message.action) return;

    console.log("Service worker received message:", message.action);

    // Open inspector page
    if (message.action === "open_inspector_page") {

        chrome.tabs.create({
            url: chrome.runtime.getURL("inspector/inspector.html")
        });

    }

});