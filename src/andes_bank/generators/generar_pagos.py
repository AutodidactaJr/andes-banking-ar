# 📄 Archivo: src/andes_bank/generators/generar_pagos.py
# Generador de datos sintéticos de pagos

import random
import os
from . import config, utils

def generar_pagos():
    utils.set_seed()
    cuentas = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'cuentas', 'cuentas.csv'))
    ids_cuentas = [int(c['id_cuenta']) for c in cuentas]

    pagos = []
    id_pago_actual = 1

    tipos_pago = ['Servicio', 'Tarjeta de crédito', 'Cuota de préstamo']
    pesos = [0.5, 0.3, 0.2]
    entidades_servicio = ['Edesur', 'Metrogas', 'Aguas Argentinas', 'Telecom', 'Personal', 'Movistar', 'Claro', 'ABSA', 'Edenor', 'Naturgy']
    anios = [2023, 2022, 2021]
    pesos_anios = [0.5, 0.3, 0.2]

    for _ in range(config.NUM_PAGOS):
        id_cuenta = random.choice(ids_cuentas)
        tipo_pago = random.choices(tipos_pago, weights=pesos)[0]
        if tipo_pago == 'Servicio':
            entidad = random.choice(entidades_servicio)
        elif tipo_pago == 'Tarjeta de crédito':
            entidad = random.choice(['Visa', 'Mastercard', 'AndesCard'])
        else:
            entidad = 'Andes Bank Préstamo'

        monto = round(random.uniform(500, 50000), 2)
        anio = random.choices(anios, weights=pesos_anios)[0]
        fecha = utils.random_datetime(f"{anio}-01-01", f"{anio}-12-31")
        canal = random.choice(['Home Banking', 'Mobile Banking', 'Sucursal', 'Cajero Automático'])
        estado = 'Exitoso' if random.random() < 0.98 else 'Fallido'
        referencia = f"PAGO-{id_pago_actual:06d}"

        if random.random() < 0.01:
            monto = -abs(monto)
        if random.random() < 0.005:
            entidad = ''

        pago = {
            'id_pago': id_pago_actual,
            'id_cuenta': id_cuenta,
            'entidad': entidad,
            'tipo_pago': tipo_pago,
            'monto': monto,
            'fecha': fecha,
            'canal': canal,
            'estado': estado,
            'referencia': referencia
        }
        pagos.append(pago)
        id_pago_actual += 1

    fieldnames = ['id_pago', 'id_cuenta', 'entidad', 'tipo_pago', 'monto', 'fecha', 'canal', 'estado', 'referencia']
    ruta = os.path.join(config.RAW_DIR, 'core_bancario', 'pagos', 'pagos.csv')
    utils.write_csv(ruta, fieldnames, pagos)

if __name__ == '__main__':
    generar_pagos()