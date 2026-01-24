import asyncio
from unittest import TestCase
from unittest.mock import MagicMock, AsyncMock, patch

from src.util import close_page, add_conn, rem_conn, core

class TestUtil(TestCase):
    
    chat_patch = patch("src.util.Chat")
    box_patch = patch("src.util.ConnBox")

    def setUp(self):
        self.mock_chat_cls = self.chat_patch.start()
        self.mock_box_cls = self.box_patch.start()
        
        self.mock_reactor = MagicMock()
        self.mock_layout = MagicMock()
        self.mock_layout.conn_boxes_dict = {}

    def tearDown(self):
        self.chat_patch.stop()
        self.box_patch.stop()

    def test_close_page(self):
        mock_event = MagicMock()
        mock_page = MagicMock()
        mock_page.window.destroy = AsyncMock()
        mock_page.window.close = AsyncMock()
        
        asyncio.run(close_page(mock_event, mock_page))
        
        mock_event.clear.assert_called()
        mock_page.window.destroy.assert_called()
        mock_page.window.close.assert_called()

    def test_add_conn_success(self):
        mock_conn = MagicMock()
        self.mock_reactor.enqueue_new_conn.return_value = mock_conn
        
        conn_data = ("localhost", "6379", "user", "pass")
        add_conn(conn_data, self.mock_reactor, self.mock_layout)
        
        self.mock_reactor.enqueue_new_conn.assert_called_with(conn_data)
        self.mock_box_cls.assert_called()
        self.mock_layout.agenda_frame.add_box.assert_called()
        self.mock_chat_cls.assert_called()
        self.mock_layout.chat_frame.sel_chat.assert_called()
        self.mock_reactor.bind_chat.assert_called_with(mock_conn, self.mock_chat_cls.return_value)
        
        self.assertIn(mock_conn, self.mock_layout.conn_boxes_dict)

    @patch("src.util.logger")
    def test_add_conn_failure(self, mock_logger):
        self.mock_reactor.enqueue_new_conn.side_effect = core.ConnectionCountError("Full")
        
        conn_data = ("localhost", "6379")
        add_conn(conn_data, self.mock_reactor, self.mock_layout)
        
        self.mock_reactor.enqueue_new_conn.assert_called_with(conn_data)
        mock_logger.error.assert_called()
        
        self.mock_box_cls.assert_not_called()
        self.mock_layout.agenda_frame.add_box.assert_not_called()
        self.mock_chat_cls.assert_not_called()
        self.mock_layout.chat_frame.sel_chat.assert_not_called()
        self.mock_reactor.bind_chat.assert_not_called()
        
        self.assertEqual(len(self.mock_layout.conn_boxes_dict), 0)

    def test_add_conn_callbacks(self):
        """
        Verify lambda callbacks are wired correctly.
        """
        mock_conn = MagicMock()
        self.mock_reactor.enqueue_new_conn.return_value = mock_conn
        
        conn_data = ("host.com", "6379")
        add_conn(conn_data, self.mock_reactor, self.mock_layout)
        
        box_kwargs = self.mock_box_cls.call_args[1]
        on_click = box_kwargs['on_click']
        on_close = box_kwargs['on_close']
        
        on_click()
        self.mock_layout.chat_frame.sel_chat.assert_called()
        
        on_close()
        self.mock_reactor.enqueue_close_conn.assert_called()

    def test_rem_conn(self):
        mock_conn = MagicMock()
        mock_box = MagicMock()
        
        self.mock_layout.conn_boxes_dict = {mock_conn: mock_box}
        rem_conn(mock_conn, self.mock_reactor, self.mock_layout)
        
        self.mock_reactor.enqueue_close_conn.assert_called_with(mock_conn)
        self.mock_layout.agenda_frame.rem_box.assert_called_with(mock_box)
        self.mock_layout.chat_frame.rem_chat.assert_called()
