\# Accessible DevTools Inspector (ADI)



A keyboard-driven, screen-reader-friendly tool that allows accessibility testers to inspect focused elements on a webpage and extract DevTools-equivalent information such as HTML, CSS, and JavaScript metadata.



---



\## Problem Statement



Browser DevTools are heavily visual and mouse-dependent, making them difficult or impossible to use efficiently with screen readers such as NVDA.



As a result, accessibility testers face challenges when:

\- Inspecting HTML structure

\- Understanding applied CSS

\- Identifying JavaScript behavior

\- Explaining accessibility bugs clearly to developers



---



\## Project Goal



To provide a fully keyboard-accessible inspection tool that:

\- Works on the currently focused element

\- Extracts the same information visible in DevTools

\- Presents the data in a screen-reader-friendly format

\- Helps accessibility testers report issues accurately



---



\## Scope Definition



\### What This Tool Provides



\- HTML (current DOM state)

\- ARIA attributes and accessibility properties

\- Applied CSS rules

\- Computed styles

\- JavaScript event listener metadata



\### What This Tool Does NOT Provide



\- Full JavaScript source code

\- Application business logic

\- Framework internals (React, Angular, Vue)

\- Server-side or build-time code



This tool mirrors what DevTools exposes, not the entire application source.



---



\## Target Users



\### Primary Users

\- Accessibility testers

\- NVDA users

\- Blind / low-vision QA engineers



\### Secondary Users

\- Front-end developers

\- Accessibility consultants

\- QA teams



---



\## High-Level Architecture





