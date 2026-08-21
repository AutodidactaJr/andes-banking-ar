# 📄 Archivo: src/andes_bank/generators/generar_seguros.py
# Generador de pólizas de seguros

import random
import os
from . import config, utils

def generar_seguros():
    utils.set_seed()
    clientes = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'clientes', 'clientes.csv'))
    ids_clientes = [int(c['id_cliente']) for c in clientes]
    seguros = []
    id_seguro = 1

    tipos = ['Vida', 'Robo', 'Retiro', 'Hogar', 'Auto']
    for _ in range(config.NUM_SEGUROS):
        id_cliente = random.choice(ids_clientes)
        tipo_seguro = random.choice(tipos)
        prima = round(random.uniform(500, 50000), 2)
        fecha_contratacion = utils.random_date('2021-01-01', '2023-12-31')
        estado = random.choice(['Activo', 'Cancelado'])
        seguros.append({
            'id_seguro': id_seguro,
            'id_cliente': id_cliente,
            'tipo_seguro': tipo_seguro,
            'prima_mensual': prima,
            'fecha_contratacion': fecha_contratacion,
            'estado': estado
        })
        id_seguro += 1

    fieldnames = ['id_seguro','id_cliente','tipo_seguro','prima_mensual','fecha_contratacion','estado']
    ruta = os.path.join(config.RAW_DIR, 'core_bancario', 'seguros', 'seguros.csv')
    utils.write_csv(ruta, fieldnames, seguros)

if __name__ == '__main__':
    generar_seguros()