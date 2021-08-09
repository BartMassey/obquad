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

        self.graphic = Canvas(self)
        self.graphic.pack(side="top")
    
    def enter_decimal(self, event):
        value = self.decimal_value.get()
        value = decimal_to_quad(value)
        if value is None:
            self.quad_value.set("")
            self.decimal_value.set("")
            return
        self.quad_value.set(value)

    def enter_quad(self, event):
        value = self.quad_value.get()
        value = quad_to_decimal(value)
        if value is None:
            self.quad_value.set("")
            self.decimal_value.set("")
            return
        self.decimal_value.set(value)

root = Tk()
app = Application(master=root)
app.mainloop()
