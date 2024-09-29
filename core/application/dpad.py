from tkinter import Frame, Button
from studio import WidgetMeta

class DPad(Frame):

    def __init__(self, master, **kw):
        super(DPad, self).__init__(master, **kw)
        self.left = Button(self, text="L", padx=8, pady=5)
        self.right = Button(self, text="R", padx=8, pady=5)
        self.up = Button(self, text="U", padx=8, pady=5)
        self.down = Button(self, text="D", padx=8, pady=5)

        self.up.grid(row=0, column=1)
        self.left.grid(row=1, column=0)
        self.right.grid(row=1, column=2)
        self.down.grid(row=2, column=1)


class DPadMeta(DPad, metaclass=WidgetMeta):
    display_name = 'D Pad'
    impl = DPad
    icon = "gaming"
    is_container = False
    initial_dimensions = 90, 100