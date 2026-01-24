from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.frontend.layout import Layout

class TestLayout(TestCase):

    agendaframe_patch = patch("src.frontend.layout.AgendaFrame")
    chatframe_patch = patch("src.frontend.layout.ChatFrame")
    modal_patch = patch("src.frontend.layout.Modal")
        
    def setUp(self):
        self.mock_chatframe_cls = TestLayout.chatframe_patch.start()
        self.mock_modal_cls = TestLayout.modal_patch.start()
        self.mock_agendaframe_cls = TestLayout.agendaframe_patch.start()
        
        self.add_conn_callback = MagicMock()
        self.layout = Layout(self.add_conn_callback)

    def tearDown(self):
        TestLayout.chatframe_patch.stop()
        TestLayout.modal_patch.stop()
        TestLayout.agendaframe_patch.stop()

    def test_init(self):
        self.mock_chatframe_cls.assert_called()
        self.mock_modal_cls.assert_called_with(add_conn_callback=self.add_conn_callback)
        self.mock_agendaframe_cls.assert_called()
