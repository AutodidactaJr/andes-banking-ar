# 📄 Archivo: python/etl/load_hechos.py
# Carga hechos desde staging con limpieza selectiva
# Incluye:
#   - fact_transacciones
#   - fact_pagos
#   - fact_interacciones_campana
#   - fact_leads
#   - fact_reclamos
#   - fact_ausencias
#   - fact_scoring_crediticio
#   - fact_alertas_fraude
#   - fact_asientos_contables
#   - fact_plazos_fijos
#   - fact_seguros
#   - fact_salarios_historial
#   - fact_evaluaciones
#   - fact_oportunidades

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

# ---------- HECHO TRANSACCIONES ----------
def cargar_fact_transacciones(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO fact_transacciones (
            id_transaccion_nk, id_cliente_sk, id_cuenta_sk, id_sucursal_sk, id_canal_sk,
            id_tiempo_sk, id_producto_sk, tipo_transaccion, monto, moneda, estado,
            referencia, fecha_completa
        )
        SELECT
            t.id_transaccion,
            cu.id_cliente_sk,
            cu.id_cuenta_sk,
            cu.id_sucursal_sk,
            ca.id_canal_sk,
            ti.id_tiempo_sk,
            NULL,
            t.tipo_transaccion,
            t.monto,
            t.moneda,
            t.estado,
            t.referencia,
            t.fecha
        FROM stg_transacciones t
        INNER JOIN dim_cuenta cu ON t.id_cuenta = cu.id_cuenta_nk AND cu.es_actual = 1
        LEFT JOIN dim_canal ca ON t.canal = ca.canal_nombre
        LEFT JOIN dim_tiempo ti ON substr(t.fecha, 1, 10) = ti.fecha
        WHERE cu.id_cuenta_sk IS NOT NULL
          AND t.monto <> 0
    """)
    conn.commit()
    logging.info("fact_transacciones cargada (sin montos cero).")

# ---------- HECHO PAGOS ----------
def cargar_fact_pagos(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO fact_pagos (
            id_pago_nk, id_cliente_sk, id_cuenta_sk, id_canal_sk, id_tiempo_sk,
            entidad, tipo_pago, monto, estado, referencia, fecha_completa
        )
        SELECT
            p.id_pago,
            cu.id_cliente_sk,
            cu.id_cuenta_sk,
            ca.id_canal_sk,
            ti.id_tiempo_sk,
            CASE WHEN p.entidad IS NULL OR p.entidad = '' THEN 'Desconocido' ELSE p.entidad END,
            p.tipo_pago,
            CASE WHEN p.monto < 0 THEN ABS(p.monto) ELSE p.monto END,
            p.estado,
            p.referencia,
            p.fecha
        FROM stg_pagos p
        INNER JOIN dim_cuenta cu ON p.id_cuenta = cu.id_cuenta_nk AND cu.es_actual = 1
        LEFT JOIN dim_canal ca ON p.canal = ca.canal_nombre
        LEFT JOIN dim_tiempo ti ON substr(p.fecha, 1, 10) = ti.fecha
        WHERE cu.id_cuenta_sk IS NOT NULL
    """)
    conn.commit()
    logging.info("fact_pagos cargada (montos negativos corregidos, entidades completadas).")

