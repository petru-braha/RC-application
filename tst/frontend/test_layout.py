from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.frontend.layout import Layout

class TestLayout(TestCase):
    agenda_patch = patch("src.frontend.layout.Agenda")
    chatframe_patch = patch("src.frontend.layout.ChatFrame")
    modal_patch = patch("src.frontend.layout.ModalController")
    leftpanel_patch = patch("src.frontend.layout.LeftPanel")
        
    def setUp(self):
        self.mock_agenda_cls = TestLayout.agenda_patch.start()
        self.mock_chatframe_cls = TestLayout.chatframe_patch.start()
        self.mock_modal_cls = TestLayout.modal_patch.start()
        self.mock_leftpanel_cls = TestLayout.leftpanel_patch.start()
        
        self.layout = Layout()

    def tearDown(self):
        TestLayout.agenda_patch.stop()
        TestLayout.chatframe_patch.stop()
        TestLayout.modal_patch.stop()
        TestLayout.leftpanel_patch.stop()

    def test_init(self):
        self.mock_agenda_cls.assert_called()
        self.mock_chatframe_cls.assert_called()
        self.mock_modal_cls.assert_called()
        self.mock_leftpanel_cls.assert_called()
