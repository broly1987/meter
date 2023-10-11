import subprocess
import tkinter as tk
from tkinter import ttk
import threading
from PIL import Image, ImageTk

import calculadora3
import meter
import performing
import  sys
import os

os.chdir(os.path.dirname(__file__))
def create_rounded_button(text, command):
    # Crear una imagen redondeada para el botón
    size = (200, 50)  # Tamaño del botón
    color = "blue"  # Color de fondo del botón
    corner_radius = 25  # Radio de las esquinas

    img = Image.new("RGB", size, color)
    img = Image.new("L", size)
    img.putalpha(255)
    width, height = img.size
    for x in range(width):
        for y in range(height):
            if (x - corner_radius) ** 2 + (y - corner_radius) ** 2 > corner_radius ** 2:
                img.putpixel((x, y), 0)

    # Convertir la imagen a PhotoImage
    img = ImageTk.PhotoImage(img)

    # Crear el botón
    button = ttk.Button(root, text=text, image=img, compound="center", command=command)
    button.image = img  # Mantener una referencia a la imagen para evitar que se elimine

    return button
# Funciones para ejecutar los scripts
def ejecutar_primer_script():
    try:
        meter.meter_pro()
    except Exception as e:
        print(f"Error with meter roll over app : {e}")

def ejecutar_segundo_script():
    try:
        calculadora3.cal_f()
    except Exception as e:
        print(f"Error with the search app : {e}")

def ejecutar_tercer_script():
    try:
        print('entrando a performing')
        sys.stdout = open("output.log", "w")
        sys.stderr = open("error.log", "w")
        root = tk.Tk()
        app = performing.PerformingApp(root)  # Crea una instancia de la clase PerformingApp desde el módulo performing
        root.mainloop()

    except Exception as e:
        print(f'Error loading performing {e}')
def ejecutar_tarea_larga():
    thread = threading.Thread(target=ejecutar_primer_script)
    thread.start()


# Crear una ventana principal
root = tk.Tk()
root.title(" Riviera App")
root.geometry("400x300")  # Cambia el tamaño de la ventana a 400x300
root.configure(bg='darkblue')  # Cambia el fondo a azul oscuro

# Estilo personalizado para los botones
style = ttk.Style()
style.configure("TButton", font=("Arial", 16), background="darkblue", foreground="black", relief="ridge", borderwidth=8)

# Etiqueta de título
titulo_label = ttk.Label(root, text="Excel Tool", font=("Helvetica", 24), background="darkblue", foreground="white")
titulo_label.pack(pady=20)  # Agrega espacio vertical alrededor de la etiqueta

# Botones para ejecutar los scripts
boton_primer_script = ttk.Button(root, text="Meter Roll Over", command=ejecutar_primer_script)
boton_primer_script.pack(pady=10)  # Agrega espacio vertical entre los botones

boton_otro_scriptdos = ttk.Button(root, text="Search Roll Over", command=ejecutar_segundo_script)
boton_otro_scriptdos.pack(pady=10)

boton_otro_scripttres = ttk.Button(root, text="Performing", command=ejecutar_tercer_script)
boton_otro_scripttres.pack(pady=10)



root.mainloop()
