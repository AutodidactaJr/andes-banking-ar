# 📄 Archivo: python/etl/validaciones.py
# Script para validar la calidad de datos en las tablas de staging

import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ejecutar_regla(conn, descripcion, sql):
    """
    Ejecuta una regla de validación y devuelve el número de filas problemáticas.
    """
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        resultado = cursor.fetchone()
        cantidad = resultado[0] if resultado else 0
        logging.info(f"  [{'OK' if cantidad == 0 else 'PROBLEMA'}] {descripcion}: {cantidad} registro(s) afectado(s).")
        return cantidad
    except Exception as e:
        logging.error(f"  Error ejecutando regla '{descripcion}': {e}")
        return 0

def validar_calidad_datos(ruta_db):
    conn = sqlite3.connect(ruta_db)
    total_problemas = 0
    
    logging.info("=" * 60)
    logging.info("INICIANDO VALIDACIÓN DE CALIDAD DE DATOS")
    logging.info("=" * 60)
    
    # --- Clientes ---
    logging.info("Validando stg_clientes...")
    total_problemas += ejecutar_regla(conn,
        "Clientes con email vacío",
        "SELECT COUNT(*) FROM stg_clientes WHERE email IS NULL OR email = ''")
    total_problemas += ejecutar_regla(conn,
        "Clientes con teléfono vacío",
        "SELECT COUNT(*) FROM stg_clientes WHERE telefono IS NULL OR telefono = ''")
    total_problemas += ejecutar_regla(conn,
        "Clientes con fecha de nacimiento en formato dd/mm/yyyy",
        "SELECT COUNT(*) FROM stg_clientes WHERE fecha_nacimiento LIKE '%/%'")
    total_problemas += ejecutar_regla(conn,
        "IDs de cliente duplicados",
        "SELECT COUNT(*) FROM (SELECT id_cliente FROM stg_clientes GROUP BY id_cliente HAVING COUNT(*) > 1)")
    
    # --- Cuentas ---
    logging.info("Validando stg_cuentas...")
    total_problemas += ejecutar_regla(conn,
        "Cuentas con saldo negativo",
        "SELECT COUNT(*) FROM stg_cuentas WHERE saldo < 0")
    total_problemas += ejecutar_regla(conn,
        "Cuentas con fecha de apertura en formato incorrecto",
        "SELECT COUNT(*) FROM stg_cuentas WHERE fecha_apertura LIKE '%/%'")
    total_problemas += ejecutar_regla(conn,
        "Cuentas con cliente inexistente (integridad referencial)",
        """
        SELECT COUNT(*)
        FROM stg_cuentas c
        LEFT JOIN dim_cliente cl ON c.id_cliente = cl.id_cliente_nk
        WHERE cl.id_cliente_sk IS NULL
        """)
    
    # --- Tarjetas ---
    logging.info("Validando stg_tarjetas...")
    total_problemas += ejecutar_regla(conn,
        "Tarjetas con número duplicado",
        "SELECT COUNT(*) FROM (SELECT numero FROM stg_tarjetas GROUP BY numero HAVING COUNT(*) > 1)")
    total_problemas += ejecutar_regla(conn,
        "Tarjetas con fecha de vencimiento vencida",
        "SELECT COUNT(*) FROM stg_tarjetas WHERE fecha_vencimiento < '2024-01-01'")
    
    # --- Transacciones ---
    logging.info("Validando stg_transacciones...")
    total_problemas += ejecutar_regla(conn,
        "Transacciones con monto cero",
        "SELECT COUNT(*) FROM stg_transacciones WHERE monto = 0")
    total_problemas += ejecutar_regla(conn,
        "Transacciones con fecha inválida",
        "SELECT COUNT(*) FROM stg_transacciones WHERE date(substr(fecha,1,10)) IS NULL AND fecha LIKE '____-__-__%'")
    total_problemas += ejecutar_regla(conn,
        "Transacciones con cuenta inexistente",
        """
        SELECT COUNT(*)
        FROM stg_transacciones t
        LEFT JOIN dim_cuenta cu ON t.id_cuenta = cu.id_cuenta_nk
        WHERE cu.id_cuenta_sk IS NULL
        """)
    
    # --- Pagos ---
    logging.info("Validando stg_pagos...")
    total_problemas += ejecutar_regla(conn,
        "Pagos con monto negativo",
        "SELECT COUNT(*) FROM stg_pagos WHERE monto < 0")
    total_problemas += ejecutar_regla(conn,
        "Pagos con entidad vacía",
        "SELECT COUNT(*) FROM stg_pagos WHERE entidad IS NULL OR entidad = ''")
    
    logging.info("=" * 60)
    logging.info(f"TOTAL DE PROBLEMAS ENCONTRADOS: {total_problemas}")
    logging.info("=" * 60)
    conn.close()

if __name__ == '__main__':
    RUTA_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    RUTA_DB = os.path.join(RUTA_BASE, 'data', 'andes_dw.db')
    validar_calidad_datos(RUTA_DB)