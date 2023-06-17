import requests
import pystray
import subprocess

from PIL import Image

# Función para verificar si hay una actualización disponible
import requests


def hay_actualizacion_disponible():
    url_actualizacion = "https://raw.githubusercontent.com/broly1987/meter/main/act.json?token=GHSAT0AAAAAACDUTGCETFSUH2GMY6JRNG2SZENJ4KA"

    try:
        response = requests.get(url_actualizacion)
        if response.status_code == 200:
            data = response.json()
            # Aquí puedes procesar la información del archivo JSON
            version_actual = "1.0.0"  # Versión actual de tu aplicación
            version_disponible = data["version"]  # Versión disponible en el archivo JSON

            if version_disponible > version_actual:
                # Hay una actualización disponible
                return True
    except requests.exceptions.RequestException as e:
        print("Error al verificar la actualización:", str(e))

    return False


# Función para mostrar la notificación de actualización
def mostrar_notificacion():
    icono = Image.open("image.jpg")  # Reemplaza "icono.png" con la ruta de tu propio ícono
    menu = (
        pystray.MenuItem("Actualizar", lambda: subprocess.run(["python", "actualizar.py"])),
        pystray.MenuItem("Salir", lambda: pystray.quit()),
    )
    icono_notificacion = pystray.Icon("meter_roll_over", icono, "new update avaliable", menu)
    icono_notificacion.run()

# Verificar si hay una actualización disponible
if hay_actualizacion_disponible():
    # Mostrar la notificación de actualización
    mostrar_notificacion()