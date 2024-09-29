from tkinter import Frame, Button
from studio import WidgetMeta
class ScrolledListBox(Frame):
    def __init__(self, master, **kw):

class ScrolledListBoxMeta(DPad, metaclass=WidgetMeta):
    display_name = 'Scrolled List'
    impl = ScrolledListBox
    icon = "gaming"
    is_container = False
    initial_dimensions = 100, 100