# ---------- HECHO INTERACCIONES CAMPAÑA ----------
def cargar_fact_interacciones_campana(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO fact_interacciones_campana (
            id_interaccion_nk, id_campana_sk, id_cliente_sk, id_tiempo_sk,
            tipo_interaccion, dispositivo, fecha_completa
        )
        SELECT
            i.id_interaccion,
            dc.id_campana_sk,
            cl.id_cliente_sk,
            ti.id_tiempo_sk,
            i.tipo_interaccion,
            i.dispositivo,
            i.fecha
        FROM stg_interacciones i
        INNER JOIN dim_campana dc ON i.id_campana = dc.id_campana_nk
        INNER JOIN dim_cliente cl ON i.id_cliente = cl.id_cliente_nk AND cl.es_actual = 1
        LEFT JOIN dim_tiempo ti ON substr(i.fecha, 1, 10) = ti.fecha
    """)
    conn.commit()
    logging.info("fact_interacciones_campana cargada.")

# ---------- HECHO LEADS ----------
def cargar_fact_leads(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO fact_leads (
            id_lead_nk, id_campana_sk, id_cliente_sk, id_tiempo_sk,
            estado, producto_interes, fecha_creacion
        )
        SELECT
            l.id_lead,
            dc.id_campana_sk,
            cl.id_cliente_sk,
            ti.id_tiempo_sk,
            l.estado,
            l.producto_interes,
            l.fecha_creacion
        FROM stg_leads l
        INNER JOIN dim_campana dc ON l.id_campana = dc.id_campana_nk
        LEFT JOIN dim_cliente cl ON l.id_cliente = cl.id_cliente_nk AND cl.es_actual = 1
        LEFT JOIN dim_tiempo ti ON l.fecha_creacion = ti.fecha
    """)
    conn.commit()
    logging.info("fact_leads cargada.")

# ---------- HECHO RECLAMOS ----------
def cargar_fact_reclamos(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO fact_reclamos (
            id_reclamo_nk, id_cliente_sk, id_sucursal_sk, id_tipo_reclamo_sk, id_tiempo_sk,
            estado, resolucion_dias, fecha_creacion, fecha_resolucion
        )
        SELECT
            t.id_ticket,
            cl.id_cliente_sk,
            NULL,
            tr.id_tipo_reclamo_sk,
            ti.id_tiempo_sk,
            t.estado,
            CASE WHEN t.fecha_resolucion IS NOT NULL AND t.fecha_resolucion != '' THEN
                CAST((julianday(t.fecha_resolucion) - julianday(t.fecha_creacion)) AS INTEGER)
            ELSE NULL END,
            t.fecha_creacion,
            t.fecha_resolucion
        FROM stg_tickets t
        INNER JOIN dim_cliente cl ON t.id_cliente = cl.id_cliente_nk AND cl.es_actual = 1
        LEFT JOIN dim_tipo_reclamo tr ON t.tipo_reclamo = tr.tipo_reclamo_nombre
        LEFT JOIN dim_tiempo ti ON substr(t.fecha_creacion, 1, 10) = ti.fecha
    """)
    conn.commit()
    logging.info("fact_reclamos cargada.")

# ---------- HECHO AUSENCIAS ----------
def cargar_fact_ausencias(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO fact_ausencias (
            id_ausencia_nk, id_empleado_sk, id_sucursal_sk, id_tiempo_sk,
            tipo_ausencia, dias, fecha_inicio, fecha_fin
        )
        SELECT
            a.id_ausencia,
            de.id_empleado_sk,
            de.id_sucursal_sk,
            ti.id_tiempo_sk,
            a.tipo_ausencia,
            a.dias,
            a.fecha_inicio,
            a.fecha_fin
        FROM stg_ausencias a
        INNER JOIN dim_empleado de ON a.id_empleado = de.id_empleado_nk
        LEFT JOIN dim_tiempo ti ON a.fecha_inicio = ti.fecha
    """)
    conn.commit()
    logging.info("fact_ausencias cargada.")

