# 📄 Archivo: src/andes_bank/generators/generar_prestamos.py
# Generador de datos sintéticos de préstamos

import random
import os
from . import config, utils

def generar_prestamos():
    utils.set_seed()
    clientes = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'clientes', 'clientes.csv'))
    ids_clientes = [int(c['id_cliente']) for c in clientes]

    prestamos = []
    id_prestamo_actual = 1

    for _ in range(config.NUM_PRESTAMOS):
        id_cliente = random.choice(ids_clientes)

        r = random.random()
        if r < 0.50:
            tipo = 'Personal'
            monto = round(random.uniform(50000, 2000000), 2)
            plazo_meses = random.randint(12, 60)
            tasa_interes = round(random.uniform(30, 60), 2)
        elif r < 0.60:
            tipo = 'Hipotecario'
            monto = round(random.uniform(2000000, 20000000), 2)
            plazo_meses = random.randint(60, 240)
            tasa_interes = round(random.uniform(20, 40), 2)
        elif r < 0.75:
            tipo = 'Prendario'
            monto = round(random.uniform(500000, 5000000), 2)
            plazo_meses = random.randint(24, 72)
            tasa_interes = round(random.uniform(25, 50), 2)
        elif r < 0.95:
            tipo = 'PyME'
            monto = round(random.uniform(500000, 10000000), 2)
            plazo_meses = random.randint(12, 60)
            tasa_interes = round(random.uniform(35, 55), 2)
        else:
            tipo = 'Microcrédito'
            monto = round(random.uniform(5000, 200000), 2)
            plazo_meses = random.randint(3, 12)
            tasa_interes = round(random.uniform(40, 80), 2)

        cuota = round(monto * (1 + tasa_interes/100 * plazo_meses/12) / plazo_meses, 2)
        fecha_desembolso = utils.random_date('2021-01-01', '2023-12-31')

        estado = 'Activo' if random.random() < 0.70 else ('Pagado' if random.random() < 0.67 else 'Moroso')
        if estado == 'Pagado':
            saldo_pendiente = 0.0
        elif estado == 'Moroso':
            saldo_pendiente = round(monto * random.uniform(0.3, 0.7), 2)
        else:
            saldo_pendiente = round(monto * random.uniform(0.4, 0.9), 2)

        if random.random() < 0.005:
            id_cliente = random.randint(100000, 999999)

        prestamo = {
            'id_prestamo': id_prestamo_actual,
            'id_cliente': id_cliente,
            'tipo': tipo,
            'monto': monto,
            'tasa_interes': tasa_interes,
            'plazo_meses': plazo_meses,
            'cuota': cuota,
            'fecha_desembolso': fecha_desembolso,
            'saldo_pendiente': saldo_pendiente,
            'estado': estado
        }
        prestamos.append(prestamo)
        id_prestamo_actual += 1

    fieldnames = ['id_prestamo', 'id_cliente', 'tipo', 'monto', 'tasa_interes', 'plazo_meses', 'cuota', 'fecha_desembolso', 'saldo_pendiente', 'estado']
    ruta = os.path.join(config.RAW_DIR, 'core_bancario', 'prestamos', 'prestamos.csv')
    utils.write_csv(ruta, fieldnames, prestamos)

if __name__ == '__main__':
    generar_prestamos()