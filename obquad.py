# Obduction™ Villain quad calculator
# Bart Massey 2021

from math import *
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
        master.title("obquad")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        frame = Frame(self)
        frame.pack(side="top")
        grid = frame.grid()

        label = Label(frame, text="Decimal")
        label.grid(row=0, column=0, sticky=E)
        self.decimal = Entry(frame)
        self.decimal.grid(row=0, column=1)
        self.decimal_value = StringVar()
        self.decimal["textvariable"] = self.decimal_value
        self.decimal.bind('<Key-Return>', self.enter_decimal)

        label = Label(frame, text="Quad")
        label.grid(row=1, column=0, sticky=E)
        self.quad = Entry(frame)
        self.quad.grid(row=1, column=1)
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
        size = self.graphic_size
        d = size // 24

        def coord(row, col):
            s = size / 2
            x = 2 * (col + 1) * d + 6 * d - s
            y = 2 * (row + 1) * d + 6 * d - s
            r = sqrt(x**2 + y**2)
            t = atan2(y, x)
            cx = int(r * cos(t - pi / 4) + s)
            cy = int(r * sin(t - pi / 4) + s)
            return cx, cy

        ra = d // 3

        def spot(r, c, fill="#000"):
            x, y = coord(r, c)
            cv.create_oval(x - ra, y - r, x + ra, y + ra, fill=fill)

        def line(r0, c0, r1, c1, fill="#000"):
            x0, y0 = coord(r0, c0)
            x1, y1 = coord(r1, c1)
            cv.create_line(x0, y0, x1, y1, fill=fill)

        cv.delete("all")
        cv.create_rectangle(
            size // 4,
            size // 4,
            3 * size //
            4, 3 * size // 4,
            fill="#fff",
        )
        line(0, 0, 0, 4, fill="#880")
        line(0, 4, 4, 4, fill="#880")
        line(4, 4, 4, 0, fill="#880")
        line(4, 0, 0, 0, fill="#880")

        spots = {(r, c) for r in range(5) for c in range(5)}
        missing = {(r, c) for r in (0, 2, 4) for c in (0, 2, 4)}
        missing -= {(2, 2)}
        spots -= missing
        for r, c in spots:
            spot(r, c)

        def render_digit(start, digit):
            if digit == '0':
                return

            r, c = start

            if digit == '1':
                line(r, c, r - 1, c)
                return

            if digit == '2':
                line(r, c, r + 1, c)
                line(r, c, r, c + 1)
                return

            if digit == '3':
                line(r, c, r, c + 1)
                line(r, c, r, c - 1)
                line(r, c, r - 1, c)
                return

            assert False

        starts = (
            (2, 2),
            (1, 3),
            (3, 3),
            (3, 1),
            (1, 1),
        )

        for i, digit in enumerate(reversed(self.quad_value.get())):
            if i >= 5:
                break
            render_digit(starts[i], digit)

root = Tk()
app = Application(master=root)
app.mainloop()
