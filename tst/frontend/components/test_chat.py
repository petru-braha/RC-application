import asyncio
from unittest import TestCase
from unittest.mock import MagicMock, AsyncMock, PropertyMock, patch

from src.frontend.components.chat import Chat

class TestChat(TestCase):
    
    def setUp(self):
        self.on_enter = MagicMock()
        self.on_exit = MagicMock()
        self.chat = Chat("my_chat", self.on_enter, self.on_exit)
        
        self.page_patcher = patch.object(Chat, 'page', new_callable=PropertyMock)
        self.mock_page_val = MagicMock()
        self.mock_page_prop = self.page_patcher.start()
        self.mock_page_prop.return_value = self.mock_page_val
        self.addCleanup(self.page_patcher.stop)
        self.mock_page_val.run_task = MagicMock()
        
        # Mock internals for interaction verification
        self.chat.history_box = MagicMock()
        self.chat.history_box.update = MagicMock()
        self.chat.history_box.controls = MagicMock()
        self.chat.history_box.controls.clear = MagicMock()
        self.chat.history_box.controls.append = MagicMock()
        
        self.chat.cmd_input = MagicMock()
        self.chat.cmd_input.value = ""
        self.chat.cmd_input.focus = AsyncMock()

    def test_init(self):
        self.assertTrue(self.chat.content)

    def test_on_submit_empty(self):
        self.chat.cmd_input.value = ""
        
        asyncio.run(self.chat.add_req(None))
        
        self.on_enter.assert_not_called()

    def test_on_submit_valid(self):
        self.chat.cmd_input.value = "GET key"
        
        asyncio.run(self.chat.add_req(None))
        
        self.on_enter.assert_called_with("GET key")
        self.chat.cmd_input.focus.assert_called()
        self.assertEqual(self.chat.cmd_input.value, "")
        
        self.chat.history_box.controls.append.assert_called()
    
    def test_on_submit_clear(self):
        self.chat.cmd_input.value = "CLEAR"
        
        asyncio.run(self.chat.add_req(None))
        
        self.chat.history_box.controls.clear.assert_called()
        self.on_enter.assert_not_called()
        self.chat.cmd_input.focus.assert_called()

    def test_on_submit_exit(self):
        self.chat.cmd_input.value = "EXIT"
        
        asyncio.run(self.chat.add_req(None))
        
        self.on_exit.assert_called()
        self.on_enter.assert_not_called()
        self.chat.cmd_input.focus.assert_called()

    def test_add_res(self):
        asyncio.run(self.chat.add_res("OK"))
        
        self.chat.history_box.controls.append.assert_called()
        self.chat.history_box.update.assert_called()
