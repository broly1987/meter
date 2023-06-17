import requests
import subprocess

# Función para verificar si hay una actualización disponible
def hay_actualizacion_disponible():
    # URL del servidor de actualizaciones
    url_actualizacion = "https://raw.githubusercontent.com/broly1987/meter/main/act.json?token=GHSAT0AAAAAACDUTGCETFSUH2GMY6JRNG2SZENJ4KA"

    try:
        response = requests.get(url_actualizacion)
        # Verificar el código de respuesta HTTP
        if response.status_code == 200:
            # Si la respuesta es exitosa, se considera que hay una actualización disponible
            return True
    except requests.exceptions.RequestException as e:
        # Manejar errores de conexión
        print("Error al verificar la actualización:", str(e))

    # Si ocurre algún error o la respuesta no es exitosa, se considera que no hay una actualización disponible
    return False





# Función para realizar la actualización
import subprocess


# Función para realizar la actualización
def realizar_actualizacion():
    # Comandos para establecer la rama de seguimiento y realizar la actualización
    comando_establecer_rama = "git branch --set-upstream-to=origin/master master"
    comando_actualizacion = "git pull"

    try:
        # Establecer la rama de seguimiento
        subprocess.run(comando_establecer_rama, shell=True, check=True)

        # Ejecutar el comando de actualización
        subprocess.run(comando_actualizacion, shell=True, check=True)

        # Puedes agregar aquí cualquier otra acción necesaria para completar la actualización

        print("Actualización realizada exitosamente.")
    except subprocess.CalledProcessError as e:
        # Manejar errores en la ejecución de los comandos
        print("Error al realizar la actualización:", str(e))
