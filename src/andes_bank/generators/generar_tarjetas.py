# 📄 Archivo: src/andes_bank/generators/generar_tarjetas.py
# Generador de datos sintéticos de tarjetas

import random
import os
from . import config, utils

def generar_tarjetas():
    utils.set_seed()

    clientes = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'clientes', 'clientes.csv'))
    cuentas = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'cuentas', 'cuentas.csv'))

    cuentas_por_cliente = {}
    for cuenta in cuentas:
        id_cliente = int(cuenta['id_cliente'])
        tipo = cuenta['tipo_cuenta']
        if tipo == 'Caja de Ahorro ARS':
            cuentas_por_cliente.setdefault(id_cliente, []).append(int(cuenta['id_cuenta']))

    ids_clientes = [int(c['id_cliente']) for c in clientes]
    tarjetas = []
    id_tarjeta_actual = 1
    numeros_usados = set()

    for _ in range(config.NUM_TARJETAS):
        id_cliente = random.choice(ids_clientes)
        tipo = 'Débito' if random.random() < 0.60 else 'Crédito'
        if tipo == 'Débito':
            marca = random.choices(['Visa', 'Mastercard', 'AndesCard'], weights=[0.5, 0.3, 0.2])[0]
        else:
            marca = random.choices(['Visa', 'Mastercard'], weights=[0.6, 0.4])[0]

        id_cuenta = None
        if tipo == 'Débito' and cuentas_por_cliente.get(id_cliente):
            id_cuenta = random.choice(cuentas_por_cliente[id_cliente])
        elif tipo == 'Crédito' and random.random() < 0.5 and cuentas_por_cliente.get(id_cliente):
            id_cuenta = random.choice(cuentas_por_cliente[id_cliente])

        numero = f"{random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"
        if random.random() < 0.01 and numeros_usados:
            numero = random.choice(list(numeros_usados))
        numeros_usados.add(numero)

        fecha_emision = utils.random_date('2018-01-01', '2023-12-31')
        anio_vencimiento = random.randint(2024, 2028)
        mes_vencimiento = random.randint(1, 12)
        fecha_vencimiento = f"{anio_vencimiento}-{mes_vencimiento:02d}-01"
        if random.random() < 0.005:
            fecha_vencimiento = f"2023-{mes_vencimiento:02d}-01"

        limite = round(random.uniform(50000, 1000000), 2) if tipo == 'Crédito' else 0.0
        estado = 'Activa' if random.random() < 0.95 else 'Bloqueada'

        tarjeta = {
            'id_tarjeta': id_tarjeta_actual,
            'id_cliente': id_cliente,
            'id_cuenta': id_cuenta if id_cuenta else '',
            'marca': marca,
            'tipo': tipo,
            'numero': numero,
            'limite': limite,
            'fecha_emision': fecha_emision,
            'fecha_vencimiento': fecha_vencimiento,
            'estado': estado
        }
        tarjetas.append(tarjeta)
        id_tarjeta_actual += 1

    fieldnames = ['id_tarjeta', 'id_cliente', 'id_cuenta', 'marca', 'tipo', 'numero', 'limite', 'fecha_emision', 'fecha_vencimiento', 'estado']
    ruta = os.path.join(config.RAW_DIR, 'core_bancario', 'tarjetas', 'tarjetas.csv')
    utils.write_csv(ruta, fieldnames, tarjetas)

if __name__ == '__main__':
    generar_tarjetas()