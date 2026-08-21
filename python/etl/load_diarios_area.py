# 📄 Archivo: python/etl/load_diarios_area.py
# Carga archivos CSV diarios de todas las áreas a sus bases de datos

import csv
import sqlite3
import os
import glob
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def insertar_csv(ruta_csv, ruta_db, tabla, columnas):
    if not os.path.exists(ruta_csv):
        return 0
    conn = sqlite3.connect(ruta_db)
    cur = conn.cursor()
    filas = 0
    with open(ruta_csv, 'r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        placeholders = ','.join(['?'] * len(columnas))
        sql = f"INSERT OR IGNORE INTO {tabla} ({','.join(columnas)}) VALUES ({placeholders})"
        for fila in lector:
            valores = []
            for col in columnas:
                v = fila.get(col, '')
                if v == '':
                    v = None
                # Conversión de tipos numéricos
                if col.startswith('id_') or col in ['id_cliente', 'id_cuenta', 'id_campana', 'score', 'dias', 'satisfaccion', 'duracion_seg', 'dias_mora']:
                    try:
                        v = int(v) if v is not None else None
                    except (ValueError, TypeError):
                        v = None
                if col in ['monto', 'deuda_pendiente', 'salario', 'costo', 'limite', 'saldo', 'tasa_interes', 'cuota', 'saldo_pendiente', 'monto_debe', 'monto_haber', 'monto_presupuestado']:
                    try:
                        v = float(v) if v is not None else None
                    except (ValueError, TypeError):
                        v = None
                valores.append(v)
            try:
                cur.execute(sql, valores)
                filas += 1
            except Exception as e:
                logging.error(f"Error en fila: {e}")
    conn.commit()
    conn.close()
    if filas > 0:
        logging.info(f"{tabla}: {filas} insertados desde {os.path.basename(ruta_csv)}")
    return filas

def cargar_area(area, ruta_area_db, mapeo, data_raw):
    """Recorre archivos diarios en el área y los inserta en la base de datos correspondiente."""
    total = 0
    for subcarpeta, tabla, columnas in mapeo:
        ruta_entidad = os.path.join(data_raw, area, subcarpeta)
        if not os.path.exists(ruta_entidad):
            continue
        patron = os.path.join(ruta_entidad, f"{subcarpeta}_*.csv")
        archivos = glob.glob(patron)
        archivos.sort()  # cronológico
        for archivo in archivos:
            total += insertar_csv(archivo, ruta_area_db, tabla, columnas)
    return total

def main():
    RUTA_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_raw = os.path.join(RUTA_BASE, 'data', 'raw')
    data_dbs = os.path.join(RUTA_BASE, 'data', 'databases')

    areas = {
        'core_bancario': {
            'db': os.path.join(data_dbs, 'core_bancario.db'),
            'mapeo': [
                ('clientes', 'clientes', ['id_cliente','tipo_doc','num_doc','nombre','apellido','email','telefono','fecha_nacimiento','direccion','ciudad','provincia','segmento']),
                ('transacciones', 'transacciones', ['id_transaccion','id_cuenta','tipo_transaccion','monto','moneda','fecha','canal','estado','referencia']),
                ('pagos', 'pagos', ['id_pago','id_cuenta','entidad','tipo_pago','monto','fecha','canal','estado','referencia'])
            ]
        },
        'crm': {
            'db': os.path.join(data_dbs, 'crm.db'),
            'mapeo': [
                ('interacciones', 'interacciones', ['id_interaccion','id_campana','id_cliente','fecha','tipo_interaccion','dispositivo']),
                ('leads', 'leads', ['id_lead','id_campana','id_cliente','fecha_creacion','estado','producto_interes']),
                ('campanas', 'campanas', ['id_campana','nombre','canal','segmento_objetivo','fecha_inicio','fecha_fin','costo'])
            ]
        },
        'riesgos': {
            'db': os.path.join(data_dbs, 'riesgos.db'),
            'mapeo': [
                ('alertas_fraude', 'alertas_fraude', ['id_alerta','id_cliente','id_cuenta','tipo_alerta','monto','estado','fecha_deteccion']),
                ('incidentes', 'incidentes', ['id_incidente','id_cliente','descripcion','severidad','estado','fecha_incidente']),
                ('scoring_crediticio', 'scoring_crediticio', ['id_scoring','id_cliente','score','riesgo','fecha_calculo']),
                ('morosidad', 'morosidad', ['id_morosidad','id_cliente','dias_mora','deuda_pendiente','fecha_reporte'])
            ]
        },
        'atencion_cliente': {
            'db': os.path.join(data_dbs, 'atencion_cliente.db'),
            'mapeo': [
                ('tickets', 'tickets', ['id_ticket','id_cliente','tipo_reclamo','descripcion','estado','fecha_creacion','fecha_resolucion']),
                ('llamadas', 'llamadas', ['id_llamada','id_cliente','duracion_seg','resultado','fecha_llamada']),
                ('encuestas', 'encuestas', ['id_encuesta','id_cliente','satisfaccion','comentario','fecha_encuesta'])
            ]
        },
        'rrhh': {
            'db': os.path.join(data_dbs, 'rrhh.db'),
            'mapeo': [
                ('ausencias', 'ausencias', ['id_ausencia','id_empleado','tipo_ausencia','dias','fecha_inicio','fecha_fin']),
                ('empleados', 'empleados', ['id_empleado','nombre','apellido','cargo','id_sucursal','fecha_contratacion','salario'])
            ]
        },
        'contabilidad': {
            'db': os.path.join(data_dbs, 'contabilidad.db'),
            'mapeo': [
                ('asientos_contables', 'asientos_contables', ['id_asiento','id_cuenta_contable','fecha_contable','tipo_asiento','monto_debe','monto_haber','descripcion']),
                ('presupuesto', 'presupuesto', ['id_presupuesto','id_cuenta_contable','monto_presupuestado','fecha_presupuesto'])
            ]
        }
    }

    total_general = 0
    for area, config_area in areas.items():
        total_general += cargar_area(area, config_area['db'], config_area['mapeo'], data_raw)
    logging.info(f"Total de registros insertados en todas las áreas: {total_general}")

if __name__ == '__main__':
    main()