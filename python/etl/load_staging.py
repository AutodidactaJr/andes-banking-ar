# 📄 Archivo: python/etl/load_staging.py
# Carga staging extrayendo desde las bases de datos de área
# Incluye tablas nuevas: plazos_fijos, seguros, salarios_historial,
# evaluaciones, agentes, sla_tickets, oportunidades

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

def extraer_tabla_area(conn_dw, ruta_db, nombre_tabla_area, nombre_tabla_staging):
    """Copia datos de una tabla de área a staging en el DW."""
    try:
        conn_dw.execute("ATTACH DATABASE ? AS area_tmp", (ruta_db,))
        cursor = conn_dw.cursor()
        cursor.execute(f"INSERT OR REPLACE INTO {nombre_tabla_staging} SELECT * FROM area_tmp.{nombre_tabla_area}")
        conn_dw.commit()
        cursor.execute(f"SELECT COUNT(*) FROM {nombre_tabla_staging}")
        filas = cursor.fetchone()[0]
        logging.info(f"{nombre_tabla_staging}: {filas} registros.")
        conn_dw.execute("DETACH DATABASE area_tmp")
        return filas
    except Exception as e:
        logging.error(f"Error copiando {nombre_tabla_area} a {nombre_tabla_staging}: {e}")
        return 0

def main():
    RUTA_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    RUTA_DW = os.path.join(RUTA_BASE, 'data', 'andes_dw.db')
    RUTA_DBS = os.path.join(RUTA_BASE, 'data', 'databases')

    conn_dw = sqlite3.connect(RUTA_DW)
    conn_dw.execute("PRAGMA foreign_keys = OFF")
    script_name = 'load_staging.py'
    registrar_log(conn_dw, script_name, 0, 'INICIO')

    total_filas = 0
    try:
        # ==============================================
        # CORE BANCARIO
        # ==============================================
        ruta_core = os.path.join(RUTA_DBS, 'core_bancario.db')
        tablas_core = [
            ('clientes', 'stg_clientes'),
            ('sucursales', 'stg_sucursales'),
            ('cuentas', 'stg_cuentas'),
            ('tarjetas', 'stg_tarjetas'),
            ('prestamos', 'stg_prestamos'),
            ('transacciones', 'stg_transacciones'),
            ('pagos', 'stg_pagos'),
            ('plazos_fijos', 'stg_plazos_fijos'),
            ('seguros', 'stg_seguros')
        ]
        for tabla_area, tabla_staging in tablas_core:
            total_filas += extraer_tabla_area(conn_dw, ruta_core, tabla_area, tabla_staging)

        # ==============================================
        # CRM
        # ==============================================
        ruta_crm = os.path.join(RUTA_DBS, 'crm.db')
        tablas_crm = [
            ('campanas', 'stg_campanas'),
            ('interacciones', 'stg_interacciones'),
            ('leads', 'stg_leads'),
            ('oportunidades', 'stg_oportunidades')
        ]
        for tabla_area, tabla_staging in tablas_crm:
            total_filas += extraer_tabla_area(conn_dw, ruta_crm, tabla_area, tabla_staging)

        # ==============================================
        # RIESGOS
        # ==============================================
        ruta_riesgos = os.path.join(RUTA_DBS, 'riesgos.db')
        tablas_riesgos = [
            ('scoring_crediticio', 'stg_scoring_crediticio'),
            ('alertas_fraude', 'stg_alertas_fraude'),
            ('incidentes', 'stg_incidentes'),
            ('morosidad', 'stg_morosidad')
        ]
        for tabla_area, tabla_staging in tablas_riesgos:
            total_filas += extraer_tabla_area(conn_dw, ruta_riesgos, tabla_area, tabla_staging)

        # ==============================================
        # ATENCIÓN AL CLIENTE
        # ==============================================
        ruta_atencion = os.path.join(RUTA_DBS, 'atencion_cliente.db')
        tablas_atencion = [
            ('tickets', 'stg_tickets'),
            ('llamadas', 'stg_llamadas'),
            ('encuestas', 'stg_encuestas'),
            ('agentes', 'stg_agentes'),
            ('sla_tickets', 'stg_sla_tickets')
        ]
        for tabla_area, tabla_staging in tablas_atencion:
            total_filas += extraer_tabla_area(conn_dw, ruta_atencion, tabla_area, tabla_staging)

        # ==============================================
        # RRHH
        # ==============================================
        ruta_rrhh = os.path.join(RUTA_DBS, 'rrhh.db')
        tablas_rrhh = [
            ('empleados', 'stg_empleados'),
            ('ausencias', 'stg_ausencias'),
            ('salarios_historial', 'stg_salarios_historial'),
            ('evaluaciones', 'stg_evaluaciones')
        ]
        for tabla_area, tabla_staging in tablas_rrhh:
            total_filas += extraer_tabla_area(conn_dw, ruta_rrhh, tabla_area, tabla_staging)

        # ==============================================
        # CONTABILIDAD
        # ==============================================
        ruta_contab = os.path.join(RUTA_DBS, 'contabilidad.db')
        tablas_contab = [
            ('cuentas_contables', 'stg_cuentas_contables'),
            ('asientos_contables', 'stg_asientos_contables'),
            ('presupuesto', 'stg_presupuesto')
        ]
        for tabla_area, tabla_staging in tablas_contab:
            total_filas += extraer_tabla_area(conn_dw, ruta_contab, tabla_area, tabla_staging)

        registrar_log(conn_dw, script_name, total_filas, 'EXITO', 'Staging cargado desde todas las áreas')
    except Exception as e:
        conn_dw.rollback()
        registrar_log(conn_dw, script_name, 0, 'ERROR', str(e))
        logging.error(f"Error general: {e}")
    finally:
        conn_dw.execute("PRAGMA foreign_keys = ON")
        conn_dw.close()

if __name__ == '__main__':
    main()