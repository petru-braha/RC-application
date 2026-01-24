from unittest import TestCase
from unittest.mock import MagicMock

from src.frontend.components.conn_box import ConnBox

class TestConnBox(TestCase):
    
    def setUp(self):
        self.on_click = MagicMock()
        self.on_close = MagicMock()
        self.box = ConnBox("conn1", self.on_click, self.on_close)

    def test_init(self):
        self.assertTrue(self.box.content)
        
    def test_on_click(self):
        self.box.on_click()
        self.on_click.assert_called()

    def test_on_close(self):
        icon_btn = self.box.content.controls[1]
        icon_btn.on_click()
        self.on_close.assert_called()
