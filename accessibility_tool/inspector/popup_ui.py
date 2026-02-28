"""
Inspector Popup UI

Responsible for:
- Rendering inspection data in a browser
- Running a lightweight local Flask server
- Displaying structured selection information

This is a minimal UI layer.
"""

import threading
import webbrowser
from typing import Dict, Any

from flask import Flask, render_template_string


class PopupUI:
    """
    Lightweight popup UI using Flask.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 5005):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self._inspection_data: Dict[str, Any] = {}

        self._configure_routes()

    # -------------------------------------------------
    # ROUTES
    # -------------------------------------------------

    def _configure_routes(self):
        @self.app.route("/")
        def index():
            return render_template_string(self._html_template(), data=self._inspection_data)

    # -------------------------------------------------
    # PUBLIC METHOD
    # -------------------------------------------------

    def inspect(self, inspection_data: Dict[str, Any]):
        """
        Launches popup UI with inspection data.
        """

        self._inspection_data = inspection_data

        # Run server in background thread
        threading.Thread(
            target=self._run_server,
            daemon=True
        ).start()

        webbrowser.open(f"http://{self.host}:{self.port}")

    # -------------------------------------------------
    # INTERNAL
    # -------------------------------------------------

    def _run_server(self):
        self.app.run(host=self.host, port=self.port, debug=False)

    def _html_template(self) -> str:
        """
        Minimal inspection UI template.
        """

        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Accessibility Inspector</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f4f4f4;
                }
                h1 {
                    color: #333;
                }
                .section {
                    background: white;
                    padding: 15px;
                    margin-bottom: 15px;
                    border-radius: 6px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }
                pre {
                    background: #eee;
                    padding: 10px;
                    overflow-x: auto;
                }
            </style>
        </head>
        <body>
            <h1>Accessibility Inspector</h1>

            <div class="section">
                <h2>Platform</h2>
                <p>{{ data.platform }}</p>
            </div>

            <div class="section">
                <h2>Start Anchor</h2>
                <pre>{{ data.start_anchor }}</pre>
            </div>

            <div class="section">
                <h2>End Anchor</h2>
                <pre>{{ data.end_anchor }}</pre>
            </div>

            <div class="section">
                <h2>Selection Bounding Rectangle</h2>
                <pre>{{ data.bounding_rect }}</pre>
            </div>

            <div class="section">
                <h2>Summary</h2>
                <pre>{{ data.summary }}</pre>
            </div>

        </body>
        </html>
        """