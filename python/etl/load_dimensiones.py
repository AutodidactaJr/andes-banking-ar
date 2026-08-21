# 📄 Archivo: python/etl/load_dimensiones.py
# Carga dimensiones desde staging con SCD Tipo 2 y limpieza selectiva
# Incluye: dim_cliente, dim_cuenta, dim_sucursal, dim_tarjeta, dim_canal,
#          dim_producto, dim_tiempo, dim_campana, dim_empleado, dim_tipo_reclamo,
#          dim_tipo_riesgo, dim_cuenta_contable, dim_seguro, dim_agente, dim_sla

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

# ---------- DIMENSIÓN CLIENTE (SCD Tipo 2) ----------
def cargar_dim_cliente(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_cliente, MAX(tipo_doc) AS tipo_doc, MAX(num_doc) AS num_doc,
               MAX(nombre) AS nombre, MAX(apellido) AS apellido,
               MAX(email) AS email, MAX(telefono) AS telefono,
               MAX(fecha_nacimiento) AS fecha_nacimiento, MAX(direccion) AS direccion,
               MAX(ciudad) AS ciudad, MAX(provincia) AS provincia,
               MAX(segmento) AS segmento
        FROM stg_clientes
        GROUP BY id_cliente
    """)
    clientes = cursor.fetchall()
    for cli in clientes:
        id_cliente_nk = cli[0]
        nuevos_datos = {
            'tipo_doc': cli[1] or '',
            'num_doc': cli[2] or '',
            'nombre': cli[3] or '',
            'apellido': cli[4] or '',
            'email': cli[5] if cli[5] else 'no_email@andes.com.ar',
            'telefono': cli[6] if cli[6] else 'Sin teléfono',
            'fecha_nacimiento': cli[7] or '',
            'direccion': cli[8] or '',
            'ciudad': cli[9] or '',
            'provincia': cli[10] or '',
            'segmento': cli[11] or ''
        }
        cursor.execute("""
            SELECT id_cliente_sk, tipo_doc, num_doc, nombre, apellido, email,
                   telefono, fecha_nacimiento, direccion, ciudad, provincia, segmento
            FROM dim_cliente
            WHERE id_cliente_nk = ? AND es_actual = 1
        """, (id_cliente_nk,))
        actual = cursor.fetchone()
        if actual is None:
            cursor.execute("""
                INSERT INTO dim_cliente (id_cliente_nk, tipo_doc, num_doc, nombre, apellido, email,
                    telefono, fecha_nacimiento, direccion, ciudad, provincia, segmento,
                    fecha_inicio_vigencia, es_actual)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (id_cliente_nk, nuevos_datos['tipo_doc'], nuevos_datos['num_doc'],
                  nuevos_datos['nombre'], nuevos_datos['apellido'], nuevos_datos['email'],
                  nuevos_datos['telefono'], nuevos_datos['fecha_nacimiento'],
                  nuevos_datos['direccion'], nuevos_datos['ciudad'], nuevos_datos['provincia'],
                  nuevos_datos['segmento'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        else:
            datos_actuales = {
                'tipo_doc': actual[1] or '',
                'num_doc': actual[2] or '',
                'nombre': actual[3] or '',
                'apellido': actual[4] or '',
                'email': actual[5] or '',
                'telefono': actual[6] or '',
                'fecha_nacimiento': actual[7] or '',
                'direccion': actual[8] or '',
                'ciudad': actual[9] or '',
                'provincia': actual[10] or '',
                'segmento': actual[11] or ''
            }
            if datos_actuales != nuevos_datos:
                cursor.execute("""
                    UPDATE dim_cliente SET fecha_fin_vigencia = ?, es_actual = 0
                    WHERE id_cliente_sk = ?
                """, (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), actual[0]))
                cursor.execute("""
                    INSERT INTO dim_cliente (id_cliente_nk, tipo_doc, num_doc, nombre, apellido, email,
                        telefono, fecha_nacimiento, direccion, ciudad, provincia, segmento,
                        fecha_inicio_vigencia, es_actual)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                """, (id_cliente_nk, nuevos_datos['tipo_doc'], nuevos_datos['num_doc'],
                      nuevos_datos['nombre'], nuevos_datos['apellido'], nuevos_datos['email'],
                      nuevos_datos['telefono'], nuevos_datos['fecha_nacimiento'],
                      nuevos_datos['direccion'], nuevos_datos['ciudad'], nuevos_datos['provincia'],
                      nuevos_datos['segmento'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    logging.info("dim_cliente cargada.")

# ---------- DIMENSIÓN CUENTA (SCD Tipo 2 + corrección selectiva) ----------
def cargar_dim_cuenta(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_cuenta, id_cliente,
               MAX(tipo_cuenta) AS tipo_cuenta,
               MAX(moneda) AS moneda,
               CASE
                    WHEN MAX(tipo_cuenta) IN ('Caja de Ahorro ARS', 'Caja de Ahorro USD') AND MAX(saldo) < 0
                    THEN ABS(MAX(saldo))
                    ELSE MAX(saldo)
               END AS saldo,
               MAX(fecha_apertura) AS fecha_apertura,
               MAX(estado) AS estado,
               MAX(id_sucursal) AS id_sucursal
        FROM stg_cuentas
        GROUP BY id_cuenta, id_cliente
    """)
    cuentas = cursor.fetchall()
    for cue in cuentas:
        id_cuenta_nk = cue[0]
        id_cliente_nk = cue[1]
        nuevos_datos = {
            'tipo_cuenta': cue[2] or '',
            'moneda': cue[3] or '',
            'saldo': cue[4] if cue[4] is not None else 0,
            'fecha_apertura': cue[5] or '',
            'estado': cue[6] or '',
            'id_sucursal_nk': cue[7]
        }
        cursor.execute("SELECT id_cliente_sk FROM dim_cliente WHERE id_cliente_nk = ? AND es_actual = 1", (id_cliente_nk,))
        res_cli = cursor.fetchone()
        if not res_cli:
            continue
        id_cliente_sk = res_cli[0]

        id_sucursal_sk = None
        if nuevos_datos['id_sucursal_nk']:
            cursor.execute("SELECT id_sucursal_sk FROM dim_sucursal WHERE id_sucursal_nk = ?", (nuevos_datos['id_sucursal_nk'],))
            res_suc = cursor.fetchone()
            if res_suc:
                id_sucursal_sk = res_suc[0]

        cursor.execute("""
            SELECT id_cuenta_sk, tipo_cuenta, moneda, saldo, fecha_apertura, estado, id_sucursal_sk
            FROM dim_cuenta
            WHERE id_cuenta_nk = ? AND es_actual = 1
        """, (id_cuenta_nk,))
        actual = cursor.fetchone()
        if actual is None:
            # Insertar nueva fila actual con INSERT OR IGNORE para evitar UNIQUE constraint
            cursor.execute("""
                INSERT OR IGNORE INTO dim_cuenta (id_cuenta_nk, id_cliente_sk, id_sucursal_sk, tipo_cuenta,
                    moneda, saldo, fecha_apertura, estado, fecha_inicio_vigencia, es_actual)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (id_cuenta_nk, id_cliente_sk, id_sucursal_sk, nuevos_datos['tipo_cuenta'],
                  nuevos_datos['moneda'], nuevos_datos['saldo'], nuevos_datos['fecha_apertura'],
                  nuevos_datos['estado'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        else:
            datos_actuales = {
                'tipo_cuenta': actual[1] or '',
                'moneda': actual[2] or '',
                'saldo': actual[3] if actual[3] is not None else 0,
                'fecha_apertura': actual[4] or '',
                'estado': actual[5] or '',
                'id_sucursal_sk': actual[6]
            }
            nuevos_datos_para_comparar = {
                'tipo_cuenta': nuevos_datos['tipo_cuenta'],
                'moneda': nuevos_datos['moneda'],
                'saldo': nuevos_datos['saldo'],
                'fecha_apertura': nuevos_datos['fecha_apertura'],
                'estado': nuevos_datos['estado'],
                'id_sucursal_sk': id_sucursal_sk
            }
            if datos_actuales != nuevos_datos_para_comparar:
                # Cerrar fila actual
                cursor.execute("""
                    UPDATE dim_cuenta SET fecha_fin_vigencia = ?, es_actual = 0
                    WHERE id_cuenta_sk = ?
                """, (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), actual[0]))
                # Insertar nueva versión con INSERT OR IGNORE
                cursor.execute("""
                    INSERT OR IGNORE INTO dim_cuenta (id_cuenta_nk, id_cliente_sk, id_sucursal_sk, tipo_cuenta,
                        moneda, saldo, fecha_apertura, estado, fecha_inicio_vigencia, es_actual)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                """, (id_cuenta_nk, id_cliente_sk, id_sucursal_sk, nuevos_datos['tipo_cuenta'],
                      nuevos_datos['moneda'], nuevos_datos['saldo'], nuevos_datos['fecha_apertura'],
                      nuevos_datos['estado'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    logging.info("dim_cuenta cargada (corrección selectiva aplicada).")

# ---------- DIMENSIÓN SUCURSAL ----------
def cargar_dim_sucursal(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO dim_sucursal (id_sucursal_nk, nombre, direccion, ciudad, provincia, region, fecha_apertura)
        SELECT id_sucursal, nombre, direccion, ciudad, provincia, region,
               CASE WHEN fecha_apertura LIKE '%/%' THEN substr(fecha_apertura,7,4)||'-'||substr(fecha_apertura,4,2)||'-'||substr(fecha_apertura,1,2)
                    ELSE fecha_apertura END
        FROM stg_sucursales
    """)
    conn.commit()
    logging.info("dim_sucursal cargada.")

# ---------- DIMENSIÓN TARJETA ----------
def cargar_dim_tarjeta(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO dim_tarjeta (id_tarjeta_nk, id_cliente_sk, id_cuenta_sk, marca, tipo, numero, limite,
            fecha_emision, fecha_vencimiento, estado)
        SELECT t.id_tarjeta, cl.id_cliente_sk, cu.id_cuenta_sk, t.marca, t.tipo, t.numero,
               t.limite, t.fecha_emision, t.fecha_vencimiento, t.estado
        FROM stg_tarjetas t
        INNER JOIN dim_cliente cl ON t.id_cliente = cl.id_cliente_nk AND cl.es_actual = 1
        LEFT JOIN dim_cuenta cu ON t.id_cuenta = cu.id_cuenta_nk AND cu.es_actual = 1
        WHERE cl.id_cliente_sk IS NOT NULL
    """)
    conn.commit()
    logging.info("dim_tarjeta cargada.")

# ---------- DIMENSIÓN CANAL ----------
def cargar_dim_canal(conn):
    cursor = conn.cursor()
    canales = ['Home Banking', 'Mobile Banking', 'Sucursal', 'Cajero Automático', 'Call Center', 'Posnet', 'QR']
    for canal in canales:
        cursor.execute("INSERT OR IGNORE INTO dim_canal (canal_nombre) VALUES (?)", (canal,))
    conn.commit()
    logging.info("dim_canal cargada.")

# ---------- DIMENSIÓN PRODUCTO ----------
def cargar_dim_producto(conn):
    cursor = conn.cursor()
    productos = [
        ('Caja de Ahorro ARS', 'Cuentas'), ('Caja de Ahorro USD', 'Cuentas'),
        ('Cuenta Corriente', 'Cuentas'), ('Tarjeta de Débito', 'Tarjetas'),
        ('Tarjeta de Crédito', 'Tarjetas'), ('Préstamo Personal', 'Préstamos'),
        ('Préstamo Hipotecario', 'Préstamos'), ('Préstamo Prendario', 'Préstamos'),
        ('Plazo Fijo', 'Inversiones'), ('Seguro de Vida', 'Seguros'),
        ('Seguro contra Robo', 'Seguros'), ('Microcrédito', 'Préstamos'),
        ('Billetera Virtual', 'Pagos digitales')
    ]
    for nombre, categoria in productos:
        cursor.execute("INSERT OR IGNORE INTO dim_producto (producto_nombre, categoria) VALUES (?, ?)", (nombre, categoria))
    conn.commit()
    logging.info("dim_producto cargada.")

# ---------- DIMENSIÓN TIEMPO ----------
def cargar_dim_tiempo(conn):
    cursor = conn.cursor()
    start = datetime.date(2021, 1, 1)
    end = datetime.date(2023, 12, 31)
    delta = end - start
    dias = []
    for i in range(delta.days + 1):
        fecha = start + datetime.timedelta(days=i)
        dias.append((fecha.strftime('%Y-%m-%d'), fecha.year, fecha.month, fecha.day,
                     fecha.strftime('%B'), fecha.strftime('%A')))
    cursor.executemany("""
        INSERT OR IGNORE INTO dim_tiempo (fecha, anio, mes, dia, nombre_mes, nombre_dia_semana)
        VALUES (?, ?, ?, ?, ?, ?)
    """, dias)
    conn.commit()
    logging.info(f"dim_tiempo cargada con {len(dias)} días.")

# ---------- DIMENSIÓN CAMPAÑA ----------
def cargar_dim_campana(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO dim_campana (id_campana_nk, nombre, canal, segmento_objetivo, fecha_inicio, fecha_fin, costo)
        SELECT id_campana, nombre, canal, segmento_objetivo, fecha_inicio, fecha_fin, costo
        FROM stg_campanas
    """)
    conn.commit()
    logging.info("dim_campana cargada.")

# ---------- DIMENSIÓN EMPLEADO ----------
def cargar_dim_empleado(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO dim_empleado (id_empleado_nk, nombre, apellido, cargo, id_sucursal_sk, fecha_contratacion, salario)
        SELECT e.id_empleado, e.nombre, e.apellido, e.cargo, s.id_sucursal_sk, e.fecha_contratacion, e.salario
        FROM stg_empleados e
        LEFT JOIN dim_sucursal s ON e.id_sucursal = s.id_sucursal_nk
        WHERE e.id_empleado IS NOT NULL
    """)
    conn.commit()
    logging.info("dim_empleado cargada.")

# ---------- DIMENSIÓN TIPO RECLAMO ----------
def cargar_dim_tipo_reclamo(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO dim_tipo_reclamo (tipo_reclamo_nombre)
        SELECT DISTINCT tipo_reclamo FROM stg_tickets WHERE tipo_reclamo IS NOT NULL
    """)
    conn.commit()
    logging.info("dim_tipo_reclamo cargada.")

# ---------- DIMENSIÓN TIPO RIESGO ----------
def cargar_dim_tipo_riesgo(conn):
    cursor = conn.cursor()
    tipos_riesgo = ['Movimiento inusual', 'Login sospechoso', 'Cambio de datos', 'Phishing']
    for tipo in tipos_riesgo:
        cursor.execute("INSERT OR IGNORE INTO dim_tipo_riesgo (tipo_riesgo_nombre) VALUES (?)", (tipo,))
    conn.commit()
    logging.info("dim_tipo_riesgo cargada.")

# ---------- DIMENSIÓN CUENTA CONTABLE ----------
def cargar_dim_cuenta_contable(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO dim_cuenta_contable (codigo_cuenta, descripcion, tipo_cuenta)
        SELECT codigo_cuenta, descripcion, tipo_cuenta
        FROM stg_cuentas_contables
    """)
    conn.commit()
    logging.info("dim_cuenta_contable cargada.")

# ---------- DIMENSIÓN SEGURO ----------
def cargar_dim_seguro(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO dim_seguro (id_seguro_nk, tipo_seguro)
        SELECT id_seguro, tipo_seguro FROM stg_seguros
    """)
    conn.commit()
    logging.info("dim_seguro cargada.")

# ---------- DIMENSIÓN AGENTE ----------
def cargar_dim_agente(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO dim_agente (id_agente_nk, nombre, apellido, id_sucursal_sk)
        SELECT a.id_agente, a.nombre, a.apellido, s.id_sucursal_sk
        FROM stg_agentes a
        LEFT JOIN dim_sucursal s ON a.id_sucursal = s.id_sucursal_nk
    """)
    conn.commit()
    logging.info("dim_agente cargada.")

# ---------- DIMENSIÓN SLA ----------
def cargar_dim_sla(conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO dim_sla (id_sla_nk, tipo_reclamo, tiempo_objetivo_horas)
        SELECT id_sla, tipo_reclamo, tiempo_objetivo_horas FROM stg_sla_tickets
    """)
    conn.commit()
    logging.info("dim_sla cargada.")

# ---------- MAIN ----------
def main():
    RUTA_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    RUTA_DB = os.path.join(RUTA_BASE, 'data', 'andes_dw.db')
    conn = sqlite3.connect(RUTA_DB)
    conn.execute("PRAGMA foreign_keys = OFF")
    script_name = 'load_dimensiones.py'
    registrar_log(conn, script_name, 0, 'INICIO')
    try:
        logging.info("Cargando dimensiones...")
        cargar_dim_cliente(conn)
        cargar_dim_sucursal(conn)
        cargar_dim_cuenta(conn)
        cargar_dim_tarjeta(conn)
        cargar_dim_canal(conn)
        cargar_dim_producto(conn)
        cargar_dim_tiempo(conn)
        cargar_dim_campana(conn)
        cargar_dim_empleado(conn)
        cargar_dim_tipo_reclamo(conn)
        cargar_dim_tipo_riesgo(conn)
        cargar_dim_cuenta_contable(conn)
        cargar_dim_seguro(conn)
        cargar_dim_agente(conn)
        cargar_dim_sla(conn)
        total = conn.execute("SELECT COUNT(*) FROM dim_cliente WHERE es_actual=1").fetchone()[0]
        registrar_log(conn, script_name, total, 'EXITO', 'Todas las dimensiones cargadas')
    except Exception as e:
        conn.rollback()
        registrar_log(conn, script_name, 0, 'ERROR', str(e))
        logging.error(f"Error: {e}")
    finally:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.close()

if __name__ == '__main__':
    main()