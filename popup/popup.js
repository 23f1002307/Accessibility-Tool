// popup/popup.js

function sendAction(action) {

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {

        if (!tabs.length) return;

        chrome.tabs.sendMessage(tabs[0].id, {
            action: action
        });

    });
}

document.getElementById("startBtn").addEventListener("click", () => {
    sendAction("mark_start");
});

document.getElementById("endBtn").addEventListener("click", () => {
    sendAction("mark_end");
});

document.getElementById("inspectBtn").addEventListener("click", () => {
    sendAction("inspect_selection");
});