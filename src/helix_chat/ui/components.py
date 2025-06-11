from textual.widgets import Input

class ChatInput(Input):
    """Enhanced input widget for chat"""
    
    def __init__(self, **kwargs):
        super().__init__(
            placeholder="Ask Anything...",
            **kwargs
        )
