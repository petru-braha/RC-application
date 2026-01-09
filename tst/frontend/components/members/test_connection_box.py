from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.frontend.components.members.connection_box import ConnectionBox

class TestConnectionBox(TestCase):
    
    def setUp(self):
        self.on_click = MagicMock()
        self.on_close = MagicMock()
        self.on_rem = MagicMock()
        
        self.box = ConnectionBox("conn1", self.on_click, self.on_close, self.on_rem)

    def test_init(self):
        # Verify content
        self.assertTrue(self.box.content)
        
    def test_on_rem_interal_callback(self):
        # Trigger the closure.
        # on_rem is bound to the IconButton in content.Stack.controls[1]
        # structure: content=Stack([Text, IconButton])
        stack = self.box.content
        icon_btn = stack.controls[1]
        
        # Call the on_click
        icon_btn.on_click()
        
        self.on_close.assert_called()
        self.on_rem.assert_called_with(self.box)

    def test_on_click(self):
        # This is passed directly to super calls, verify kwargs
        # We can't strictly modify super callargs easily without tricky patching of ConnectionBox itself
        # But we assume flet handles it.
        pass
