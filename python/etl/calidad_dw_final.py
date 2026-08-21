# 📄 Archivo: python/etl/calidad_dw_final.py
# Framework de calidad de datos final: valida staging y Data Warehouse
# Incluye reglas para nuevas tablas: plazos_fijos, seguros, salarios_historial, evaluaciones

import sqlite3
import os
import logging
import csv
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ------------------------------------------------------------
# Reglas de calidad para staging (errores crudos esperados)
# ------------------------------------------------------------
REGLAS_STAGING = [
    {
        'tabla': 'stg_clientes',
        'descripcion': 'Clientes con email vacío',
        'sql': "SELECT COUNT(*) FROM stg_clientes WHERE email IS NULL OR email = ''"
    },
    {
        'tabla': 'stg_clientes',
        'descripcion': 'Clientes con teléfono vacío',
        'sql': "SELECT COUNT(*) FROM stg_clientes WHERE telefono IS NULL OR telefono = ''"
    },
    {
        'tabla': 'stg_clientes',
        'descripcion': 'Clientes con fecha de nacimiento en formato dd/mm/yyyy',
        'sql': "SELECT COUNT(*) FROM stg_clientes WHERE fecha_nacimiento LIKE '%/%'"
    },
    {
        'tabla': 'stg_cuentas',
        'descripcion': 'Cuentas con saldo negativo',
        'sql': "SELECT COUNT(*) FROM stg_cuentas WHERE saldo < 0"
    },
    {
        'tabla': 'stg_cuentas',
        'descripcion': 'Cuentas con fecha de apertura en formato incorrecto',
        'sql': "SELECT COUNT(*) FROM stg_cuentas WHERE fecha_apertura LIKE '%/%'"
    },
    {
        'tabla': 'stg_transacciones',
        'descripcion': 'Transacciones con monto cero',
        'sql': "SELECT COUNT(*) FROM stg_transacciones WHERE monto = 0"
    },
    {
        'tabla': 'stg_pagos',
        'descripcion': 'Pagos con monto negativo',
        'sql': "SELECT COUNT(*) FROM stg_pagos WHERE monto < 0"
    },
    {
        'tabla': 'stg_pagos',
        'descripcion': 'Pagos con entidad vacía',
        'sql': "SELECT COUNT(*) FROM stg_pagos WHERE entidad IS NULL OR entidad = ''"
    },
]

# ------------------------------------------------------------
# Reglas de calidad para Data Warehouse final (deben ser 0)
# ------------------------------------------------------------
REGLAS_DW = [
    {
        'tabla': 'dim_cuenta',
        'descripcion': 'Cajas de ahorro con saldo negativo (error de negocio)',
        'sql': """
            SELECT COUNT(*)
            FROM dim_cuenta
            WHERE saldo < 0
              AND tipo_cuenta IN ('Caja de Ahorro ARS', 'Caja de Ahorro USD')
              AND es_actual = 1
        """
    },
    {
        'tabla': 'fact_transacciones',
        'descripcion': 'Transacciones con monto cero (deben haberse descartado)',
        'sql': "SELECT COUNT(*) FROM fact_transacciones WHERE monto = 0"
    },
    {
        'tabla': 'fact_pagos',
        'descripcion': 'Pagos con monto negativo (deben haberse corregido)',
        'sql': "SELECT COUNT(*) FROM fact_pagos WHERE monto < 0"
    },
    {
        'tabla': 'fact_pagos',
        'descripcion': 'Pagos con entidad vacía (deben haberse rellenado)',
        'sql': "SELECT COUNT(*) FROM fact_pagos WHERE entidad IS NULL OR entidad = ''"
    },
    {
        'tabla': 'fact_transacciones',
        'descripcion': 'Transacciones con cuenta inexistente (integridad referencial)',
        'sql': """
            SELECT COUNT(*)
            FROM fact_transacciones ft
            LEFT JOIN dim_cuenta cu ON ft.id_cuenta_sk = cu.id_cuenta_sk
            WHERE cu.id_cuenta_sk IS NULL
        """
    },
    {
        'tabla': 'fact_plazos_fijos',
        'descripcion': 'Plazos fijos con monto negativo o cero',
        'sql': "SELECT COUNT(*) FROM fact_plazos_fijos WHERE monto <= 0"
    },
    {
        'tabla': 'fact_seguros',
        'descripcion': 'Seguros con prima negativa',
        'sql': "SELECT COUNT(*) FROM fact_seguros WHERE prima_mensual < 0"
    },
    {
        'tabla': 'fact_salarios_historial',
        'descripcion': 'Salarios negativos',
        'sql': "SELECT COUNT(*) FROM fact_salarios_historial WHERE salario < 0"
    },
    {
        'tabla': 'fact_evaluaciones',
        'descripcion': 'Puntajes fuera de rango',
        'sql': "SELECT COUNT(*) FROM fact_evaluaciones WHERE puntaje < 1 OR puntaje > 100"
    },
    
        {
        'tabla': 'dim_agente',
        'descripcion': 'Agentes sin sucursal asignada',
        'sql': "SELECT COUNT(*) FROM dim_agente WHERE id_sucursal_sk IS NULL"
    },
    {
        'tabla': 'dim_sla',
        'descripcion': 'SLA con tiempo objetivo negativo o cero',
        'sql': "SELECT COUNT(*) FROM dim_sla WHERE tiempo_objetivo_horas <= 0"
    },
    
    {
        'tabla': 'fact_oportunidades',
        'descripcion': 'Oportunidades con cliente inexistente',
        'sql': """
            SELECT COUNT(*)
            FROM fact_oportunidades fo
            LEFT JOIN dim_cliente cl ON fo.id_cliente_sk = cl.id_cliente_sk
            WHERE cl.id_cliente_sk IS NULL
        """
    },
]

