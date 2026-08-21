# 📄 Archivo: python/etl/load_area_atencion.py
# Carga los CSV de Atención al Cliente desde subcarpetas

import csv
import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def cargar_csv(ruta_csv, ruta_db, tabla, columnas):
    if not os.path.exists(ruta_csv):
        logging.error(f"Falta {ruta_csv}")
        return
    conn = sqlite3.connect(ruta_db)
    cur = conn.cursor()
    with open(ruta_csv, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        placeholders = ','.join(['?'] * len(columnas))
        sql = f"INSERT OR REPLACE INTO {tabla} ({','.join(columnas)}) VALUES ({placeholders})"
        filas = 0
        for fila in lector:
            valores = []
            for col in columnas:
                v = fila.get(col, '')
                if v == '':
                    v = None
                if col.startswith('id_') or col in ['duracion_seg', 'satisfaccion', 'tiempo_objetivo_horas']:
                    try:
                        v = int(v) if v is not None else None
                    except (ValueError, TypeError):
                        v = None
                valores.append(v)
            cur.execute(sql, valores)
            filas += 1
    conn.commit()
    conn.close()
    logging.info(f"{tabla}: {filas} registros cargados.")

def main():
    RUTA_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    RUTA_RAW_ATENCION = os.path.join(RUTA_BASE, 'data', 'raw', 'atencion_cliente')
    RUTA_DB = os.path.join(RUTA_BASE, 'data', 'databases', 'atencion_cliente.db')

    os.makedirs(os.path.dirname(RUTA_DB), exist_ok=True)

    conn = sqlite3.connect(RUTA_DB)
    with open(os.path.join(RUTA_BASE, 'sql', 'esquemas_area', 'atencion_cliente.sql'), 'r') as f:
        conn.executescript(f.read())
    conn.close()

    cargar_csv(os.path.join(RUTA_RAW_ATENCION, 'tickets', 'tickets.csv'), RUTA_DB, 'tickets',
               ['id_ticket','id_cliente','tipo_reclamo','descripcion','estado','fecha_creacion','fecha_resolucion'])
    cargar_csv(os.path.join(RUTA_RAW_ATENCION, 'llamadas', 'llamadas.csv'), RUTA_DB, 'llamadas',
               ['id_llamada','id_cliente','duracion_seg','resultado','fecha_llamada'])
    cargar_csv(os.path.join(RUTA_RAW_ATENCION, 'encuestas', 'encuestas.csv'), RUTA_DB, 'encuestas',
               ['id_encuesta','id_cliente','satisfaccion','comentario','fecha_encuesta'])

    # Nuevas tablas
    cargar_csv(os.path.join(RUTA_RAW_ATENCION, 'agentes', 'agentes.csv'), RUTA_DB, 'agentes',
               ['id_agente','nombre','apellido','id_sucursal'])
    cargar_csv(os.path.join(RUTA_RAW_ATENCION, 'sla_tickets', 'sla_tickets.csv'), RUTA_DB, 'sla_tickets',
               ['id_sla','tipo_reclamo','tiempo_objetivo_horas'])

if __name__ == '__main__':
    main()