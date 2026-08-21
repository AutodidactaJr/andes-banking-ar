# 📄 Archivo: src/andes_bank/generators/generar_evaluaciones.py
# Generador de evaluaciones de desempeño

import random
import os
from . import config, utils

def generar_evaluaciones():
    utils.set_seed()
    ruta_empleados = os.path.join(config.RAW_DIR, 'rrhh', 'empleados', 'empleados.csv')
    empleados = utils.read_csv(ruta_empleados)
    ids_empleados = [int(e['id_empleado']) for e in empleados]

    evaluaciones = []
    id_evaluacion = 1

    for _ in range(config.NUM_EVALUACIONES):
        id_empleado = random.choice(ids_empleados)
        anio = random.randint(2021, 2023)
        puntaje = random.randint(1, 100)
        comentario = random.choice(['Excelente', 'Bueno', 'Regular', 'Necesita mejorar'])
        evaluaciones.append({
            'id_evaluacion': id_evaluacion,
            'id_empleado': id_empleado,
            'anio': anio,
            'puntaje': puntaje,
            'comentario': comentario
        })
        id_evaluacion += 1

    fieldnames = ['id_evaluacion', 'id_empleado', 'anio', 'puntaje', 'comentario']
    ruta = os.path.join(config.RAW_DIR, 'rrhh', 'evaluaciones', 'evaluaciones.csv')
    utils.write_csv(ruta, fieldnames, evaluaciones)

if __name__ == '__main__':
    generar_evaluaciones()