from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal,Vertical,VerticalScroll
from textual.widgets import Static,Header


class helix(App):
    CSS_PATH = "layout.tcss"

    def compose(self) -> ComposeResult:
        yield Static("Helix",id="header")
        with VerticalScroll(id="sidebar"):
            for id in range(15):
                yield Static(f"session {id}",classes="box")
        with Vertical():
            with VerticalScroll():
                yield Static("Output Box",id="output_box")
            yield Static("Input Box",id="input_box")



if __name__ == "__main__":
    app = helix()
    app.run()