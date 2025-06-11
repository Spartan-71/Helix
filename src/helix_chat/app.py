from textual.app import App
from textual.binding import Binding

from .config import load_config
from .models import SessionManager
from .llm_client import LLMClient
from .ui.screens import ChatScreen


class HelixApp(App):
    """Main Helix application"""
    
    CSS_PATH = "layout.tcss"
    
    BINDINGS = [
        Binding("ctrl+m", "change_model", "Change Model"),
        Binding("ctrl+q", "quit", "Quit"),
        Binding("escape", "focus_input", "Focus Input"),
    ]
    
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.session_manager = SessionManager()
        self.llm_client = LLMClient(self.config)
    
    def on_mount(self) -> None:
        """Initialize the application"""
        chat_screen = ChatScreen(self.session_manager,self.llm_client)
        self.push_screen(chat_screen)
    
    
    def action_focus_input(self) -> None:
        """Focus the chat input"""
        try:
            input_widget = self.query_one("#chat-input")
            input_widget.focus()
        except:
            pass
    

def main():
    """Entry point for the application"""
    app = HelixApp()
    app.run()
