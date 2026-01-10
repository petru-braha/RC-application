from unittest import TestCase
from unittest.mock import MagicMock

from src.frontend.components.agenda import Agenda

class TestAgenda(TestCase):
    
    def setUp(self):
        self.agenda = Agenda()
        self.agenda._page = MagicMock()
        self.agenda.list_view = MagicMock()
        self.agenda.update = MagicMock()

    def tearDown(self):
        self.agenda.list_view.controls = []

    def test_add_box(self):
        mock_box = MagicMock()
        
        self.agenda.add_box(mock_box)
        
        self.agenda.list_view.controls.append.assert_called_with(mock_box)
        self.agenda.update.assert_called()

    def test_rem_box(self):
        mock_box = MagicMock()
        
        self.agenda.rem_box(mock_box)
        
        self.agenda.list_view.controls.remove.assert_called_with(mock_box)
        self.agenda.update.assert_called()
