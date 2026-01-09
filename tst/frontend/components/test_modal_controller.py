from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from core.exceptions import ConnectionCountError
from src.frontend.components.modal_controller import ModalController

class TestModalController(TestCase):
    
    def setUp(self):
        # Patch dependencies used in __init__ or methods
        self.manual_patch = patch("src.frontend.components.modal_controller.ManualConnect")
        self.mock_manual_cls = self.manual_patch.start()
        self.addCleanup(self.manual_patch.stop)
        
        self.url_patch = patch("src.frontend.components.modal_controller.UrlConnect")
        self.mock_url_cls = self.url_patch.start()
        self.addCleanup(self.url_patch.stop)
        
        self.conn_patcher = patch("src.frontend.components.modal_controller.Connection")
        self.mock_conn_cls = self.conn_patcher.start()
        self.addCleanup(self.conn_patcher.stop)
        
        self.enque_new_patcher = patch("src.frontend.components.modal_controller.enque_new_connection")
        self.mock_enque_new = self.enque_new_patcher.start()
        self.addCleanup(self.enque_new_patcher.stop)
        
        self.enque_close_patcher = patch("src.frontend.components.modal_controller.enque_close_connection")
        self.mock_enque_close = self.enque_close_patcher.start()
        self.addCleanup(self.enque_close_patcher.stop)

        # Also patch Chat and ConnectionBox for on_continue
        self.chat_patch = patch("src.frontend.components.modal_controller.Chat")
        self.mock_chat_cls = self.chat_patch.start()
        self.addCleanup(self.chat_patch.stop)
             
        self.box_patch = patch("src.frontend.components.modal_controller.ConnectionBox")
        self.mock_box_cls = self.box_patch.start()
        self.addCleanup(self.box_patch.stop)
        
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
        
        # Patch page property on ModalController class
        self.page_patcher = patch.object(ModalController, 'page', new_callable=PropertyMock)
        self.mock_page_val = MagicMock()
        self.mock_page_prop = self.page_patcher.start()
        self.mock_page_prop.return_value = self.mock_page_val
        self.addCleanup(self.page_patcher.stop)
        
        self.controller.hide = MagicMock()
        # ModalController init creates url_view and manual_view using mocks
        self.controller.url_view = self.mock_url_cls.return_value
        self.controller.manual_view = self.mock_manual_cls.return_value

    def test_init(self):
        self.assertFalse(self.controller.is_manual)
        self.assertFalse(self.controller.visible)
        # Verify ManualConnect and UrlConnect initialized (mocks)

    def test_switch_modal(self):
        # Initial state is URL view (is_manual=False)
        self.controller.content = self.controller.url_view
        
        # Switch to Manual
        self.controller.switch_modal(None)
        self.assertTrue(self.controller.is_manual)
        self.assertEqual(self.controller.content, self.controller.manual_view)
        self.mock_page_val.update.assert_called()
        
        # Switch back to URL
        self.controller.switch_modal(None)
        self.assertFalse(self.controller.is_manual)
        self.assertEqual(self.controller.content, self.controller.url_view)

    def test_on_continue_success(self):
        mock_conn = MagicMock()
        self.mock_conn_cls.return_value = mock_conn
        mock_conn.addr = "localhost:6379"
        
        self.controller.on_continue(("localhost", "6379", "user", "pass"))
        
        # 1. Connection created
        self.mock_conn_cls.assert_called_with("localhost", "6379", "user", "pass")
        
        # 2. Chat created and selected
        self.on_chat_sel.assert_called() # Called with chat obj
        
        # 3. ConnectionBox created and added to agenda
        self.on_agenda_add.assert_called()
        
        # 4. Connection enqued to reactor
        self.mock_enque_new.assert_called()
        
        # 5. Modal hidden (visible=False)
        self.assertFalse(self.controller.visible) # hide() sets visible=False and calls update() but we mocked it?
                                                  # hide is mixin from PresenceChangeable or just method?
                                                  # Wait, hide() is not defined in ModalController or ControllerBase.
                                                  # Inherits from PresenceChangeable?
                                                  # Yes: class ModalController(..., PresenceChangeable)

    def test_on_continue_connection_error(self):
        self.mock_conn_cls.side_effect = ConnectionCountError("Too many")
        
        self.controller.on_continue(("a", "b"))
        
        self.on_chat_sel.assert_not_called()
        self.on_agenda_add.assert_not_called()
        self.mock_enque_new.assert_not_called()

    def test_connection_cleanup_callback(self):
        # Test the closure defined inside on_continue
        mock_conn = MagicMock()
        self.mock_conn_cls.return_value = mock_conn
        
        self.controller.on_continue(("a", "b"))
        
        # Extract arguments passed to ConnectionBox
        # call_args[1] is kwargs
        kwargs = self.mock_box_cls.call_args[1]
        on_close_cb = kwargs['on_connection_close']
            
        # Execute callback
        on_close_cb()
            
        self.mock_enque_close.assert_called_with(mock_conn)
        self.on_chat_rem.assert_called()
