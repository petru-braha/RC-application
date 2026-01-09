from unittest import TestCase
from unittest.mock import MagicMock, patch, AsyncMock, PropertyMock
import asyncio

from src.frontend.components.members.chat import Chat

class TestChat(TestCase):
    
    def setUp(self):
        self.on_enter = MagicMock()
        self.chat = Chat("my_chat", self.on_enter)
        
        # Patch page property on Chat class to avoid RuntimeError
        self.page_patcher = patch.object(Chat, 'page', new_callable=PropertyMock)
        self.mock_page_val = MagicMock()
        self.mock_page_prop = self.page_patcher.start()
        self.mock_page_prop.return_value = self.mock_page_val
        self.addCleanup(self.page_patcher.stop)
        self.chat._page = self.mock_page_val # Keep consistency if needed
        self.mock_page_val.run_task = MagicMock()
        
        # Mock internals for interaction verification
        self.chat.history_box = MagicMock()
        self.chat.history_box.update = MagicMock()
        self.chat.cmd_input = MagicMock()
        self.chat.cmd_input.value = ""

    def test_init(self):
        # Real init check
        self.assertTrue(self.chat.content)
        # We can't check assert_called on real classes easily.
        # Verify structure setup
        pass

    def test_on_submit_empty(self):
        self.chat.cmd_input.value = ""
        
        # Run async method
        asyncio.run(self.chat.on_submit(None))
        
        self.on_enter.assert_not_called()

    def test_on_submit_valid(self):
        self.chat.cmd_input.value = "GET key"
        self.chat.cmd_input.focus = AsyncMock() # Mock awaitable
        
        asyncio.run(self.chat.on_submit(None))
        
        self.on_enter.assert_called_with("GET key")
        self.chat.cmd_input.focus.assert_called()
        self.assertEqual(self.chat.cmd_input.value, "")
        
        # Verify bubble added
        self.chat.history_box.controls.append.assert_called()
    
    def test_on_response(self):
        # on_response queues a task on page
        self.chat.on_response("OK")
        
        self.mock_page_val.run_task.assert_called()
        
        # Extract the task function and run it
        task_func = self.mock_page_val.run_task.call_args[0][0]
        asyncio.run(task_func())
        
        self.chat.history_box.controls.append.assert_called()
        self.chat.history_box.update.assert_called()
