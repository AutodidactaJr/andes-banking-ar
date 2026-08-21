# 📄 Archivo: src/andes_bank/generators/generar_agentes.py
# Generador de agentes de call center

import random
import os
from . import config, utils

def generar_agentes():
    utils.set_seed()
    sucursales = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'sucursales', 'sucursales.csv'))
    ids_sucursales = [int(s['id_sucursal']) for s in sucursales]
    nombres = ['Lucas', 'Martina', 'Santiago', 'Camila', 'Nicolás', 'Florencia', 'Agustín', 'Valentina', 'Julián', 'Candela']
    apellidos = ['Romero', 'Giménez', 'Sosa', 'Molina', 'Acosta', 'Herrera', 'Cabrera', 'Ríos', 'Peralta', 'Suárez']

    agentes = []
    for i in range(config.NUM_AGENTES):
        agentes.append({
            'id_agente': i + 1,
            'nombre': random.choice(nombres),
            'apellido': random.choice(apellidos),
            'id_sucursal': random.choice(ids_sucursales)
        })

    fieldnames = ['id_agente','nombre','apellido','id_sucursal']
    ruta = os.path.join(config.RAW_DIR, 'atencion_cliente', 'agentes', 'agentes.csv')
    utils.write_csv(ruta, fieldnames, agentes)

if __name__ == '__main__':
    generar_agentes()
