# 📄 Archivo: python/etl/load_crm_to_dw.py
# Carga datos de CRM al Data Warehouse con auditoría

import sqlite3
import os
import logging
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def registrar_log(conn, script, filas_afectadas, estado, mensaje=''):
    fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute("""
        INSERT INTO etl_log (script, fecha_ejecucion, filas_afectadas, estado, mensaje)
        VALUES (?, ?, ?, ?, ?)
    """, (script, fecha, filas_afectadas, estado, mensaje))
    conn.commit()

def cargar_dim_campana(conn_crm, conn_dw):
    cursor_crm = conn_crm.cursor()
    cursor_dw = conn_dw.cursor()
    cursor_crm.execute("SELECT id_campana, nombre, canal, segmento_objetivo, fecha_inicio, fecha_fin, costo FROM campanas")
    filas = cursor_crm.fetchall()
    for fila in filas:
        cursor_dw.execute("""
            INSERT OR REPLACE INTO dim_campana (id_campana_nk, nombre, canal, segmento_objetivo, fecha_inicio, fecha_fin, costo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, fila)
    conn_dw.commit()
    count = cursor_dw.execute("SELECT COUNT(*) FROM dim_campana").fetchone()[0]
    logging.info(f"dim_campana cargada con {count} registros.")
    return count

def cargar_fact_interacciones(conn_crm, conn_dw):
    cursor_crm = conn_crm.cursor()
    cursor_dw = conn_dw.cursor()
    cursor_crm.execute("""
        SELECT id_interaccion, id_campana, id_cliente, fecha, tipo_interaccion, dispositivo
        FROM interacciones
    """)
    filas = cursor_crm.fetchall()
    insertadas = 0
    for fila in filas:
        id_interaccion, id_campana_nk, id_cliente_nk, fecha, tipo, dispositivo = fila
        cursor_dw.execute("SELECT id_campana_sk FROM dim_campana WHERE id_campana_nk = ?", (id_campana_nk,))
        res = cursor_dw.fetchone()
        if not res: continue
        id_campana_sk = res[0]
        cursor_dw.execute("SELECT id_cliente_sk FROM dim_cliente WHERE id_cliente_nk = ? AND es_actual = 1", (id_cliente_nk,))
        res = cursor_dw.fetchone()
        if not res: continue
        id_cliente_sk = res[0]
        cursor_dw.execute("SELECT id_tiempo_sk FROM dim_tiempo WHERE fecha = substr(?, 1, 10)", (fecha,))
        res = cursor_dw.fetchone()
        id_tiempo_sk = res[0] if res else None
        cursor_dw.execute("""
            INSERT OR IGNORE INTO fact_interacciones_campana
            (id_interaccion_nk, id_campana_sk, id_cliente_sk, id_tiempo_sk, tipo_interaccion, dispositivo, fecha_completa)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_interaccion, id_campana_sk, id_cliente_sk, id_tiempo_sk, tipo, dispositivo, fecha))
        insertadas += 1
    conn_dw.commit()
    logging.info(f"fact_interacciones_campana cargada con {insertadas} registros.")
    return insertadas

def cargar_fact_leads(conn_crm, conn_dw):
    cursor_crm = conn_crm.cursor()
    cursor_dw = conn_dw.cursor()
    cursor_crm.execute("""
        SELECT id_lead, id_campana, id_cliente, fecha_creacion, estado, producto_interes
        FROM leads
    """)
    filas = cursor_crm.fetchall()
    insertadas = 0
    for fila in filas:
        id_lead, id_campana_nk, id_cliente_nk, fecha_creacion, estado, producto = fila
        cursor_dw.execute("SELECT id_campana_sk FROM dim_campana WHERE id_campana_nk = ?", (id_campana_nk,))
        res = cursor_dw.fetchone()
        if not res: continue
        id_campana_sk = res[0]
        id_cliente_sk = None
        if id_cliente_nk and id_cliente_nk != '':
            cursor_dw.execute("SELECT id_cliente_sk FROM dim_cliente WHERE id_cliente_nk = ? AND es_actual = 1", (id_cliente_nk,))
            res = cursor_dw.fetchone()
            if res:
                id_cliente_sk = res[0]
        cursor_dw.execute("SELECT id_tiempo_sk FROM dim_tiempo WHERE fecha = ?", (fecha_creacion,))
        res = cursor_dw.fetchone()
        id_tiempo_sk = res[0] if res else None
        cursor_dw.execute("""
            INSERT OR IGNORE INTO fact_leads
            (id_lead_nk, id_campana_sk, id_cliente_sk, id_tiempo_sk, estado, producto_interes, fecha_creacion)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_lead, id_campana_sk, id_cliente_sk, id_tiempo_sk, estado, producto, fecha_creacion))
        insertadas += 1
    conn_dw.commit()
    logging.info(f"fact_leads cargada con {insertadas} registros.")
    return insertadas

def main():
    RUTA_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    RUTA_CRM_DB = os.path.join(RUTA_BASE, 'data', 'databases', 'crm.db')
    RUTA_DW = os.path.join(RUTA_BASE, 'data', 'andes_dw.db')
    
    conn_crm = sqlite3.connect(RUTA_CRM_DB)
    conn_dw = sqlite3.connect(RUTA_DW)
    conn_dw.execute("PRAGMA foreign_keys = ON")
    script_name = 'load_crm_to_dw.py'
    
    registrar_log(conn_dw, script_name, 0, 'INICIO')
    
    try:
        logging.info("Cargando CRM al Data Warehouse...")
        total = 0
        total += cargar_dim_campana(conn_crm, conn_dw)
        total += cargar_fact_interacciones(conn_crm, conn_dw)
        total += cargar_fact_leads(conn_crm, conn_dw)
        registrar_log(conn_dw, script_name, total, 'EXITO', 'CRM cargado correctamente')
    except Exception as e:
        conn_dw.rollback()
        registrar_log(conn_dw, script_name, 0, 'ERROR', str(e))
        logging.error(f"Error: {e}")
    finally:
        conn_crm.close()
        conn_dw.close()

if __name__ == '__main__':
    main()