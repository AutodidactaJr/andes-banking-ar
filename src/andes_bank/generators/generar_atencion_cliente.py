# 📄 Archivo: src/andes_bank/generators/generar_atencion_cliente.py
# Generador de datos para Atención al Cliente

import random, os
from . import config, utils

def generar_atencion_cliente():
    utils.set_seed()
    clientes = utils.read_csv(os.path.join(config.RAW_DIR, 'core_bancario', 'clientes', 'clientes.csv'))
    ids_clientes = [int(c['id_cliente']) for c in clientes]

    # Tickets
    tickets = []
    for i in range(config.NUM_TICKETS):
        estado = random.choice(['Abierto', 'En proceso', 'Cerrado'])
        fecha_creacion = utils.random_datetime('2022-01-01', '2023-12-31')
        fecha_resolucion = utils.random_datetime(fecha_creacion[:10], '2023-12-31') if estado == 'Cerrado' else ''
        tickets.append({
            'id_ticket': i+1,
            'id_cliente': random.choice(ids_clientes),
            'tipo_reclamo': random.choice(['Reclamo', 'Consulta', 'Sugerencia', 'Error']),
            'descripcion': f"Ticket {i+1}",
            'estado': estado,
            'fecha_creacion': fecha_creacion,
            'fecha_resolucion': fecha_resolucion
        })

    # Llamadas
    llamadas = []
    for i in range(config.NUM_LLAMADAS):
        llamadas.append({
            'id_llamada': i+1,
            'id_cliente': random.choice(ids_clientes),
            'duracion_seg': random.randint(30, 1800),
            'resultado': random.choice(['Resuelto', 'No resuelto', 'Transferido']),
            'fecha_llamada': utils.random_datetime('2022-01-01', '2023-12-31')
        })

    # Encuestas
    encuestas = []
    for i in range(config.NUM_ENCUESTAS):
        encuestas.append({
            'id_encuesta': i+1,
            'id_cliente': random.choice(ids_clientes),
            'satisfaccion': random.randint(1, 5),
            'comentario': random.choice(['Excelente', 'Bueno', 'Regular', 'Malo']),
            'fecha_encuesta': utils.random_date('2022-01-01', '2023-12-31')
        })

    # Guardar en subcarpetas
    utils.write_csv(os.path.join(config.RAW_DIR, 'atencion_cliente', 'tickets', 'tickets.csv'),
                    ['id_ticket','id_cliente','tipo_reclamo','descripcion','estado','fecha_creacion','fecha_resolucion'], tickets)
    utils.write_csv(os.path.join(config.RAW_DIR, 'atencion_cliente', 'llamadas', 'llamadas.csv'),
                    ['id_llamada','id_cliente','duracion_seg','resultado','fecha_llamada'], llamadas)
    utils.write_csv(os.path.join(config.RAW_DIR, 'atencion_cliente', 'encuestas', 'encuestas.csv'),
                    ['id_encuesta','id_cliente','satisfaccion','comentario','fecha_encuesta'], encuestas)

if __name__ == '__main__':
    generar_atencion_cliente()