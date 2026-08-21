# 📄 Archivo: src/andes_bank/generators/generar_sucursales.py
# Generador de datos sintéticos de sucursales

import random
import os
from . import config, utils

def generar_sucursales():
    utils.set_seed()
    sucursales = []

    casa_central = {
        'id_sucursal': 1,
        'nombre': 'Casa Central',
        'direccion': 'Av. San Martín 100',
        'ciudad': 'Mendoza',
        'provincia': 'Mendoza',
        'region': 'Cuyo',
        'fecha_apertura': '1995-04-01'
    }
    sucursales.append(casa_central)

    for id_sucursal in range(2, config.NUM_SUCURSALES + 1):
        provincia = random.choice(list(config.PROVINCIAS.keys()))
        ciudad = random.choice(config.PROVINCIAS[provincia])
        if provincia in ['Mendoza', 'San Juan', 'San Luis']:
            region = 'Cuyo'
        elif provincia in ['Córdoba', 'Santa Fe']:
            region = 'Centro'
        elif provincia in ['Tucumán', 'Salta', 'Jujuy']:
            region = 'Norte'
        elif provincia in ['Entre Ríos', 'Corrientes']:
            region = 'Litoral'
        elif provincia in ['Neuquén', 'Río Negro']:
            region = 'Patagonia'
        else:
            region = 'Otra'

        fecha_apertura = utils.random_date('1996-01-01', '2023-01-01')
        sucursal = {
            'id_sucursal': id_sucursal,
            'nombre': f'Sucursal {ciudad}',
            'direccion': f'Calle {random.randint(1,2000)} N°{random.randint(100,999)}',
            'ciudad': ciudad,
            'provincia': provincia,
            'region': region,
            'fecha_apertura': fecha_apertura
        }
        sucursales.append(sucursal)

    fieldnames = ['id_sucursal', 'nombre', 'direccion', 'ciudad', 'provincia', 'region', 'fecha_apertura']
    ruta = os.path.join(config.RAW_DIR, 'core_bancario', 'sucursales', 'sucursales.csv')
    utils.write_csv(ruta, fieldnames, sucursales)

if __name__ == '__main__':
    generar_sucursales()