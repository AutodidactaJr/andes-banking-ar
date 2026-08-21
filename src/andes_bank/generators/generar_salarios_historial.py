# 📄 Archivo: src/andes_bank/generators/generar_salarios_historial.py
# Generador de historial salarial

import random
import os
from datetime import datetime, timedelta
from . import config, utils

def generar_salarios_historial():
    utils.set_seed()
    ruta_empleados = os.path.join(config.RAW_DIR, 'rrhh', 'empleados', 'empleados.csv')
    empleados = utils.read_csv(ruta_empleados)
    ids_empleados = [int(e['id_empleado']) for e in empleados]

    salarios = []
    id_salario = 1

    for _ in range(config.NUM_SALARIOS_HISTORIAL):
        id_empleado = random.choice(ids_empleados)
        salario = round(random.uniform(50000, 200000), 2)
        fecha_inicio = utils.random_date('2021-01-01', '2024-12-31')
        # Algunos registros actuales sin fecha_fin
        if random.random() < 0.5:
            fecha_fin = ''
        else:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = (fecha_inicio_dt + timedelta(days=random.randint(365, 1095))).strftime('%Y-%m-%d')

        salarios.append({
            'id_salario': id_salario,
            'id_empleado': id_empleado,
            'salario': salario,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin
        })
        id_salario += 1

    fieldnames = ['id_salario', 'id_empleado', 'salario', 'fecha_inicio', 'fecha_fin']
    ruta = os.path.join(config.RAW_DIR, 'rrhh', 'salarios_historial', 'salarios_historial.csv')
    utils.write_csv(ruta, fieldnames, salarios)

if __name__ == '__main__':
    generar_salarios_historial()