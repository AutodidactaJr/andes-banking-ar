# 📄 Archivo: src/andes_bank/generators/generar_cuentas.py
# Generador de datos sintéticos de cuentas bancarias

import random
import os
from . import config, utils

def generar_cuentas():
    utils.set_seed()

    # Leer clientes y sucursales desde las nuevas rutas
    clientes = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'clientes', 'clientes.csv'))
    sucursales = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'sucursales', 'sucursales.csv'))

    ids_clientes = [int(c['id_cliente']) for c in clientes]
    ids_sucursales = [int(s['id_sucursal']) for s in sucursales]

    cuentas = []
    id_cuenta_actual = 1

    for _ in range(config.NUM_CUENTAS):
        id_cliente = random.choice(ids_clientes)
        id_sucursal = random.choice(ids_sucursales)

        r = random.random()
        if r < 0.60:
            tipo_cuenta = 'Caja de Ahorro ARS'
            moneda = 'ARS'
            saldo = round(random.uniform(1000, 5000000), 2)
        elif r < 0.75:
            tipo_cuenta = 'Caja de Ahorro USD'
            moneda = 'USD'
            saldo = round(random.uniform(100, 100000), 2)
        else:
            tipo_cuenta = 'Cuenta Corriente'
            moneda = 'ARS'
            saldo = round(random.uniform(5000, 10000000), 2)

        fecha_apertura = utils.random_date('2015-01-01', '2023-12-31')
        estado = 'Activa' if random.random() < 0.95 else 'Inactiva'

        if random.random() < 0.01:
            saldo = -abs(saldo)
        if random.random() < 0.005:
            partes = fecha_apertura.split('-')
            fecha_apertura = f"{partes[2]}/{partes[1]}/{partes[0]}"
        if random.random() < 0.002:
            id_cliente = random.randint(100000, 999999)

        cuenta = {
            'id_cuenta': id_cuenta_actual,
            'id_cliente': id_cliente,
            'tipo_cuenta': tipo_cuenta,
            'moneda': moneda,
            'saldo': saldo,
            'fecha_apertura': fecha_apertura,
            'estado': estado,
            'id_sucursal': id_sucursal
        }
        cuentas.append(cuenta)
        id_cuenta_actual += 1

    fieldnames = ['id_cuenta', 'id_cliente', 'tipo_cuenta', 'moneda', 'saldo', 'fecha_apertura', 'estado', 'id_sucursal']
    ruta = os.path.join(config.RAW_DIR, 'core_bancario', 'cuentas', 'cuentas.csv')
    utils.write_csv(ruta, fieldnames, cuentas)

if __name__ == '__main__':
    generar_cuentas()