def ejecutar_regla(conn, regla):
    cursor = conn.cursor()
    try:
        cursor.execute(regla['sql'])
        resultado = cursor.fetchone()
        cantidad = resultado[0] if resultado else 0
        estado = 'OK' if cantidad == 0 else 'PROBLEMA'
        logging.info(f"  [{estado}] {regla['descripcion']}: {cantidad} registro(s).")
        return cantidad
    except Exception as e:
        logging.error(f"  Error en regla '{regla['descripcion']}': {e}")
        return -1

def generar_reporte(conn, reglas, ruta_reporte, tipo):
    resultados = []
    total_problemas = 0
    for regla in reglas:
        cantidad = ejecutar_regla(conn, regla)
        if cantidad > 0:
            total_problemas += cantidad
        resultados.append({
            'tabla': regla['tabla'],
            'regla': regla['descripcion'],
            'problemas': cantidad,
            'estado': 'OK' if cantidad == 0 else 'PROBLEMA'
        })
    with open(ruta_reporte, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['tabla', 'regla', 'problemas', 'estado'])
        writer.writeheader()
        writer.writerows(resultados)
    logging.info(f"Reporte {tipo} guardado en {ruta_reporte}")
    return total_problemas

def main():
    RUTA_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    RUTA_DB = os.path.join(RUTA_BASE, 'data', 'andes_dw.db')
    RUTA_REPORTE_STG = os.path.join(RUTA_BASE, 'docs', 'reportes_calidad', 'calidad_staging.csv')
    RUTA_REPORTE_DW = os.path.join(RUTA_BASE, 'docs', 'reportes_calidad', 'calidad_dw_final.csv')
    os.makedirs(os.path.dirname(RUTA_REPORTE_STG), exist_ok=True)

    conn = sqlite3.connect(RUTA_DB)
    logging.info("=" * 60)
    logging.info("VALIDACIÓN DE STAGING (datos crudos)")
    logging.info("=" * 60)
    total_stg = generar_reporte(conn, REGLAS_STAGING, RUTA_REPORTE_STG, 'staging')
    logging.info(f"Total problemas en staging: {total_stg}")

    logging.info("=" * 60)
    logging.info("VALIDACIÓN DEL DATA WAREHOUSE FINAL (dim/fact)")
    logging.info("=" * 60)
    total_dw = generar_reporte(conn, REGLAS_DW, RUTA_REPORTE_DW, 'DW final')
    logging.info(f"Total problemas en DW final: {total_dw}")

    logging.info("=" * 60)
    logging.info("RESUMEN FINAL")
    logging.info("=" * 60)
    logging.info(f"Staging: {total_stg} problemas (esperados en crudos)")
    logging.info(f"Data Warehouse final: {total_dw} problemas (debe ser 0)")
    logging.info("=" * 60)
    conn.close()

if __name__ == '__main__':
    main()