from unittest import TestCase
from unittest.mock import MagicMock

from src.frontend.modal_views.manual_view import ManualView

class TestManualConnect(TestCase):
    
    def setUp(self):
        self.on_continue = MagicMock()
        self.switch_btn = MagicMock()
        self.close_btn = MagicMock()
        self.modal = ManualView(self.on_continue, self.switch_btn, self.close_btn)

    def test_init(self):
        self.assertTrue(self.modal.content)

    def test_on_process_manual(self):
        self.modal.host_input.value = "host"
        self.modal.port_input.value = "port"
        self.modal.user_input.value = "user"
        self.modal.pass_input.value = "pass"
        self.modal.db_input.value = "1"
        
        self.modal.on_process_manual(None)
        
        expected_data = ("host", "port", "user", "pass", "1")
        self.on_continue.assert_called_with(expected_data)
