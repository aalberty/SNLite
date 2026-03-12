from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Footer, Header, TextArea
from textual.reactive import var


TEXT = """\
console.log('Hello, World!');
"""

class SNLite(App):
    """A Textual app to manage stopwatches."""

    COMMAND_PALETTE_BINDING = "p"
    CSS_PATH = "tui.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("f", "toggle_sample", "Sample toggle keybind for testing")
    ]

    show_plain_area = var(True)

    def watch_show_plain_area(self, show_plain_area: bool) -> None:
        """Called when show_plain_area is modified."""
        self.set_class(show_plain_area, "-show-plain-area")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container():
            yield TextArea(id="plain-area")
            with VerticalScroll(id="code-area"):
                yield TextArea.code_editor(TEXT, language="javascript", id="code")
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
    
    def action_toggle_sample(self) -> None:
        """An action to open/close file explorer pane."""
        self.show_plain_area = not self.show_plain_area
        pass

if __name__ == "__main__":
    SNLite().run()