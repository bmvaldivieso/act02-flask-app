from flask import Flask
from datetime import datetime  
import requests

app = Flask(__name__)

URL_DATOS = "https://gist.githubusercontent.com/reroes/502d11c95f1f8a17d300ece914464c57/raw/872172ebb60e22e95baf8f50e2472551f49311ff/gistfile1.txt"

@app.route("/")
def home():
    encabezado, personas = obtener_datos_filtrados()

    tabla_html = """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <div class="container mt-4">
        <h1>¡Hola, mundo loja!</h1>
        <p><b>Fecha y hora actual:</b> """ + datetime.now().strftime("%d, %B, %Y, %H:%M:%S") + """</p>
        <h2>Personas con ID iniciando en 3, 4, 5 o 7</h2>
        <table class="table table-bordered">
            <thead>
                <tr>
                    """ + "".join([f"<th>{col}</th>" for col in encabezado]) + """
                </tr>
            </thead>
            <tbody>
    """
    
    for persona in personas:
        tabla_html += "<tr>" + "".join([f"<td>{dato}</td>" for dato in persona]) + "</tr>"

    tabla_html += """
            </tbody>
        </table>
    </div>
    """
    
    return tabla_html

def obtener_contenido(url):
    response = requests.get(url)
    return response.text if response.status_code == 200 else ""

def obtener_datos_filtrados():
    contenido = obtener_contenido(URL_DATOS)
    lineas = contenido.strip().split("\n")

    encabezado = lineas[0].split("|")
    datos = lineas[1:]

    # Filtro de IDs
    ids_validos = ("3", "4", "5", "7")
    # Empezamos con la lista (datos), que es una lista de cadenas de texto que no contiene el encabezado.
    # for linea in datos: esta parte recorre todas las líneas de datos. 
    # linea.split("|"): esto lo que hace es separar el texto en partes usando como delimitador (|). Esto convierte la línea en una lista de la siguiente forma: ['3', 'Carlos', 'M', 'Loja']
    # linea.split("|")[0]: ahora, esto en cambio hace que de la nueva lista se tome solo el primer elemento (ID).
    # .startswith(ids_validos): por otro lado, esto verifica si la cadena empieza con uno de los valores dados (ids_validos es una tupla que tiene los valores: ("3", "4", "5", "7")).
    # Lo anterior va a devolver True si el ID comienza con 3, 4, 5 o 7, y False si no.
    # if linea.split("|")[0].startswith(ids_validos): el if que tenemos al inicio de esta parte filtra solo las líneas que cumplen la condición.
    # Al final, todas las listas filtradas que pasaron el filtro se almacenan en personas_filtradas.
    personas_filtradas = [linea.split("|") for linea in datos if linea.split("|")[0].startswith(ids_validos)]

    return encabezado, personas_filtradas

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
