import requests
import subprocess

class Actualizador:
    @staticmethod
    def hay_actualizacion_disponible():
        url_actualizacion = "https://raw.githubusercontent.com/broly1987/meter/main/act.json"

        try:
            response = requests.get(url_actualizacion)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException as e:
            print("Error checking update:", str(e))

        return False

    @staticmethod
    def realizar_actualizacion():
        comando_establecer_rama = "git branch --set-upstream-to=origin/master master"
        comando_actualizacion = "git pull"

        try:
            subprocess.run(comando_establecer_rama, shell=True, check=True)
            subprocess.run(comando_actualizacion, shell=True, check=True)
            print("Update successful.")
        except subprocess.CalledProcessError as e:
            print("Error updating:", str(e))

# Llamar a los métodos de la clase Actualizador
if Actualizador.hay_actualizacion_disponible():
    respuesta = input("Hay una actualización disponible. ¿Deseas actualizar? (s/n): ")
    if respuesta.lower() == "s":
        Actualizador.realizar_actualizacion()
    else:
        print("Actualización cancelada.")
