# 📄 Archivo: src/andes_bank/generators/generar_transacciones.py
# Generador de datos sintéticos de transacciones

import random
import os
from . import config, utils

def generar_transacciones():
    utils.set_seed()
    cuentas = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'cuentas', 'cuentas.csv'))
    ids_cuentas = [int(c['id_cuenta']) for c in cuentas]

    transacciones = []
    id_transaccion_actual = 1

    tipos = ['Depósito', 'Retiro', 'Transferencia enviada', 'Transferencia recibida', 'Consumo débito', 'Pago de tarjeta', 'Cobro de préstamo']
    pesos = [0.20, 0.15, 0.15, 0.15, 0.25, 0.05, 0.05]
    canales = config.CANALES
    anios = [2023, 2022, 2021]
    pesos_anios = [0.5, 0.3, 0.2]

    for _ in range(config.NUM_TRANSACCIONES):
        id_cuenta = random.choice(ids_cuentas)
        tipo = random.choices(tipos, weights=pesos)[0]
        signo = 1 if tipo in ['Depósito', 'Transferencia recibida', 'Cobro de préstamo'] else -1

        if tipo == 'Retiro':
            monto = random.uniform(500, 50000)
        elif tipo == 'Consumo débito':
            monto = random.uniform(100, 50000)
        elif tipo in ['Transferencia enviada', 'Transferencia recibida']:
            monto = random.uniform(1000, 500000)
        elif tipo == 'Depósito':
            monto = random.uniform(1000, 200000)
        elif tipo == 'Pago de tarjeta':
            monto = random.uniform(1000, 100000)
        else:
            monto = random.uniform(500, 20000)

        monto = round(monto * signo, 2)
        anio = random.choices(anios, weights=pesos_anios)[0]
        fecha = utils.random_datetime(f"{anio}-01-01", f"{anio}-12-31")
        canal = random.choice(canales)
        estado = 'Completada' if random.random() < 0.97 else 'Rechazada'
        referencia = f"TRX-{id_transaccion_actual:06d}"

        if random.random() < 0.01:
            monto = 0.0
        if random.random() < 0.005:
            fecha = f"{anio}-02-30 10:00:00"
        if random.random() < 0.002:
            id_cuenta = random.randint(100000, 999999)

        transaccion = {
            'id_transaccion': id_transaccion_actual,
            'id_cuenta': id_cuenta,
            'tipo_transaccion': tipo,
            'monto': monto,
            'moneda': 'ARS',
            'fecha': fecha,
            'canal': canal,
            'estado': estado,
            'referencia': referencia
        }
        transacciones.append(transaccion)
        id_transaccion_actual += 1

    fieldnames = ['id_transaccion', 'id_cuenta', 'tipo_transaccion', 'monto', 'moneda', 'fecha', 'canal', 'estado', 'referencia']
    ruta = os.path.join(config.RAW_DIR, 'core_bancario', 'transacciones', 'transacciones.csv')
    utils.write_csv(ruta, fieldnames, transacciones)

if __name__ == '__main__':
    generar_transacciones()