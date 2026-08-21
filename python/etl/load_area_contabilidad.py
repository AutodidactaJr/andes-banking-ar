# 📄 Archivo: python/etl/load_area_contabilidad.py
# Carga los CSV de Contabilidad desde subcarpetas

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
                if col.startswith('id_') or col == 'id_cuenta_contable':
                    try:
                        v = int(v) if v is not None else None
                    except (ValueError, TypeError):
                        v = None
                if col in ['monto_debe', 'monto_haber', 'monto_presupuestado']:
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
    RUTA_RAW_CONTAB = os.path.join(RUTA_BASE, 'data', 'raw', 'contabilidad')
    RUTA_DB = os.path.join(RUTA_BASE, 'data', 'databases', 'contabilidad.db')
    
    os.makedirs(os.path.dirname(RUTA_DB), exist_ok=True)
    
    conn = sqlite3.connect(RUTA_DB)
    with open(os.path.join(RUTA_BASE, 'sql', 'esquemas_area', 'contabilidad.sql'), 'r') as f:
        conn.executescript(f.read())
    conn.close()
    
    cargar_csv(os.path.join(RUTA_RAW_CONTAB, 'cuentas_contables', 'cuentas_contables.csv'), RUTA_DB, 'cuentas_contables',
               ['id_cuenta_contable','codigo_cuenta','descripcion','tipo_cuenta'])
    cargar_csv(os.path.join(RUTA_RAW_CONTAB, 'asientos_contables', 'asientos_contables.csv'), RUTA_DB, 'asientos_contables',
               ['id_asiento','id_cuenta_contable','fecha_contable','tipo_asiento','monto_debe','monto_haber','descripcion'])
    cargar_csv(os.path.join(RUTA_RAW_CONTAB, 'presupuesto', 'presupuesto.csv'), RUTA_DB, 'presupuesto',
               ['id_presupuesto','id_cuenta_contable','monto_presupuestado','fecha_presupuesto'])

if __name__ == '__main__':
    main()