# 📄 Archivo: python/etl/load_area_rrhh.py
# Carga los CSV de RRHH a rrhh.db

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
                if col.startswith('id_') or col == 'dias' or col == 'anio' or col == 'puntaje':
                    try:
                        v = int(v) if v is not None else None
                    except (ValueError, TypeError):
                        v = None
                if col == 'salario':
                    try:
                        v = float(v) if v is not None else None
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
    RUTA_RAW_RRHH = os.path.join(RUTA_BASE, 'data', 'raw', 'rrhh')
    RUTA_DB = os.path.join(RUTA_BASE, 'data', 'databases', 'rrhh.db')

    os.makedirs(os.path.dirname(RUTA_DB), exist_ok=True)

    # Crear tablas
    conn = sqlite3.connect(RUTA_DB)
    with open(os.path.join(RUTA_BASE, 'sql', 'esquemas_area', 'rrhh.sql'), 'r') as f:
        conn.executescript(f.read())
    conn.close()

    # Cargar empleados y ausencias
    cargar_csv(os.path.join(RUTA_RAW_RRHH, 'empleados', 'empleados.csv'), RUTA_DB, 'empleados',
               ['id_empleado','nombre','apellido','cargo','id_sucursal','fecha_contratacion','salario'])
    cargar_csv(os.path.join(RUTA_RAW_RRHH, 'ausencias', 'ausencias.csv'), RUTA_DB, 'ausencias',
               ['id_ausencia','id_empleado','tipo_ausencia','dias','fecha_inicio','fecha_fin'])

    # Cargar nuevas tablas
    cargar_csv(os.path.join(RUTA_RAW_RRHH, 'salarios_historial', 'salarios_historial.csv'), RUTA_DB, 'salarios_historial',
               ['id_salario','id_empleado','salario','fecha_inicio','fecha_fin'])
    cargar_csv(os.path.join(RUTA_RAW_RRHH, 'evaluaciones', 'evaluaciones.csv'), RUTA_DB, 'evaluaciones',
               ['id_evaluacion','id_empleado','anio','puntaje','comentario'])

if __name__ == '__main__':
    main()