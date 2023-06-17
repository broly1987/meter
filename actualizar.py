import requests
import pystray
from PIL import Image

# Función para verificar si hay una actualización disponible
def hay_actualizacion_disponible():
    # URL del servidor de actualizaciones
    url_actualizacion = "https://github.com/broly1987/meter.git"

    try:
        response = requests.get(url_actualizacion)
        # Verificar el código de respuesta HTTP
        if response.status_code == 200:
            # Si la respuesta es exitosa, se considera que hay una actualización disponible
            return True
    except requests.exceptions.RequestException as e:
        # Manejar errores de conexión
        print("error fetching data:", str(e))

    # Si ocurre algún error o la respuesta no es exitosa, se considera que no hay una actualización disponible
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