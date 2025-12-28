import selectors

class SelectorHolder:
    """
    """
    
    SELECTOR: selectors.BaseSelector

    @staticmethod
    def open():
        SelectorHolder.SELECTOR = selectors.DefaultSelector()
    
    @staticmethod
    def close():
        SelectorHolder.SELECTOR.close()
