# 📄 Archivo: src/andes_bank/generators/generar_leads.py
# Generador de leads (clientes potenciales)

import random
import os
from . import config, utils

def generar_leads():
    utils.set_seed()

    clientes = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'clientes', 'clientes.csv'))
    ids_clientes = [int(c['id_cliente']) for c in clientes]

    leads = []
    id_lead = 1

    for _ in range(config.NUM_LEADS):
        id_campana = random.randint(1, config.NUM_CAMPANAS)
        id_cliente = None
        if random.random() < 0.7:
            id_cliente = random.choice(ids_clientes)

        fecha_creacion = utils.random_date('2022-01-01', '2023-12-31')
        estado = random.choices(config.ESTADOS_LEAD, weights=[0.4, 0.3, 0.2, 0.1])[0]
        producto_interes = random.choice(config.PRODUCTOS_INTERES)

        lead = {
            'id_lead': id_lead,
            'id_campana': id_campana,
            'id_cliente': id_cliente if id_cliente else '',
            'fecha_creacion': fecha_creacion,
            'estado': estado,
            'producto_interes': producto_interes
        }
        leads.append(lead)
        id_lead += 1

    fieldnames = ['id_lead', 'id_campana', 'id_cliente', 'fecha_creacion', 'estado', 'producto_interes']
    ruta = os.path.join(config.RAW_DIR, 'crm', 'leads', 'leads.csv')
    utils.write_csv(ruta, fieldnames, leads)

if __name__ == '__main__':
    generar_leads()