# ---------- HECHO SCORING CREDITICIO ----------
def cargar_fact_scoring_crediticio(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO fact_scoring_crediticio (
            id_scoring_nk, id_cliente_sk, id_tiempo_sk, score, riesgo, fecha_calculo
        )
        SELECT
            s.id_scoring,
            cl.id_cliente_sk,
            ti.id_tiempo_sk,
            s.score,
            s.riesgo,
            s.fecha_calculo
        FROM stg_scoring_crediticio s
        INNER JOIN dim_cliente cl ON s.id_cliente = cl.id_cliente_nk AND cl.es_actual = 1
        LEFT JOIN dim_tiempo ti ON s.fecha_calculo = ti.fecha
    """)
    conn.commit()
    logging.info("fact_scoring_crediticio cargada.")

# ---------- HECHO ALERTAS FRAUDE ----------
def cargar_fact_alertas_fraude(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO fact_alertas_fraude (
            id_alerta_nk, id_cliente_sk, id_cuenta_sk, id_tipo_riesgo_sk, id_tiempo_sk,
            tipo_alerta, monto, estado, fecha_deteccion
        )
        SELECT
            a.id_alerta,
            cl.id_cliente_sk,
            cu.id_cuenta_sk,
            tr.id_tipo_riesgo_sk,
            ti.id_tiempo_sk,
            a.tipo_alerta,
            a.monto,
            a.estado,
            a.fecha_deteccion
        FROM stg_alertas_fraude a
        INNER JOIN dim_cliente cl ON a.id_cliente = cl.id_cliente_nk AND cl.es_actual = 1
        LEFT JOIN dim_cuenta cu ON a.id_cuenta = cu.id_cuenta_nk AND cu.es_actual = 1
        LEFT JOIN dim_tipo_riesgo tr ON a.tipo_alerta = tr.tipo_riesgo_nombre
        LEFT JOIN dim_tiempo ti ON substr(a.fecha_deteccion, 1, 10) = ti.fecha
    """)
    conn.commit()
    logging.info("fact_alertas_fraude cargada.")

# ---------- HECHO ASIENTOS CONTABLES ----------
def cargar_fact_asientos_contables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO fact_asientos_contables (
            id_asiento_nk, id_cuenta_contable_sk, id_tiempo_sk, id_sucursal_sk,
            tipo_asiento, monto_debe, monto_haber, descripcion, fecha_contable
        )
        SELECT
            a.id_asiento,
            cc.id_cuenta_contable_sk,
            ti.id_tiempo_sk,
            NULL,
            a.tipo_asiento,
            a.monto_debe,
            a.monto_haber,
            a.descripcion,
            a.fecha_contable
        FROM stg_asientos_contables a
        INNER JOIN stg_cuentas_contables scc ON a.id_cuenta_contable = scc.id_cuenta_contable
        INNER JOIN dim_cuenta_contable cc ON scc.codigo_cuenta = cc.codigo_cuenta
        LEFT JOIN dim_tiempo ti ON a.fecha_contable = ti.fecha
    """)
    conn.commit()
    logging.info("fact_asientos_contables cargada.")

# ---------- NUEVO HECHO PLAZOS FIJOS ----------
def cargar_fact_plazos_fijos(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO fact_plazos_fijos (
            id_plazo_nk, id_cliente_sk, id_tiempo_sk, monto, tasa_interes, fecha_vencimiento, estado
        )
        SELECT
            p.id_plazo_fijo,
            cl.id_cliente_sk,
            ti.id_tiempo_sk,
            p.monto,
            p.tasa_interes,
            p.fecha_vencimiento,
            p.estado
        FROM stg_plazos_fijos p
        INNER JOIN dim_cliente cl ON p.id_cliente = cl.id_cliente_nk AND cl.es_actual = 1
        LEFT JOIN dim_tiempo ti ON p.fecha_constitucion = ti.fecha
    """)
    conn.commit()
    logging.info("fact_plazos_fijos cargada.")

# ---------- NUEVO HECHO SEGUROS ----------
def cargar_fact_seguros(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO fact_seguros (
            id_seguro_nk, id_cliente_sk, id_seguro_tipo_sk, id_tiempo_sk, prima_mensual, estado
        )
        SELECT
            s.id_seguro,
            cl.id_cliente_sk,
            ds.id_seguro_sk,
            ti.id_tiempo_sk,
            s.prima_mensual,
            s.estado
        FROM stg_seguros s
        INNER JOIN dim_cliente cl ON s.id_cliente = cl.id_cliente_nk AND cl.es_actual = 1
        LEFT JOIN dim_seguro ds ON s.id_seguro = ds.id_seguro_nk
        LEFT JOIN dim_tiempo ti ON s.fecha_contratacion = ti.fecha
    """)
    conn.commit()
    logging.info("fact_seguros cargada.")

# ---------- NUEVO HECHO SALARIOS HISTORIAL ----------
def cargar_fact_salarios_historial(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO fact_salarios_historial (
            id_salario_nk, id_empleado_sk, salario, fecha_inicio, fecha_fin
        )
        SELECT
            s.id_salario,
            de.id_empleado_sk,
            s.salario,
            s.fecha_inicio,
            s.fecha_fin
        FROM stg_salarios_historial s
        INNER JOIN dim_empleado de ON s.id_empleado = de.id_empleado_nk
    """)
    conn.commit()
    logging.info("fact_salarios_historial cargada.")

