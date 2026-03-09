// content/anchor.js

/*
Anchor

Represents a DOM element used as a start or end point
for the accessibility selection.
*/

class Anchor {

    constructor(element, rect, xpath) {
        this.element = element;
        this.rect = rect;
        this.xpath = xpath;
    }

    // -----------------------------
    // Create anchor from current DOM position
    // -----------------------------
    static createFromCurrentPosition() {

        let element = document.activeElement;

        // If no focused element, fall back to element under cursor
        if (!element || element === document.body) {
            element = document.elementFromPoint(
                window.innerWidth / 2,
                window.innerHeight / 2
            );
        }

        if (!element) {
            console.warn("No element detected for anchor.");
            return null;
        }

        const rect = element.getBoundingClientRect();

        const xpath = Anchor.getXPath(element);

        return new Anchor(
            element,
            {
                x: rect.left + window.scrollX,
                y: rect.top + window.scrollY,
                width: rect.width,
                height: rect.height
            },
            xpath
        );
    }

    // -----------------------------
    // Generate XPath
    // -----------------------------
    static getXPath(element) {

        if (element.id !== "") {
            return `//*[@id="${element.id}"]`;
        }

        if (element === document.body) {
            return "/html/body";
        }

        let ix = 0;
        const siblings = element.parentNode.childNodes;

        for (let i = 0; i < siblings.length; i++) {

            const sibling = siblings[i];

            if (sibling === element) {
                return (
                    Anchor.getXPath(element.parentNode) +
                    "/" +
                    element.tagName.toLowerCase() +
                    "[" +
                    (ix + 1) +
                    "]"
                );
            }

            if (
                sibling.nodeType === 1 &&
                sibling.tagName === element.tagName
            ) {
                ix++;
            }
        }
    }

}