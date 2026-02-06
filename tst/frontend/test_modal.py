from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from src.frontend.modal import Modal

class TestModal(TestCase):

    manual_patch = patch("src.frontend.modal.ManualView")
    url_patch = patch("src.frontend.modal.UrlView")
    page_patcher = patch.object(Modal, 'page', new_callable=PropertyMock)

    def setUp(self):
        self.mock_manual_cls = TestModal.manual_patch.start()
        self.mock_url_cls = TestModal.url_patch.start()
        
        self.add_conn_callback = MagicMock()
        self.controller = Modal(self.add_conn_callback)

        # Patch page property on Modal class.
        self.mock_page_val = MagicMock()
        self.mock_page_prop = TestModal.page_patcher.start()
        self.mock_page_prop.return_value = self.mock_page_val

        self.controller.hide = MagicMock()
        self.controller.url_view = self.mock_url_cls.return_value
        self.controller.manual_view = self.mock_manual_cls.return_value

    def tearDown(self):
        TestModal.manual_patch.stop()
        TestModal.url_patch.stop()
        TestModal.page_patcher.stop()

    def test_init(self):
        """
        Verify ManualView and UrlView mocks are initialized.
        """
        self.assertFalse(self.controller.is_manual)
        self.assertFalse(self.controller.visible)

    def test_switch_modal(self):
        """
        Verify the initial state, and the switching between manual and url views.
        """
        # Initial state is UrlConnect.
        self.assertFalse(self.controller.is_manual)
        self.controller.switch_view(None)
        self.assertTrue(self.controller.is_manual)
        self.assertEqual(self.controller.content, self.mock_manual_cls.return_value)
        self.mock_page_val.update.assert_called()
        
        # Back to url model.
        self.controller.switch_view(None)
        self.assertFalse(self.controller.is_manual)
        self.assertEqual(self.controller.content, self.mock_url_cls.return_value)

    def test_on_continue(self):
        """
        Verify the on_continue method calls the callback and hides the modal.
        """
        conn_data = ("localhost", "6379")
        self.controller.on_continue(conn_data)
        
        self.add_conn_callback.assert_called_with(conn_data)
        self.controller.hide.assert_called()
