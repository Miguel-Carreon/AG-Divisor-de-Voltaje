import random
import math
import time
import tkinter as tk
from tkinter.constants import GROOVE, RAISED
from tkinter.font import BOLD
from PIL import Image, ImageTk

vin = 0
vout = 0

root = tk.Tk()
root.title("Calculadora de resistencias para Divisor de Voltaje")

canvas = tk.Canvas(root, width=1200, height=600, bg='white')
canvas.grid(columnspan=3, rowspan=8)

#title
title = tk.Label(root, text="Calculadora de valores de resistencias para un Divisor de Voltaje", fg='#4550e6', bg='white', font=('Trebuchet MS', 20, 'bold'))
title.grid(columnspan=3, column=0, row=0)

#entry1 title
entry1_title = tk.Label(root, text="Ingrese voltaje de entrada (Vin)", fg='#4550e6', bg='white', font=('Trebuchet MS', 12, 'bold'))
entry1_title.grid(column=0, row=1)

#entry1
entry1_text = tk.StringVar()
entry1 = tk.Entry(root, textvariable=entry1_text, fg ='grey', font=('Trebuchet MS', 11),width = 40)
entry1_text.set("Ingresar voltaje...")
entry1.grid(column=0, row=2)

#entry2 title
entry2_title = tk.Label(root, text="Ingrese voltaje de salida (Vout)", fg='#4550e6', bg='white', font=('Trebuchet MS', 12, 'bold'))
entry2_title.grid(column=0, row=4)

#entry2
entry2_text = tk.StringVar()
entry2 = tk.Entry(root, textvariable=entry2_text, fg='grey', font=('Trebuchet MS', 11),width = 40)
entry2_text.set("Ingresar voltaje...")
entry2.grid(column=0, row=5)

#diagram
diagram = Image.open('DV_rescaled.png')
diagram = ImageTk.PhotoImage(diagram)
diagram_label = tk.Label(image = diagram,bg='white')
diagram_label.image = diagram
diagram_label.grid(rowspan=7, column=2, row=0)

def run_algorithm():
    vin = entry1.get
    vout = entry2.get

    vin = int(vin)
    vout = int(vout)

    result = vin + vout

    new_label = tk.Label(root, text="Answer is " + result)
    new_label.grid(columnspan=3, column=0, row=7)

#calculate button
calculate_text = tk.StringVar()
calculate_btn = tk.Button(root, textvariable=calculate_text, fg='white', bg='#4550e6', font=('Trebuchet MS', 11, 'bold'), command=run_algorithm)
calculate_btn.config(width=10, height=2, fg='white', borderwidth=0)
calculate_text.set("Calcular")
calculate_btn.grid(columnspan=3, column=0, row=6)

root.mainloop()