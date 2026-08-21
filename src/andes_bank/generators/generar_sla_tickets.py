# 📄 Archivo: src/andes_bank/generators/generar_sla_tickets.py
# Generador de acuerdos de nivel de servicio (SLA)

import os
from . import config, utils

def generar_sla_tickets():
    utils.set_seed()
    tipos_reclamo = ['Reclamo', 'Consulta', 'Sugerencia', 'Error', 'Queja', 'Solicitud']
    sla = []
    for i, tipo in enumerate(tipos_reclamo):
        sla.append({
            'id_sla': i + 1,
            'tipo_reclamo': tipo,
            'tiempo_objetivo_horas': config.TIEMPO_SLA[tipo] if hasattr(config, 'TIEMPO_SLA') else 24
        })

    fieldnames = ['id_sla','tipo_reclamo','tiempo_objetivo_horas']
    ruta = os.path.join(config.RAW_DIR, 'atencion_cliente', 'sla_tickets', 'sla_tickets.csv')
    utils.write_csv(ruta, fieldnames, sla)

if __name__ == '__main__':
    generar_sla_tickets()