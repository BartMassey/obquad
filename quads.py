from tkinter import *
from tkinter.ttk import *

def decimal_to_quad(decimal):
    try:
        value = int(decimal)
    except:
        return None
    digits = ""
    while value > 0:
        digits = chr(ord('0') + value % 4) + digits
        value //= 4
    return digits

def quad_to_decimal(quad):
    value = 0
    for d in quad:
        digit = ord(d) - ord('0')
        if digit not in {0, 1, 2, 3}:
            return None
        value *= 4
        value += digit
    return str(value)

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.decimal = Entry(self)
        self.decimal.pack(side="top")
        self.decimal_value = StringVar()
        self.decimal["textvariable"] = self.decimal_value
        self.decimal.bind('<Key-Return>', self.enter_decimal)

        self.quad = Entry(self)
        self.quad.pack(side="top")
        self.quad_value = StringVar()
        self.quad["textvariable"] = self.quad_value
        self.quad.bind('<Key-Return>', self.enter_quad)

        d = 288
        self.graphic_size = d
        self.graphic = Canvas(width=d, height=d)
        self.graphic.pack(side="top")
        self.render_graphic()
    
    def refresh(self, decimal, quad):
        if decimal is None or quad is None:
            decimal = ""
            quad = ""
        self.decimal_value.set(decimal)
        self.quad_value.set(quad)
        self.render_graphic()


    def enter_decimal(self, event):
        decimal = self.decimal_value.get()
        quad = decimal_to_quad(decimal)
        self.refresh(decimal, quad)

    def enter_quad(self, event):
        quad = self.quad_value.get()
        decimal = quad_to_decimal(quad)
        self.refresh(decimal, quad)

    def render_graphic(self):
        cv = self.graphic
        d = self.graphic_size // 24
        spots = {(r, c) for r in range(5) for c in range(5)}
        missing = {(r, c) for r in (0, 2, 4) for c in (0, 2, 4)}
        missing -= {(2, 2)}
        spots -= missing

        def coord(r, c):
            x = 2 * (c + 1) * d + 6 * d
            y = 2 * (r + 1) * d + 6 * d
            return x, y

        for r, c in spots:
            x0, y0 = coord(r, c)
            r = d // 3
            cv.create_oval(x0 - r, y0 - r, x0 + r, y0 + r, fill="#000")

        def render_digit(start, digit):
            if digit == '0':
                return

            r, c = start
            x0, y0 = coord(r, c)

            if digit == '1':
                x1, y1 = coord(r - 1, c)
                cv.create_line(x0, y0, x1, y1, fill="#000")
                return

            if digit == '2':
                x1, y1 = coord(r + 1, c)
                cv.create_line(x0, y0, x1, y1, fill="#000")
                x1, y1 = coord(r, c + 1)
                cv.create_line(x0, y0, x1, y1, fill="#000")
                return

            if digit == '3':
                x1, y1 = coord(r, c + 1)
                cv.create_line(x0, y0, x1, y1, fill="#000")
                x1, y1 = coord(r, c - 1)
                cv.create_line(x0, y0, x1, y1, fill="#000")
                x1, y1 = coord(r - 1, c)
                cv.create_line(x0, y0, x1, y1, fill="#000")
                return

            assert False

        starts = (
            (2, 2),
            (3, 3),
            (1, 3),
            (1, 1),
            (3, 1),
        )

        for i, digit in enumerate(reversed(self.quad_value.get())):
            if i >= 5:
                break
            render_digit(starts[i], digit)

root = Tk()
app = Application(master=root)
app.mainloop()