# ---------- NUEVO HECHO EVALUACIONES ----------
def cargar_fact_evaluaciones(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO fact_evaluaciones (
            id_evaluacion_nk, id_empleado_sk, anio, puntaje, comentario
        )
        SELECT
            e.id_evaluacion,
            de.id_empleado_sk,
            e.anio,
            e.puntaje,
            e.comentario
        FROM stg_evaluaciones e
        INNER JOIN dim_empleado de ON e.id_empleado = de.id_empleado_nk
    """)
    conn.commit()
    logging.info("fact_evaluaciones cargada.")

# ---------- NUEVO HECHO OPORTUNIDADES ----------
def cargar_fact_oportunidades(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO fact_oportunidades (
            id_oportunidad_nk, id_cliente_sk, id_tiempo_sk, producto_interes, estado, fecha_creacion
        )
        SELECT
            o.id_oportunidad,
            cl.id_cliente_sk,
            ti.id_tiempo_sk,
            o.producto_interes,
            o.estado,
            o.fecha_creacion
        FROM stg_oportunidades o
        INNER JOIN dim_cliente cl ON o.id_cliente = cl.id_cliente_nk AND cl.es_actual = 1
        LEFT JOIN dim_tiempo ti ON o.fecha_creacion = ti.fecha
    """)
    conn.commit()
    logging.info("fact_oportunidades cargada.")

# ---------- MAIN ----------
def main():
    RUTA_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    RUTA_DB = os.path.join(RUTA_BASE, 'data', 'andes_dw.db')
    conn = sqlite3.connect(RUTA_DB)
    conn.execute("PRAGMA foreign_keys = OFF")
    script_name = 'load_hechos.py'
    registrar_log(conn, script_name, 0, 'INICIO')
    try:
        logging.info("Cargando hechos...")
        cargar_fact_transacciones(conn)
        cargar_fact_pagos(conn)
        cargar_fact_interacciones_campana(conn)
        cargar_fact_leads(conn)
        cargar_fact_reclamos(conn)
        cargar_fact_ausencias(conn)
        cargar_fact_scoring_crediticio(conn)
        cargar_fact_alertas_fraude(conn)
        cargar_fact_asientos_contables(conn)
        cargar_fact_plazos_fijos(conn)
        cargar_fact_seguros(conn)
        cargar_fact_salarios_historial(conn)
        cargar_fact_evaluaciones(conn)
        cargar_fact_oportunidades(conn)
        total = conn.execute("""
            SELECT (SELECT COUNT(*) FROM fact_transacciones) +
                   (SELECT COUNT(*) FROM fact_pagos) +
                   (SELECT COUNT(*) FROM fact_interacciones_campana) +
                   (SELECT COUNT(*) FROM fact_leads) +
                   (SELECT COUNT(*) FROM fact_reclamos) +
                   (SELECT COUNT(*) FROM fact_ausencias) +
                   (SELECT COUNT(*) FROM fact_scoring_crediticio) +
                   (SELECT COUNT(*) FROM fact_alertas_fraude) +
                   (SELECT COUNT(*) FROM fact_asientos_contables) +
                   (SELECT COUNT(*) FROM fact_plazos_fijos) +
                   (SELECT COUNT(*) FROM fact_seguros) +
                   (SELECT COUNT(*) FROM fact_salarios_historial) +
                   (SELECT COUNT(*) FROM fact_evaluaciones) +
                   (SELECT COUNT(*) FROM fact_oportunidades)
        """).fetchone()[0]
        registrar_log(conn, script_name, total, 'EXITO', 'Todos los hechos cargados')
    except Exception as e:
        conn.rollback()
        registrar_log(conn, script_name, 0, 'ERROR', str(e))
        logging.error(f"Error: {e}")
    finally:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.close()

if __name__ == '__main__':
    main()