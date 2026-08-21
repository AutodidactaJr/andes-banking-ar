# 📄 Archivo: src/andes_bank/generators/generar_oportunidades.py
# Generador de oportunidades de venta (pipeline CRM)

import random
import os
from . import config, utils

def generar_oportunidades():
    utils.set_seed()
    clientes = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'clientes', 'clientes.csv'))
    ids_clientes = [int(c['id_cliente']) for c in clientes]

    productos = ['Caja de Ahorro', 'Tarjeta de Crédito', 'Préstamo Personal', 'Plazo Fijo', 'Seguro de Vida']
    estados = ['Abierta', 'En negociación', 'Ganada', 'Perdida']

    oportunidades = []
    for i in range(config.NUM_OPORTUNIDADES):
        oportunidades.append({
            'id_oportunidad': i + 1,
            'id_cliente': random.choice(ids_clientes),
            'producto_interes': random.choice(productos),
            'fecha_creacion': utils.random_date('2022-01-01', '2023-12-31'),
            'estado': random.choices(estados, weights=[0.3, 0.2, 0.4, 0.1])[0]
        })

    fieldnames = ['id_oportunidad','id_cliente','producto_interes','fecha_creacion','estado']
    ruta = os.path.join(config.RAW_DIR, 'crm', 'oportunidades', 'oportunidades.csv')
    utils.write_csv(ruta, fieldnames, oportunidades)

if __name__ == '__main__':
    generar_oportunidades()