// inspector/inspector.js

/*
Inspector script

Populates the inspector page with the selected element data
received from the extension.
*/

document.addEventListener("DOMContentLoaded", () => {

    chrome.storage.local.get("inspectionData", (data) => {

        if (!data || !data.inspectionData) {
            console.warn("No inspection data available.");
            return;
        }

        const info = data.inspectionData;

        document.getElementById("xpath").textContent = info.xpath || "";
        document.getElementById("tag").textContent = info.tag || "";
        document.getElementById("text").textContent = info.text || "";

        document.getElementById("attributes").textContent =
            JSON.stringify(info.attributes, null, 2);

        document.getElementById("html").textContent = info.html || "";

        document.getElementById("a11y").textContent =
            info.interactive
                ? "Interactive element detected. Verify keyboard accessibility and ARIA roles."
                : "Non‑interactive element. Ensure semantic HTML is used.";
    });

});