from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.frontend.left_panel import LeftPanel

class TestLeftPanel(TestCase):
    
    def setUp(self):
        self.mock_agenda = MagicMock()
        self.mock_btn = MagicMock()
        self.panel = LeftPanel(self.mock_agenda, self.mock_btn)

    def test_init(self):
        col = self.panel.content
        self.assertIn(self.mock_agenda, col.controls)
        
        footer = col.controls[-1]
        self.assertIn(self.mock_btn, footer.controls)
