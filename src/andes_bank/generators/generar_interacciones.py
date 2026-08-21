# 📄 Archivo: src/andes_bank/generators/generar_interacciones.py
# Generador de interacciones de clientes con campañas

import random
import os
from . import config, utils

def generar_interacciones():
    utils.set_seed()

    clientes = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'clientes', 'clientes.csv'))
    ids_clientes = [int(c['id_cliente']) for c in clientes]

    interacciones = []
    id_interaccion = 1

    for _ in range(config.NUM_INTERACCIONES):
        id_campana = random.randint(1, config.NUM_CAMPANAS)
        id_cliente = random.choice(ids_clientes)
        fecha = utils.random_datetime('2022-01-01', '2023-12-31')
        tipo = random.choices(config.TIPOS_INTERACCION, weights=[0.5, 0.3, 0.15, 0.05])[0]
        dispositivo = random.choice(config.DISPOSITIVOS)

        if random.random() < 0.005:
            id_cliente = random.randint(100000, 999999)

        interaccion = {
            'id_interaccion': id_interaccion,
            'id_campana': id_campana,
            'id_cliente': id_cliente,
            'fecha': fecha,
            'tipo_interaccion': tipo,
            'dispositivo': dispositivo
        }
        interacciones.append(interaccion)
        id_interaccion += 1

    fieldnames = ['id_interaccion', 'id_campana', 'id_cliente', 'fecha', 'tipo_interaccion', 'dispositivo']
    ruta = os.path.join(config.RAW_DIR, 'crm', 'interacciones', 'interacciones.csv')
    utils.write_csv(ruta, fieldnames, interacciones)

if __name__ == '__main__':
    generar_interacciones()