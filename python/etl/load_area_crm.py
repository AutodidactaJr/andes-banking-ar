# 📄 Archivo: python/etl/load_area_crm.py
# Carga los CSV de CRM desde subcarpetas a crm.db

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
                if col.startswith('id_') or col == 'id_campana':
                    try:
                        v = int(v) if v is not None else None
                    except (ValueError, TypeError):
                        v = None
                if col == 'costo':
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
    RUTA_RAW_CRM = os.path.join(RUTA_BASE, 'data', 'raw', 'crm')
    RUTA_DB = os.path.join(RUTA_BASE, 'data', 'databases', 'crm.db')
    
    os.makedirs(os.path.dirname(RUTA_DB), exist_ok=True)
    
    conn = sqlite3.connect(RUTA_DB)
    with open(os.path.join(RUTA_BASE, 'sql', 'esquemas_area', 'crm.sql'), 'r') as f:
        conn.executescript(f.read())
    conn.close()
    
    cargar_csv(os.path.join(RUTA_RAW_CRM, 'campanas', 'campanas.csv'), RUTA_DB, 'campanas',
               ['id_campana','nombre','canal','segmento_objetivo','fecha_inicio','fecha_fin','costo'])
    cargar_csv(os.path.join(RUTA_RAW_CRM, 'interacciones', 'interacciones.csv'), RUTA_DB, 'interacciones',
               ['id_interaccion','id_campana','id_cliente','fecha','tipo_interaccion','dispositivo'])
    cargar_csv(os.path.join(RUTA_RAW_CRM, 'leads', 'leads.csv'), RUTA_DB, 'leads',
               ['id_lead','id_campana','id_cliente','fecha_creacion','estado','producto_interes'])
    cargar_csv(os.path.join(RUTA_RAW_CRM, 'oportunidades', 'oportunidades.csv'), RUTA_DB, 'oportunidades',
               ['id_oportunidad','id_cliente','producto_interes','fecha_creacion','estado'])
if __name__ == '__main__':
    main()