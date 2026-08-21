# 📄 Archivo: src/andes_bank/generators/generar_campanas.py
# Generador de campañas de marketing

import random
import os
from . import config, utils

def generar_campanas():
    utils.set_seed()
    campanas = []
    nombres = [
        "Promoción Cuenta Premium", "Descuento Préstamo Personal", "Invitación Plazo Fijo UVA",
        "Bienvenida Joven", "Campaña Tarjeta de Crédito", "Seguro de Vida Familiar",
        "Vacaciones sin intereses", "CyberMonday Andes", "Semana del Cliente", "Préstamo PyME"
    ]

    for i in range(config.NUM_CAMPANAS):
        id_campana = i + 1
        nombre = random.choice(nombres) + f" {id_campana}"
        canal = random.choice(config.CANALES_CAMPANA)
        segmento = random.choice(config.SEGMENTOS_OBJETIVO)
        fecha_inicio = utils.random_date('2022-01-01', '2023-06-30')
        fecha_fin = utils.random_date(fecha_inicio, '2023-12-31')
        costo = round(random.uniform(10000, 500000), 2)

        campana = {
            'id_campana': id_campana,
            'nombre': nombre,
            'canal': canal,
            'segmento_objetivo': segmento,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'costo': costo
        }
        campanas.append(campana)

    fieldnames = ['id_campana', 'nombre', 'canal', 'segmento_objetivo', 'fecha_inicio', 'fecha_fin', 'costo']
    ruta = os.path.join(config.RAW_DIR, 'crm', 'campanas', 'campanas.csv')
    utils.write_csv(ruta, fieldnames, campanas)

if __name__ == '__main__':
    generar_campanas()