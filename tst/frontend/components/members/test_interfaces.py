from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from src.frontend.components.members.interfaces import PresenceChangeable

class TestPresenceChangeable(TestCase):
    
    def test_show_hide(self):
        # Create a dummy class inheriting from PresenceChangeable
        class Dummy(PresenceChangeable):
            def __init__(self):
                self._page = MagicMock()
            
            @property
            def page(self):
                return self._page

        dummy = Dummy()
        
        # Test show
        dummy.show()
        self.assertTrue(dummy.visible)
        dummy.page.update.assert_called()
        
        # Test hide
        dummy.hide()
        self.assertFalse(dummy.visible)
        dummy.page.update.assert_called()
