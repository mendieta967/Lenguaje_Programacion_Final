import os
import json


def inicializar_sistema():

    ruta_data = "data"
    if not os.path.exists(ruta_data):
        os.mkdir(ruta_data)

        if not os.path.exists(ruta_data):
            os.mkdir(ruta_data)