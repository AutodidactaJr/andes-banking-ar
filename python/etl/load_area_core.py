# 📄 Archivo: python/etl/load_area_core.py
# Carga los CSV del core bancario desde subcarpetas a core_bancario.db

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
                if col.startswith('id_') or col in ['id_cliente', 'id_cuenta', 'id_tarjeta', 'id_sucursal', 'id_prestamo', 'id_transaccion', 'id_pago', 'id_plazo_fijo', 'id_seguro']:
                    try:
                        v = int(v) if v is not None else None
                    except (ValueError, TypeError):
                        v = None
                if col in ['saldo', 'limite', 'monto', 'tasa_interes', 'cuota', 'saldo_pendiente', 'prima_mensual']:
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
    RUTA_RAW_CORE = os.path.join(RUTA_BASE, 'data', 'raw', 'core_bancario')
    RUTA_DB = os.path.join(RUTA_BASE, 'data', 'databases', 'core_bancario.db')

    os.makedirs(os.path.dirname(RUTA_DB), exist_ok=True)

    # Crear tablas desde esquema SQL
    conn = sqlite3.connect(RUTA_DB)
    with open(os.path.join(RUTA_BASE, 'sql', 'esquemas_area', 'core_bancario.sql'), 'r') as f:
        conn.executescript(f.read())
    conn.close()

    # Cargar CSVs
    cargar_csv(os.path.join(RUTA_RAW_CORE, 'clientes', 'clientes.csv'), RUTA_DB, 'clientes',
               ['id_cliente','tipo_doc','num_doc','nombre','apellido','email','telefono','fecha_nacimiento','direccion','ciudad','provincia','segmento'])
    cargar_csv(os.path.join(RUTA_RAW_CORE, 'sucursales', 'sucursales.csv'), RUTA_DB, 'sucursales',
               ['id_sucursal','nombre','direccion','ciudad','provincia','region','fecha_apertura'])
    cargar_csv(os.path.join(RUTA_RAW_CORE, 'cuentas', 'cuentas.csv'), RUTA_DB, 'cuentas',
               ['id_cuenta','id_cliente','tipo_cuenta','moneda','saldo','fecha_apertura','estado','id_sucursal'])
    cargar_csv(os.path.join(RUTA_RAW_CORE, 'tarjetas', 'tarjetas.csv'), RUTA_DB, 'tarjetas',
               ['id_tarjeta','id_cliente','id_cuenta','marca','tipo','numero','limite','fecha_emision','fecha_vencimiento','estado'])
    cargar_csv(os.path.join(RUTA_RAW_CORE, 'prestamos', 'prestamos.csv'), RUTA_DB, 'prestamos',
               ['id_prestamo','id_cliente','tipo','monto','tasa_interes','plazo_meses','cuota','fecha_desembolso','saldo_pendiente','estado'])
    cargar_csv(os.path.join(RUTA_RAW_CORE, 'transacciones', 'transacciones.csv'), RUTA_DB, 'transacciones',
               ['id_transaccion','id_cuenta','tipo_transaccion','monto','moneda','fecha','canal','estado','referencia'])
    cargar_csv(os.path.join(RUTA_RAW_CORE, 'pagos', 'pagos.csv'), RUTA_DB, 'pagos',
               ['id_pago','id_cuenta','entidad','tipo_pago','monto','fecha','canal','estado','referencia'])
    # Nuevas tablas
    cargar_csv(os.path.join(RUTA_RAW_CORE, 'plazos_fijos', 'plazos_fijos.csv'), RUTA_DB, 'plazos_fijos',
               ['id_plazo_fijo','id_cliente','monto','tasa_interes','fecha_constitucion','fecha_vencimiento','estado'])
    cargar_csv(os.path.join(RUTA_RAW_CORE, 'seguros', 'seguros.csv'), RUTA_DB, 'seguros',
               ['id_seguro','id_cliente','tipo_seguro','prima_mensual','fecha_contratacion','estado'])

if __name__ == '__main__':
    main()