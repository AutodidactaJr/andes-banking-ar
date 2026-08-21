# 📄 Archivo: src/andes_bank/generators/generar_plazos_fijos.py
# Generador de plazos fijos

import random
import os
import datetime
from . import config, utils

def generar_plazos_fijos():
    utils.set_seed()
    clientes = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'clientes', 'clientes.csv'))
    ids_clientes = [int(c['id_cliente']) for c in clientes]
    plazos = []
    id_plazo = 1

    for _ in range(config.NUM_PLAZOS_FIJOS):
        id_cliente = random.choice(ids_clientes)
        monto = round(random.uniform(10000, 5000000), 2)
        tasa = round(random.uniform(20, 45), 2)
        fecha_constitucion = utils.random_date('2021-01-01', '2023-12-31')
        fecha = datetime.datetime.strptime(fecha_constitucion, '%Y-%m-%d')
        dias = random.choice([30, 60, 90, 180, 365])
        fecha_vencimiento = fecha + datetime.timedelta(days=dias)
        estado = random.choice(['Vigente', 'Cobrado'])
        plazos.append({
            'id_plazo_fijo': id_plazo,
            'id_cliente': id_cliente,
            'monto': monto,
            'tasa_interes': tasa,
            'fecha_constitucion': fecha_constitucion,
            'fecha_vencimiento': fecha_vencimiento.strftime('%Y-%m-%d'),
            'estado': estado
        })
        id_plazo += 1

    fieldnames = ['id_plazo_fijo','id_cliente','monto','tasa_interes','fecha_constitucion','fecha_vencimiento','estado']
    ruta = os.path.join(config.RAW_DIR, 'core_bancario', 'plazos_fijos', 'plazos_fijos.csv')
    utils.write_csv(ruta, fieldnames, plazos)

if __name__ == '__main__':
    generar_plazos_fijos()