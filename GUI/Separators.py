from PySide6.QtWidgets import QFrame



class HorizontalLineSeparator(QFrame):
    """ A simple horizontal line so separate sections """
    
    def __init__(self):
        super().__init__()
        
        self.setFrameShape(QFrame.HLine)    # Horizontal line
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(1)