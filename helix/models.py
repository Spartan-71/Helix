from typing import List, Dict
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Message:
    """Single chat message"""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ChatSession:
    """Chat session with message history"""
    name: str
    messages: List[Message] = field(default_factory=list)
    model: str = "ollama/llama3"
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the session"""
        message = Message(role=role, content=content)
        self.messages.append(message)
    
    def get_api_messages(self) -> List[Dict[str, str]]:
        """Get messages in API format"""
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]
    
    def get_markdown_history(self) -> str:
        """Convert message history to markdown"""
        if not self.messages:
            return f"# {self.name}\n\nStart a conversation by typing below."
        
        content = [f"# {self.name}\n"]
        
        for msg in self.messages:
            if msg.role == "user":
                content.append(f"**You:** {msg.content}")
            else:
                content.append(f"**Assistant:** {msg.content}")
            content.append("")  # Empty line
        
        return "\n".join(content)

class SessionManager:
    """Manages multiple chat sessions"""
    
    def __init__(self):
        self.sessions: List[ChatSession] = []
        self.active_session_index: int = 0
        self._create_initial_session()
    
    def _create_initial_session(self) -> None:
        """Create the first session"""
        self.sessions.append(ChatSession(name="Ollama/llama3"))
    
    def add_session(self, name: str = None) -> ChatSession:
        """Add a new session"""
        if name is None:
            name = f"Chat {len(self.sessions) + 1}"
        
        session = ChatSession(name=name)
        self.sessions.append(session)
        return session
    
    def get_active_session(self) -> ChatSession:
        """Get currently active session"""
        if not self.sessions:
            self._create_initial_session()
        return self.sessions[self.active_session_index]
    
    def set_active_session(self, index: int) -> None:
        """Set active session by index"""
        if 0 <= index < len(self.sessions):
            self.active_session_index = index
    
    def delete_session(self, index: int) -> None:
        """Delete a session"""
        if len(self.sessions) > 1 and 0 <= index < len(self.sessions):
            del self.sessions[index]
            if self.active_session_index >= len(self.sessions):
                self.active_session_index = len(self.sessions) - 1
