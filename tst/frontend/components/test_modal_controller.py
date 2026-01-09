from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from core.exceptions import ConnectionCountError
from src.frontend.components.modal_controller import ModalController

class TestModalController(TestCase):

    manual_patch = patch("src.frontend.components.modal_controller.ManualConnect")
    url_patch = patch("src.frontend.components.modal_controller.UrlConnect")
    conn_patcher = patch("src.frontend.components.modal_controller.Connection")
    enque_new_patcher = patch("src.frontend.components.modal_controller.enque_new_connection")
    enque_close_patcher = patch("src.frontend.components.modal_controller.enque_close_connection")
    chat_patch = patch("src.frontend.components.modal_controller.Chat")
    box_patch = patch("src.frontend.components.modal_controller.ConnectionBox")
    page_patcher = patch.object(ModalController, 'page', new_callable=PropertyMock)

    def setUp(self):
        self.mock_manual_cls = TestModalController.manual_patch.start()
        self.mock_url_cls = TestModalController.url_patch.start()
        self.mock_conn_cls = TestModalController.conn_patcher.start()
        self.mock_enque_new = TestModalController.enque_new_patcher.start()
        self.mock_enque_close = TestModalController.enque_close_patcher.start()
        self.mock_chat_cls = TestModalController.chat_patch.start()
        self.mock_box_cls = TestModalController.box_patch.start()
        
        self.on_agenda_add = MagicMock()
        self.on_agenda_rem = MagicMock()
        self.on_chat_sel = MagicMock()
        self.on_chat_rem = MagicMock()
        
        self.controller = ModalController(
            self.on_agenda_add,
            self.on_agenda_rem,
            self.on_chat_sel,
            self.on_chat_rem
        )

        # Patch page property on ModalController class.
        self.mock_page_val = MagicMock()
        self.mock_page_prop = TestModalController.page_patcher.start()
        self.mock_page_prop.return_value = self.mock_page_val

        self.controller.hide = MagicMock()
        self.controller.url_view = self.mock_url_cls.return_value
        self.controller.manual_view = self.mock_manual_cls.return_value

    def tearDown(self):
        TestModalController.manual_patch.stop()
        TestModalController.url_patch.stop()
        TestModalController.conn_patcher.stop()
        TestModalController.enque_new_patcher.stop()
        TestModalController.enque_close_patcher.stop()
        TestModalController.chat_patch.stop()
        TestModalController.box_patch.stop()
        TestModalController.page_patcher.stop()

    def test_init(self):
        """
        Verify ManualConnect and UrlConnect mocks are initialized.
        """
        self.assertFalse(self.controller.is_manual)
        self.assertFalse(self.controller.visible)

    def test_switch_modal(self):
        """
        Verify the initial state, and the switching between manual and URL views.
        """
        self.controller.content = self.controller.url_view
        
        self.controller.switch_modal(None)
        self.assertTrue(self.controller.is_manual)
        self.assertEqual(self.controller.content, self.controller.manual_view)
        self.mock_page_val.update.assert_called()
        
        self.controller.switch_modal(None)
        self.assertFalse(self.controller.is_manual)
        self.assertEqual(self.controller.content, self.controller.url_view)

    def test_on_continue_success(self):
        """
        Verify the on_continue method creates a connection, chat, and connection box.
        """
        mock_conn = MagicMock()
        self.mock_conn_cls.return_value = mock_conn
        mock_conn.addr = "localhost:6379"
        
        self.controller.on_continue(("localhost", "6379", "user", "pass"))
        
        self.mock_conn_cls.assert_called_with("localhost", "6379", "user", "pass")
        
        # Called with chat object.
        self.on_chat_sel.assert_called()
        
        # ConnectionBox created and added to agenda.
        self.on_agenda_add.assert_called()
        
        # Connection enqued to reactor.
        self.mock_enque_new.assert_called()
    
    def test_on_continue_connection_error(self):
        self.mock_conn_cls.side_effect = ConnectionCountError("Too many")
        
        self.controller.on_continue(("a", "b"))
        
        self.on_chat_sel.assert_not_called()
        self.on_agenda_add.assert_not_called()
        self.mock_enque_new.assert_not_called()

    def test_connection_cleanup_callback(self):
        mock_conn = MagicMock()
        self.mock_conn_cls.return_value = mock_conn
        
        self.controller.on_continue(("a", "b"))
        
        kwargs = self.mock_box_cls.call_args[1]
        on_close_callback = kwargs['on_connection_close']
            
        on_close_callback()
            
        self.mock_enque_close.assert_called_with(mock_conn)
        self.on_chat_rem.assert_called()
