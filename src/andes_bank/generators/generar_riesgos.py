# 📄 Archivo: src/andes_bank/generators/generar_riesgos.py
# Generador de datos para el área de Riesgos

import random
import os
from . import config, utils

def generar_riesgos():
    utils.set_seed()

    clientes = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'clientes', 'clientes.csv'))
    ids_clientes = [int(c['id_cliente']) for c in clientes]
    cuentas = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'cuentas', 'cuentas.csv'))
    ids_cuentas = [int(c['id_cuenta']) for c in cuentas]

    # 1. Scoring crediticio (70% de clientes)
    scorings = []
    for i, id_cliente in enumerate(ids_clientes[:int(len(ids_clientes)*0.7)]):
        score = random.randint(300, 850)
        riesgo = 'Bajo' if score >= 750 else ('Medio' if score >= 600 else 'Alto')
        scorings.append({
            'id_scoring': i+1,
            'id_cliente': id_cliente,
            'score': score,
            'riesgo': riesgo,
            'fecha_calculo': utils.random_date('2022-01-01', '2023-12-31')
        })

    # 2. Alertas de fraude
    alertas = []
    for i in range(config.NUM_ALERTAS_FRAUDE):
        alertas.append({
            'id_alerta': i+1,
            'id_cliente': random.choice(ids_clientes),
            'id_cuenta': random.choice(ids_cuentas),
            'tipo_alerta': random.choice(['Movimiento inusual', 'Login sospechoso', 'Cambio de datos', 'Phishing']),
            'monto': round(random.uniform(1000, 500000), 2),
            'estado': random.choice(['Pendiente', 'Investigada', 'Resuelta', 'Falsa']),
            'fecha_deteccion': utils.random_datetime('2022-01-01', '2023-12-31')
        })

    # 3. Incidentes
    incidentes = []
    for i in range(config.NUM_INCIDENTES):
        incidentes.append({
            'id_incidente': i+1,
            'id_cliente': random.choice(ids_clientes),
            'descripcion': random.choice(['Fraude confirmado', 'Error de sistema', 'Fuga de datos', 'Acceso no autorizado']),
            'severidad': random.choice(['Baja', 'Media', 'Alta', 'Crítica']),
            'estado': random.choice(['Abierto', 'Cerrado', 'En investigación']),
            'fecha_incidente': utils.random_datetime('2022-01-01', '2023-12-31')
        })

    # 4. Morosidad
    morosidades = []
    for i in range(config.NUM_MOROSIDAD):
        morosidades.append({
            'id_morosidad': i+1,
            'id_cliente': random.choice(ids_clientes),
            'dias_mora': random.randint(1, 360),
            'deuda_pendiente': round(random.uniform(5000, 500000), 2),
            'fecha_reporte': utils.random_date('2022-01-01', '2023-12-31')
        })

    # Guardar en subcarpetas
    utils.write_csv(os.path.join(config.RAW_DIR, 'riesgos', 'scoring_crediticio', 'scoring_crediticio.csv'),
                    ['id_scoring','id_cliente','score','riesgo','fecha_calculo'], scorings)
    utils.write_csv(os.path.join(config.RAW_DIR, 'riesgos', 'alertas_fraude', 'alertas_fraude.csv'),
                    ['id_alerta','id_cliente','id_cuenta','tipo_alerta','monto','estado','fecha_deteccion'], alertas)
    utils.write_csv(os.path.join(config.RAW_DIR, 'riesgos', 'incidentes', 'incidentes.csv'),
                    ['id_incidente','id_cliente','descripcion','severidad','estado','fecha_incidente'], incidentes)
    utils.write_csv(os.path.join(config.RAW_DIR, 'riesgos', 'morosidad', 'morosidad.csv'),
                    ['id_morosidad','id_cliente','dias_mora','deuda_pendiente','fecha_reporte'], morosidades)

if __name__ == '__main__':
    generar_riesgos()