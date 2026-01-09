from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.frontend.layout import Layout

class TestLayout(TestCase):
    
    def setUp(self):
        # Patch keys: src.frontend.layout.Agenda, etc.
        self.agenda_patch = patch("src.frontend.layout.Agenda")
        self.mock_agenda_cls = self.agenda_patch.start()
        self.addCleanup(self.agenda_patch.stop)
        
        self.chatframe_patch = patch("src.frontend.layout.ChatFrame")
        self.mock_chatframe_cls = self.chatframe_patch.start()
        self.addCleanup(self.chatframe_patch.stop)
        
        self.modal_patch = patch("src.frontend.layout.ModalController")
        self.mock_modal_cls = self.modal_patch.start()
        self.addCleanup(self.modal_patch.stop)
        
        self.leftpanel_patch = patch("src.frontend.layout.LeftPanel")
        self.mock_leftpanel_cls = self.leftpanel_patch.start()
        self.addCleanup(self.leftpanel_patch.stop)

        self.layout = Layout()

    def test_init(self):
        self.mock_agenda_cls.assert_called()
        self.mock_chatframe_cls.assert_called()
        self.mock_modal_cls.assert_called()
        self.mock_leftpanel_cls.assert_called()
