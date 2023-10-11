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
    def realizar_actualizacion(con_barra=False, barra=None):
        comando_actualizacion = "git pull"

        try:
            if con_barra and barra:
                barra.UpdateBar(50)
            subprocess.run(comando_actualizacion, shell=True, check=True)

            if con_barra and barra:
                barra.UpdateBar(100)
            print("Update successful.")
        except subprocess.CalledProcessError as e:
            print("Error updating:", str(e))