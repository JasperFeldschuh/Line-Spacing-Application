import tkinter.messagebox

from pdf2image import convert_from_path
import math
import os
from PIL import Image
from tkinter import Tk
from tkinter import Button
from tkinter import filedialog
from tkinter import Frame
from tkinter import BOTTOM
from tkinter import simpledialog


def get_file():
    return filedialog.askopenfilename()

columns = 3

def get_columns():
    global columns
    columns = simpledialog.askinteger('Set Columns', 'Enter the Number Of Columns')


excluded_indexes = []

def get_excluded_indexes():
    list_of_ints = True
    global excluded_indexes
    input = simpledialog.askstring('Exclude Pages', 'Enter the pages that you wish to exclude as a comma separated list')
    input_list = input.split(',')
    for i in range(len(input_list)):
        input_list[i] = input_list[i].strip(' ')

    for i in range(len(input_list)):
        try:
            input_list[i] = int(input_list[i])
        except:
            list_of_ints = False

    if(list_of_ints):
        excluded_indexes = input_list
        #print(input_list)
    else:
        tkinter.messagebox.showwarning('Invalid Page Number', message='Please enter valid page numbers')


def make_grid():
    # Store Pdf with convert_from_path function
    path_to_pdf = get_file()
    images = convert_from_path(path_to_pdf,
                               poppler_path=r"C:\Users\feldsj\Downloads\Release-24.02.0-0\poppler-24.02.0\Library\bin")

    print('Gathering Images')
    valid_images = []
    for i in range(len(images)):
        if i + 1 not in excluded_indexes:
            valid_images.append(images[i])

    rows = math.ceil(len(valid_images) / columns)
    width = valid_images[0].width
    height = valid_images[0].height
    canvas_width = columns * width
    canvas_height = rows * height

    canvas = Image.new(mode='RGB', size=(canvas_width, canvas_height), color=(222, 235, 247))

    x = 0
    y = 0
    for i in range(len(valid_images)):
        Image.Image.paste(canvas, valid_images[i], (x, y))
        x += width
        if (i + 1) % columns == 0:
            y += height
            x -= width * columns

    name = simpledialog.askstring('Name File', 'Enter the File Name')
    path_to_folder = "G:\\My Drive\\RPI\\2024 - 25\\Strengths of Materials\\Image grids\\"

    
    file_path = path_to_folder + name + ".pdf"
    canvas.save(file_path, 'PDF')
    print('Finished')
    window.destroy()



window = Tk()
window.geometry("500x500")
window.title('PDF to Image Grid')

toolbar = Frame(window)
toolbar.pack(side=BOTTOM)

Button(toolbar, text='Generate Grid', command=make_grid).grid(row=0, column=0)
Button(toolbar, text='Set Columns', command=get_columns).grid(row=0, column=1)
Button(toolbar, text='Exclude Pages', command=get_excluded_indexes).grid(row=0, column=2)
window.mainloop()  # Displays the window



