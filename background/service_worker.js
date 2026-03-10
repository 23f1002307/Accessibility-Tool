// background/service_worker.js

chrome.commands.onCommand.addListener((command) => {

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {

        if (!tabs || tabs.length === 0) return;

        const activeTabId = tabs[0].id;

        chrome.tabs.sendMessage(activeTabId, {
            action: command
        });

    });

});


chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

    if (!message || !message.action) return;


    // OPEN INSPECTOR PAGE
    if (message.action === "open_inspector_page") {

        chrome.tabs.create({
            url: chrome.runtime.getURL("inspector/inspector.html")
        });

    }


    // SCREENSHOT WITH CROPPING
    if (message.action === "capture_screenshot") {

        chrome.tabs.captureVisibleTab(null, { format: "png" }, async (dataUrl) => {

            const rect = message.rect;

            // convert base64 image to blob
            const response = await fetch(dataUrl);
            const blob = await response.blob();

            // create bitmap from blob
            const bitmap = await createImageBitmap(blob);

            const canvas = new OffscreenCanvas(rect.width, rect.height);
            const ctx = canvas.getContext("2d");

            ctx.drawImage(
                bitmap,
                rect.x,
                rect.y,
                rect.width,
                rect.height,
                0,
                0,
                rect.width,
                rect.height
            );

            const croppedBlob = await canvas.convertToBlob();

            const reader = new FileReader();

            reader.onloadend = () => {

                chrome.downloads.download({
                    url: reader.result,
                    filename: "accessibility_selection.png"
                });

            };

            reader.readAsDataURL(croppedBlob);

        });

    }

});