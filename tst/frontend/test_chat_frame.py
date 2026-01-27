from unittest import TestCase
from unittest.mock import MagicMock

from src.frontend.chat_frame import ChatFrame

class TestChatFrame(TestCase):
    
    def setUp(self):
        self.chat_frame = ChatFrame()
        self.chat_frame.update = MagicMock()
        self.chat_frame.default_layer = MagicMock()
        self.chat_frame.content = self.chat_frame.default_layer

    def test_init(self):
        self.assertEqual(self.chat_frame.content, self.chat_frame.default_layer)

    def test_sel_chat(self):
        mock_chat = MagicMock()
        
        self.chat_frame.sel_chat(mock_chat)
        
        self.assertEqual(self.chat_frame.content, mock_chat)
        self.chat_frame.update.assert_called()

    def test_rem_chat(self):
        mock_chat = MagicMock()
        self.chat_frame.content = mock_chat
        
        self.chat_frame.rem_chat()
        
        self.assertEqual(self.chat_frame.content, self.chat_frame.default_layer)
        self.chat_frame.update.assert_called()
