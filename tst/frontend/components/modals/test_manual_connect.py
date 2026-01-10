from unittest import TestCase
from unittest.mock import MagicMock

from src.frontend.components.modals.manual_connect import ManualConnect

class TestManualConnect(TestCase):
    
    def setUp(self):
        self.on_continue = MagicMock()
        self.switch_btn = MagicMock()
        self.close_btn = MagicMock()
        
        self.modal = ManualConnect(self.on_continue, self.switch_btn, self.close_btn)
        self.modal._page = MagicMock()

    def test_init(self):
        self.assertTrue(self.modal.content)

    def test_on_process_manual(self):
        # Setup input values on REAL TextFields
        self.modal.host_input.value = "host"
        self.modal.port_input.value = "port"
        self.modal.user_input.value = "user"
        self.modal.pass_input.value = "pass"
        self.modal.db_input.value = "1"
        
        self.modal.on_process_manual(None)
        
        expected_data = ("host", "port", "user", "pass", "1")
        self.on_continue.assert_called_with(expected_data)
