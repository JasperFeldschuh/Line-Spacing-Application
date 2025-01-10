import os
from PIL import ImageTk
from tkinter import Tk, Button, Frame, BOTTOM, CENTER, TOP, filedialog, simpledialog, Label
from cp2png import *
from cp import *
import time

def is_equal(a, b):
    return abs(a - b) < 1e-9

path = ""
cp_image = ""
image_copy = ""
cp = ""
spacing_factor = 0

def open_image(image, scaled):
    if not scaled:
        image = image.resize((int(image.width / image.height * 770), 770))

    photo = ImageTk.PhotoImage(image)
    label.image = photo
    label.config(image=photo)

def open_CP():
    global path, cp_image, image_copy, cp
    path = filedialog.askopenfilename()
    print(f'path {path}')
    cp = Cp(path)
    #space_lines(cp, 1)
    #cp_image = cp2png(cp,770)
    cp_image = cp2png(cp, 770)
    image_copy = cp_image.copy()
    open_image(cp_image, True)

def increase_spacing():
    global cp_image, spacing_factor, image_copy
    image_copy = cp_image.copy()
    spacing_factor += 0.5
    image_copy = update_png(cp, space_lines_fast(cp, spacing_factor), image_copy, 770)
    open_image(image_copy, True)

def decrease_spacing():
    global cp_image, spacing_factor, image_copy
    image_copy = cp_image.copy()
    spacing_factor -= 0.5
    if spacing_factor < 0:
        spacing_factor = 0

    image_copy = update_png(cp, space_lines_fast(cp, spacing_factor), image_copy, 770)
    open_image(image_copy, True)

def save_CP():
    global cp_image
    file = filedialog.asksaveasfile(mode='w', defaultextension=".png",
                                    filetypes=(("PNG file", "*.png"), ("All Files", "*.*")))
    if file:
        abs_path = os.path.abspath(file.name)
        cp_image.save(abs_path, "PNG")

def default_save():
    global path, cp_image
    image_path = path.replace(".cp", ".png")
    cp_image.save(image_path, "PNG")

def default_action():
    global path, cp, cp_image
    path = "G:/My Drive/Jasper Crease Patterns/CP Optimizer/Test CPs for Program/Test Case 1.cp"
    path = "G:/My Drive/Jasper Crease Patterns/PNG to CP/Test cps for program/Dragonfly.cp"
    #path = "G:/My Drive/Jasper Crease Patterns/CP Optimizer/Test CPs for Program/filled grid.cp"
    cp = Cp(path)
    #cp_image = cp2png(cp, 770)
    cp_image = cp2png(cp, 770)

    decrease_spacing()

def open_original_image():
    global image_copy, cp_image
    open_image(cp_image, True)


window = Tk()
window.geometry("1000x800")
window.title('CP to PNG for Laser Cutter')

label = Label(window, image="")
label.pack()

toolbar = Frame(window)
toolbar.pack(side=BOTTOM)

Button(toolbar, text='+', command=increase_spacing).grid(row=0, column=1)
Button(toolbar, text='-', command=decrease_spacing).grid(row=0, column=2)
Button(toolbar, text='Open CP', command=open_CP).grid(row=0, column=0)
Button(toolbar, text='Save CP', command=save_CP).grid(row=0, column=3)
Button(toolbar, text='Default Save', command=default_save).grid(row=0, column=4)
Button(toolbar, text='Default Action', command=default_action).grid(row=0, column=4)
Button(toolbar, text='Original Image', command=open_original_image).grid(row=0, column=5)


window.mainloop()  # Displays the window


