from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Static, Markdown,Footer

from .components import ChatInput
from ..models import SessionManager
from ..llm_client import LLMClient

class ChatScreen(Screen):
    """Main chat screen"""
    
    def __init__(self, session_manager:SessionManager,llm_client: LLMClient):
        super().__init__()
        self.session_manager = session_manager
        self.llm_client = llm_client
    
    def compose(self) -> ComposeResult:
        """Compose the chat screen"""
        yield Static("Helix - Terminal native LLM Interface", id="header")
        
        # with Horizontal():
            # Session sidebar
            # self.sidebar = SessionSidebar(
            #     self.session_manager,
            #     id="sidebar"
            # )
            # yield self.sidebar
            
            # Main chat area
        with Vertical(id="chat-area"):
            yield VerticalScroll(
                Markdown(
                    id="chat-display",
                ),
                id="chat-container"
            )
            yield ChatInput(id="chat-input")
        yield Footer()
    
    def on_mount(self) -> None:
        """Focus input on mount"""
        self.query_one("#chat-input").focus()
    
    def on_input_submitted(self, event) -> None:
        """Handle chat input submission"""
        if not event.value.strip():
            return
        
        # Add user message
        session = self.session_manager.get_active_session()
        session.add_message("user", event.value)
        
        # Update display
        self.update_chat_display()
        
        # Clear input
        event.input.value = ""
        
        # Get LLM response
        self.run_worker(self._get_llm_response(), exclusive=True)
    
    async def _get_llm_response(self) -> None:
        """Get LLM response and update display"""
        session = self.session_manager.get_active_session()
        messages = session.get_api_messages()
        
        response = await self.llm_client.get_response(messages, session.model)
        session.add_message("assistant", response)
        
        self.update_chat_display()


    def update_chat_display(self) -> None:
        """Update chat display with current session"""
        session = self.session_manager.get_active_session()
        chat_display = self.query_one("#chat-display", Markdown)
        chat_display.update(session.get_markdown_history())
        
        # Auto-scroll to bottom
        container = self.query_one("#chat-container", VerticalScroll)
        self.call_after_refresh(container.scroll_end)
    
    
