from unittest import TestCase
from unittest.mock import MagicMock

from src.frontend.agenda_frame import AgendaFrame

class TestAgendaFrame(TestCase):
    
    def setUp(self):
        self.show_modal_callback = MagicMock()
        self.agenda_frame = AgendaFrame(self.show_modal_callback)
        self.agenda_frame.update = MagicMock()

    def test_init(self):
        content = self.agenda_frame.content
        self.assertIn(self.agenda_frame.conn_boxes, content.controls[0].controls)
        
        footer = content.controls[-1]
        btn = footer.controls[0]
        self.assertEqual(btn.on_click, self.show_modal_callback)

    def test_on_click(self):
        content = self.agenda_frame.content
        footer = content.controls[-1]
        btn = footer.controls[0]
        btn.on_click()
        self.show_modal_callback.assert_called()

    def test_add_box(self):
        mock_box = MagicMock()
        self.agenda_frame.add_box(mock_box)
        
        self.assertIn(mock_box, self.agenda_frame.conn_boxes.controls)
        self.agenda_frame.update.assert_called()

    def test_rem_box(self):
        mock_box = MagicMock()
        self.agenda_frame.add_box(mock_box)
        
        self.agenda_frame.rem_box(mock_box)
        
        self.assertNotIn(mock_box, self.agenda_frame.conn_boxes.controls)
        self.agenda_frame.update.assert_called()
