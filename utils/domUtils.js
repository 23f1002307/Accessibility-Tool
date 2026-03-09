// content/domUtils.js

/*
DOM Utilities

Helper functions for:
- extracting element HTML
- detecting interactive elements
- collecting element metadata
*/

class DomUtils {

    // -----------------------------
    // Get HTML of element
    // -----------------------------
    static getOuterHTML(element) {
        if (!element) return null;
        return element.outerHTML;
    }

    // -----------------------------
    // Get tag name
    // -----------------------------
    static getTagName(element) {
        if (!element) return null;
        return element.tagName.toLowerCase();
    }

    // -----------------------------
    // Get element attributes
    // -----------------------------
    static getAttributes(element) {

        if (!element) return {};

        const attrs = {};

        for (let attr of element.attributes) {
            attrs[attr.name] = attr.value;
        }

        return attrs;
    }

    // -----------------------------
    // Check if element is interactive
    // -----------------------------
    static isInteractive(element) {

        if (!element) return false;

        const interactiveTags = [
            "button",
            "a",
            "input",
            "select",
            "textarea",
            "label"
        ];

        if (interactiveTags.includes(element.tagName.toLowerCase())) {
            return true;
        }

        if (element.hasAttribute("onclick")) {
            return true;
        }

        if (element.getAttribute("role") === "button") {
            return true;
        }

        return false;
    }

    // -----------------------------
    // Get element text
    // -----------------------------
    static getTextContent(element) {

        if (!element) return "";

        return element.innerText.trim();
    }

    // -----------------------------
    // Extract useful element data
    // -----------------------------
    static extractElementInfo(element) {

        if (!element) return null;

        return {
            tag: DomUtils.getTagName(element),
            text: DomUtils.getTextContent(element),
            html: DomUtils.getOuterHTML(element),
            attributes: DomUtils.getAttributes(element),
            interactive: DomUtils.isInteractive(element)
        };
    }

}