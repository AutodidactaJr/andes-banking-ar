# 📄 Archivo: src/andes_bank/generators/generar_rrhh.py
# Generador de datos para RRHH

import random, os
from datetime import datetime, timedelta
from . import config, utils

def generar_rrhh():
    utils.set_seed()
    sucursales = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'sucursales', 'sucursales.csv'))
    ids_sucursales = [int(s['id_sucursal']) for s in sucursales]
    nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Sofía', 'Pedro', 'Lucía']
    apellidos = ['García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez']
    cargos = ['Cajero', 'Oficial de negocios', 'Gerente', 'Back office']

    empleados = []
    for i in range(config.NUM_EMPLEADOS):
        empleados.append({
            'id_empleado': i+1,
            'nombre': random.choice(nombres),
            'apellido': random.choice(apellidos),
            'cargo': random.choice(cargos),
            'id_sucursal': random.choice(ids_sucursales),
            'fecha_contratacion': utils.random_date('2015-01-01', '2023-01-01'),
            'salario': round(random.uniform(50000, 200000), 2)
        })

    ausencias = []
    for i in range(config.NUM_AUSENCIAS):
        fecha_inicio = utils.random_date('2022-01-01', '2023-12-31')
        dias = random.randint(1, 15)
        fin = datetime.strptime(fecha_inicio, '%Y-%m-%d') + timedelta(days=dias)
        ausencias.append({
            'id_ausencia': i+1,
            'id_empleado': random.randint(1, config.NUM_EMPLEADOS),
            'tipo_ausencia': random.choice(['Enfermedad', 'Vacaciones', 'Permiso', 'Otro']),
            'dias': dias,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fin.strftime('%Y-%m-%d')
        })

    # Guardar en subcarpetas
    utils.write_csv(os.path.join(config.RAW_DIR, 'rrhh', 'empleados', 'empleados.csv'),
                    ['id_empleado','nombre','apellido','cargo','id_sucursal','fecha_contratacion','salario'], empleados)
    utils.write_csv(os.path.join(config.RAW_DIR, 'rrhh', 'ausencias', 'ausencias.csv'),
                    ['id_ausencia','id_empleado','tipo_ausencia','dias','fecha_inicio','fecha_fin'], ausencias)

if __name__ == '__main__':
    generar_rrhh()