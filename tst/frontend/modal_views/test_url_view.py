from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.frontend.modal_views.url_view import UrlView

class TestUrlConnect(TestCase):
    
    process_patcher = patch("src.frontend.modal_views.url_view.core.process_redis_url")
    
    def setUp(self):
        self.mock_process = TestUrlConnect.process_patcher.start()
        self.on_continue = MagicMock()
        self.switch_btn = MagicMock()
        self.close_btn = MagicMock()
        self.modal = UrlView(self.on_continue, self.switch_btn, self.close_btn)
    
    def tearDown(self) -> None:
        TestUrlConnect.process_patcher.stop()

    def test_init(self):
        self.assertTrue(self.modal.content)

    def test_on_process_url_success(self):
        self.modal.url_input.value = "redis://Localhost"
        expected_components = ("localhost", "6379", "", "", "0")
        self.mock_process.return_value = expected_components
        
        self.modal.on_process_url(None)
        
        self.mock_process.assert_called_with("redis://Localhost")
        self.assertEqual(self.modal.url_input.value, "")
        self.on_continue.assert_called_with(expected_components)

    def test_on_process_url_failure(self):
        self.modal.url_input.value = "invalid"
        self.mock_process.side_effect = ValueError("Invalid")
        
        self.modal.on_process_url(None)
        
        self.on_continue.assert_not_called()
        self.assertEqual(self.modal.url_input.value, "")
