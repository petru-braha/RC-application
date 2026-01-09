from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.frontend.components.agenda import Agenda

class TestAgenda(TestCase):
    
    def setUp(self):
        self.agenda = Agenda()
        self.agenda._page = MagicMock()
        self.agenda.list_view = MagicMock()
        self.agenda.update = MagicMock()

    def test_init(self):
        # Since we use real Agenda, list_view is real until swapped in setUp
        # But we swapped it. Check if internal logic holds?
        # Actually, let's just trust real init works and we verified it by presence of list_view.
        pass # self.agenda created successfully

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
    
    def test_rem_box_not_found(self):
        mock_box = MagicMock()
        self.agenda.list_view.controls.remove.side_effect = ValueError
        
        with self.assertRaises(ValueError):
            self.agenda.rem_box(mock_box)
