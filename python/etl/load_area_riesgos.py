# 📄 Archivo: python/etl/load_area_riesgos.py
# Carga los CSV de Riesgos desde subcarpetas a riesgos.db

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
                if col.startswith('id_') or col in ['score', 'dias_mora']:
                    try:
                        v = int(v) if v is not None else None
                    except (ValueError, TypeError):
                        v = None
                if col in ['monto', 'deuda_pendiente']:
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
    RUTA_RAW_RIESGOS = os.path.join(RUTA_BASE, 'data', 'raw', 'riesgos')
    RUTA_DB = os.path.join(RUTA_BASE, 'data', 'databases', 'riesgos.db')
    
    os.makedirs(os.path.dirname(RUTA_DB), exist_ok=True)
    
    conn = sqlite3.connect(RUTA_DB)
    with open(os.path.join(RUTA_BASE, 'sql', 'esquemas_area', 'riesgos.sql'), 'r') as f:
        conn.executescript(f.read())
    conn.close()
    
    cargar_csv(os.path.join(RUTA_RAW_RIESGOS, 'scoring_crediticio', 'scoring_crediticio.csv'), RUTA_DB, 'scoring_crediticio',
               ['id_scoring','id_cliente','score','riesgo','fecha_calculo'])
    cargar_csv(os.path.join(RUTA_RAW_RIESGOS, 'alertas_fraude', 'alertas_fraude.csv'), RUTA_DB, 'alertas_fraude',
               ['id_alerta','id_cliente','id_cuenta','tipo_alerta','monto','estado','fecha_deteccion'])
    cargar_csv(os.path.join(RUTA_RAW_RIESGOS, 'incidentes', 'incidentes.csv'), RUTA_DB, 'incidentes',
               ['id_incidente','id_cliente','descripcion','severidad','estado','fecha_incidente'])
    cargar_csv(os.path.join(RUTA_RAW_RIESGOS, 'morosidad', 'morosidad.csv'), RUTA_DB, 'morosidad',
               ['id_morosidad','id_cliente','dias_mora','deuda_pendiente','fecha_reporte'])

if __name__ == '__main__':
    main()