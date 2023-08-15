import requests
import json

# URL del archivo JSON
url = 'https://raw.githubusercontent.com/broly1987/meter/main/act.json?token=GHSAT0AAAAAACDUTGCFMCWBO4LIIH2BHTQSZEON2UQ'

# Realizar la solicitud HTTP
response = requests.get(url)

# Verificar el estado de la respuesta
if response.status_code == 200:
    # Cargar el contenido JSON
    contenido = json.loads(response.text)

    # Mostrar el contenido del archivo
    print(contenido)
else:
    print('Error al obtener el archivo JSON:', response.status_code)
