# 📄 Archivo: src/andes_bank/generators/generar_contabilidad.py
# Generador de datos para Contabilidad

import random, os
from . import config, utils

def generar_contabilidad():
    utils.set_seed()

    cuentas = [
        ('1000', 'Caja', 'Activo'), ('2000', 'Bancos', 'Activo'),
        ('3000', 'Cuentas por cobrar', 'Activo'), ('4000', 'Cuentas por pagar', 'Pasivo'),
        ('5000', 'Capital', 'Patrimonio'), ('6000', 'Ingresos', 'Ingreso'),
        ('7000', 'Gastos', 'Gasto')
    ]
    cuentas_contables = []
    for i, (cod, desc, tipo) in enumerate(cuentas):
        cuentas_contables.append({
            'id_cuenta_contable': i+1,
            'codigo_cuenta': cod,
            'descripcion': desc,
            'tipo_cuenta': tipo
        })

    asientos = []
    for i in range(config.NUM_ASIENTOS):
        id_cuenta = random.randint(1, len(cuentas_contables))
        asientos.append({
            'id_asiento': i+1,
            'id_cuenta_contable': id_cuenta,
            'fecha_contable': utils.random_date('2022-01-01', '2023-12-31'),
            'tipo_asiento': random.choice(['Debe', 'Haber']),
            'monto_debe': round(random.uniform(1000, 500000), 2),
            'monto_haber': round(random.uniform(1000, 500000), 2),
            'descripcion': f'Asiento {i+1}'
        })

    presupuestos = []
    for i in range(config.NUM_PRESUPUESTO):
        presupuestos.append({
            'id_presupuesto': i+1,
            'id_cuenta_contable': random.randint(1, len(cuentas_contables)),
            'monto_presupuestado': round(random.uniform(50000, 1000000), 2),
            'fecha_presupuesto': utils.random_date('2022-01-01', '2023-12-31')
        })

    # Guardar en subcarpetas
    utils.write_csv(os.path.join(config.RAW_DIR, 'contabilidad', 'cuentas_contables', 'cuentas_contables.csv'),
                    ['id_cuenta_contable','codigo_cuenta','descripcion','tipo_cuenta'], cuentas_contables)
    utils.write_csv(os.path.join(config.RAW_DIR, 'contabilidad', 'asientos_contables', 'asientos_contables.csv'),
                    ['id_asiento','id_cuenta_contable','fecha_contable','tipo_asiento','monto_debe','monto_haber','descripcion'], asientos)
    utils.write_csv(os.path.join(config.RAW_DIR, 'contabilidad', 'presupuesto', 'presupuesto.csv'),
                    ['id_presupuesto','id_cuenta_contable','monto_presupuestado','fecha_presupuesto'], presupuestos)

if __name__ == '__main__':
    generar_contabilidad()