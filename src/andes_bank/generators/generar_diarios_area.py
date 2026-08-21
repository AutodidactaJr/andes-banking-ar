# 📄 Archivo: src/andes_bank/generators/generar_diarios_area.py
# Generador diario incremental para todas las áreas del banco

import argparse
import datetime
import os
import random
import sqlite3
from . import config, utils

# ============================================================
# 1. FUNCIONES DE ARCHIVOS DE CONTROL (últimos IDs)
# ============================================================

def leer_ultimo_id(archivo_control, default=0):
    """Lee el último ID desde un archivo de control. Si no existe, devuelve default."""
    if not os.path.exists(archivo_control):
        return default
    with open(archivo_control, 'r', encoding='utf-8') as f:
        contenido = f.read().strip()
        return int(contenido) if contenido.isdigit() else default

def escribir_ultimo_id(archivo_control, valor):
    """Escribe el último ID en un archivo de control, creando carpeta si hace falta."""
    os.makedirs(os.path.dirname(archivo_control), exist_ok=True)
    with open(archivo_control, 'w', encoding='utf-8') as f:
        f.write(str(valor))

def get_control_dir():
    """Devuelve la ruta a la carpeta data/control."""
    return os.path.join(config.BASE_DIR, 'data', 'control')


# ============================================================
# 2. FUNCIONES GENERADORAS POR ENTIDAD
# ============================================================

def generar_clientes(fecha_str, ultimo_id, cantidad):
    """Genera clientes con IDs consecutivos a partir de ultimo_id."""
    random.seed(int(fecha_str.replace('_', '')))
    clientes = []
    nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Lucía', 'Pedro', 'Sofía', 'Jorge', 'Valentina']
    apellidos = ['García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez', 'Pérez', 'Gómez', 'Díaz', 'Sosa']
    provincias = list(config.PROVINCIAS.keys())
    for i in range(cantidad):
        id_cliente = ultimo_id + i + 1
        tipo_doc = 'DNI' if random.random() < 0.8 else 'CUIT'
        if tipo_doc == 'DNI':
            num_doc = utils.random_dni()
            fecha_nac = utils.random_date('1950-01-01', '2005-12-31')
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            segmento = random.choice(['Clásico', 'Premium', 'Joven', 'Jubilado'])
        else:
            num_doc = utils.random_cuit()
            fecha_nac = ''
            nombre = f"Empresa {random.randint(1, 1000)} SRL"
            apellido = ''
            segmento = random.choice(['PyME', 'Corporativo'])
        email = f"{nombre.lower()}.{apellido.lower()}.{id_cliente}@mail.com" if apellido else f"contacto{id_cliente}@mail.com"
        telefono = '261' + ''.join([str(random.randint(0,9)) for _ in range(7)])
        provincia = random.choice(provincias)
        ciudad = random.choice(config.PROVINCIAS[provincia])
        cliente = {
            'id_cliente': id_cliente,
            'tipo_doc': tipo_doc,
            'num_doc': num_doc,
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nac,
            'direccion': f"Calle {random.randint(1,2000)} N°{random.randint(100,999)}",
            'ciudad': ciudad,
            'provincia': provincia,
            'segmento': segmento
        }
        clientes.append(cliente)
    return clientes, ultimo_id + cantidad

def generar_transacciones(fecha_str, ultimo_id, ids_cuentas, cantidad):
    """Genera transacciones con fecha del día e IDs consecutivos."""
    random.seed(int(fecha_str.replace('_', '')) + 1)
    transacciones = []
    tipos = ['Depósito', 'Retiro', 'Transferencia enviada', 'Transferencia recibida', 'Consumo débito']
    canales = config.CANALES if hasattr(config, 'CANALES') else ['Home Banking', 'Mobile Banking', 'Sucursal', 'Cajero Automático', 'Posnet']
    for i in range(cantidad):
        id_transaccion = ultimo_id + i + 1
        id_cuenta = random.choice(ids_cuentas) if ids_cuentas else random.randint(1, 8000)
        tipo = random.choice(tipos)
        signo = 1 if tipo in ['Depósito', 'Transferencia recibida'] else -1
        monto = round(random.uniform(100, 500000) * signo, 2)
        fecha = f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]} {random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"
        canal = random.choice(canales)
        estado = 'Completada' if random.random() < 0.97 else 'Rechazada'
        transaccion = {
            'id_transaccion': id_transaccion,
            'id_cuenta': id_cuenta,
            'tipo_transaccion': tipo,
            'monto': monto,
            'moneda': 'ARS',
            'fecha': fecha,
            'canal': canal,
            'estado': estado,
            'referencia': f"TRX-{id_transaccion:06d}"
        }
        transacciones.append(transaccion)
    return transacciones, ultimo_id + cantidad

def generar_interacciones(fecha_str, ultimo_id, ids_clientes, ids_campanas, cantidad):
    """Genera interacciones de campañas para una fecha."""
    random.seed(int(fecha_str.replace('_', '')) + 2)
    interacciones = []
    for i in range(cantidad):
        interaccion = {
            'id_interaccion': ultimo_id + i + 1,
            'id_campana': random.choice(ids_campanas) if ids_campanas else random.randint(1, config.NUM_CAMPANAS),
            'id_cliente': random.choice(ids_clientes),
            'fecha': utils.random_datetime(f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}", f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}"),
            'tipo_interaccion': random.choice(config.TIPOS_INTERACCION),
            'dispositivo': random.choice(config.DISPOSITIVOS)
        }
        interacciones.append(interaccion)
    return interacciones, ultimo_id + cantidad

def generar_leads(fecha_str, ultimo_id, ids_clientes, ids_campanas, cantidad):
    """Genera leads para una fecha."""
    random.seed(int(fecha_str.replace('_', '')) + 3)
    leads = []
    for i in range(cantidad):
        lead = {
            'id_lead': ultimo_id + i + 1,
            'id_campana': random.choice(ids_campanas) if ids_campanas else random.randint(1, config.NUM_CAMPANAS),
            'id_cliente': random.choice(ids_clientes) if random.random() < 0.7 else '',
            'fecha_creacion': utils.random_date(f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}", f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}"),
            'estado': random.choice(config.ESTADOS_LEAD),
            'producto_interes': random.choice(config.PRODUCTOS_INTERES)
        }
        leads.append(lead)
    return leads, ultimo_id + cantidad

def generar_alertas(fecha_str, ultimo_id, ids_clientes, ids_cuentas, cantidad):
    """Genera alertas de fraude para una fecha."""
    random.seed(int(fecha_str.replace('_', '')) + 4)
    alertas = []
    for i in range(cantidad):
        alerta = {
            'id_alerta': ultimo_id + i + 1,
            'id_cliente': random.choice(ids_clientes),
            'id_cuenta': random.choice(ids_cuentas) if ids_cuentas else None,
            'tipo_alerta': random.choice(['Movimiento inusual', 'Login sospechoso', 'Cambio de datos', 'Phishing']),
            'monto': round(random.uniform(1000, 500000), 2),
            'estado': random.choice(['Pendiente', 'Investigada', 'Resuelta', 'Falsa']),
            'fecha_deteccion': utils.random_datetime(f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}", f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}")
        }
        alertas.append(alerta)
    return alertas, ultimo_id + cantidad

def generar_tickets(fecha_str, ultimo_id, ids_clientes, cantidad):
    """Genera tickets de atención al cliente."""
    random.seed(int(fecha_str.replace('_', '')) + 5)
    tickets = []
    for i in range(cantidad):
        estado = random.choice(['Abierto', 'En proceso', 'Cerrado'])
        fecha_creacion = utils.random_datetime(f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}", f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}")
        fecha_resolucion = utils.random_datetime(f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}", f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}") if estado == 'Cerrado' else ''
        ticket = {
            'id_ticket': ultimo_id + i + 1,
            'id_cliente': random.choice(ids_clientes),
            'tipo_reclamo': random.choice(['Reclamo', 'Consulta', 'Sugerencia', 'Error']),
            'descripcion': f"Ticket {ultimo_id + i + 1}",
            'estado': estado,
            'fecha_creacion': fecha_creacion,
            'fecha_resolucion': fecha_resolucion
        }
        tickets.append(ticket)
    return tickets, ultimo_id + cantidad

def generar_llamadas(fecha_str, ultimo_id, ids_clientes, cantidad):
    """Genera llamadas de call center."""
    random.seed(int(fecha_str.replace('_', '')) + 6)
    llamadas = []
    for i in range(cantidad):
        llamada = {
            'id_llamada': ultimo_id + i + 1,
            'id_cliente': random.choice(ids_clientes),
            'duracion_seg': random.randint(30, 1800),
            'resultado': random.choice(['Resuelto', 'No resuelto', 'Transferido']),
            'fecha_llamada': utils.random_datetime(f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}", f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}")
        }
        llamadas.append(llamada)
    return llamadas, ultimo_id + cantidad

def generar_encuestas(fecha_str, ultimo_id, ids_clientes, cantidad):
    """Genera encuestas de satisfacción."""
    random.seed(int(fecha_str.replace('_', '')) + 7)
    encuestas = []
    for i in range(cantidad):
        encuesta = {
            'id_encuesta': ultimo_id + i + 1,
            'id_cliente': random.choice(ids_clientes),
            'satisfaccion': random.randint(1, 5),
            'comentario': random.choice(['Excelente', 'Bueno', 'Regular', 'Malo']),
            'fecha_encuesta': utils.random_date(f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}", f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}")
        }
        encuestas.append(encuesta)
    return encuestas, ultimo_id + cantidad

def generar_ausencias(fecha_str, ultimo_id, ids_empleados, cantidad):
    """Genera ausencias de empleados."""
    random.seed(int(fecha_str.replace('_', '')) + 8)
    ausencias = []
    for i in range(cantidad):
        ausencia = {
            'id_ausencia': ultimo_id + i + 1,
            'id_empleado': random.choice(ids_empleados) if ids_empleados else random.randint(1, config.NUM_EMPLEADOS),
            'tipo_ausencia': random.choice(['Enfermedad', 'Vacaciones', 'Permiso', 'Otro']),
            'dias': random.randint(1, 15),
            'fecha_inicio': utils.random_date(f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}", f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}"),
            'fecha_fin': utils.random_date(f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}", f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}")
        }
        ausencias.append(ausencia)
    return ausencias, ultimo_id + cantidad

def generar_asientos(fecha_str, ultimo_id, ids_cuentas_contables, cantidad):
    """Genera asientos contables."""
    random.seed(int(fecha_str.replace('_', '')) + 9)
    asientos = []
    for i in range(cantidad):
        asiento = {
            'id_asiento': ultimo_id + i + 1,
            'id_cuenta_contable': random.choice(ids_cuentas_contables) if ids_cuentas_contables else random.randint(1, 7),
            'fecha_contable': utils.random_date(f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}", f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]}"),
            'tipo_asiento': random.choice(['Debe', 'Haber']),
            'monto_debe': round(random.uniform(1000, 500000), 2),
            'monto_haber': round(random.uniform(1000, 500000), 2),
            'descripcion': f'Asiento {ultimo_id + i + 1}'
        }
        asientos.append(asiento)
    return asientos, ultimo_id + cantidad


# ============================================================
# 3. FUNCIÓN PARA GUARDAR CSV EN SUBCARPETA
# ============================================================

def guardar_csv(area, entidad, fecha_str, fieldnames, datos):
    """Guarda los datos en data/raw/<area>/<entidad>/<entidad>_<fecha_str>.csv"""
    carpeta = os.path.join(config.RAW_DIR, area, entidad)
    os.makedirs(carpeta, exist_ok=True)
    archivo = os.path.join(carpeta, f'{entidad}_{fecha_str}.csv')
    utils.write_csv(archivo, fieldnames, datos)
    print(f"Generado: {archivo}")


# ============================================================
# 4. FUNCIÓN PRINCIPAL POR ÁREA
# ============================================================

def generar_area(fecha, area):
    """Genera los archivos diarios correspondientes a un área para una fecha dada."""
    fecha_str = fecha.strftime('%Y_%m_%d')
    fecha_iso = fecha.strftime('%Y-%m-%d')
    control_dir = get_control_dir()

    # --------------------------------------------------------
    # Carga de IDs de referencia desde bases de datos existentes
    # --------------------------------------------------------
    ids_clientes = []
    ids_cuentas = []
    ids_sucursales = []
    ids_campanas = []
    ids_empleados = []
    ids_cuentas_contables = []

    # Core Bancario
    ruta_core_db = os.path.join(config.BASE_DIR, 'data', 'databases', 'core_bancario.db')
    if os.path.exists(ruta_core_db):
        conn = sqlite3.connect(ruta_core_db)
        cur = conn.cursor()
        cur.execute("SELECT id_cliente FROM clientes")
        ids_clientes = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT id_cuenta FROM cuentas")
        ids_cuentas = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT id_sucursal FROM sucursales")
        ids_sucursales = [row[0] for row in cur.fetchall()]
        conn.close()

    # CRM
    ruta_crm_db = os.path.join(config.BASE_DIR, 'data', 'databases', 'crm.db')
    if os.path.exists(ruta_crm_db):
        conn = sqlite3.connect(ruta_crm_db)
        cur = conn.cursor()
        cur.execute("SELECT id_campana FROM campanas")
        ids_campanas = [row[0] for row in cur.fetchall()]
        conn.close()

    # RRHH
    ruta_rrhh_db = os.path.join(config.BASE_DIR, 'data', 'databases', 'rrhh.db')
    if os.path.exists(ruta_rrhh_db):
        conn = sqlite3.connect(ruta_rrhh_db)
        cur = conn.cursor()
        cur.execute("SELECT id_empleado FROM empleados")
        ids_empleados = [row[0] for row in cur.fetchall()]
        conn.close()

    # Contabilidad
    ruta_contab_db = os.path.join(config.BASE_DIR, 'data', 'databases', 'contabilidad.db')
    if os.path.exists(ruta_contab_db):
        conn = sqlite3.connect(ruta_contab_db)
        cur = conn.cursor()
        cur.execute("SELECT id_cuenta_contable FROM cuentas_contables")
        ids_cuentas_contables = [row[0] for row in cur.fetchall()]
        conn.close()

    # Fallbacks si no hay datos
    if not ids_clientes:
        ids_clientes = list(range(1, 5001))
    if not ids_cuentas:
        ids_cuentas = list(range(1, 8001))
    if not ids_sucursales:
        ids_sucursales = list(range(1, config.NUM_SUCURSALES + 1))
    if not ids_campanas:
        ids_campanas = list(range(1, config.NUM_CAMPANAS + 1))
    if not ids_empleados:
        ids_empleados = list(range(1, config.NUM_EMPLEADOS + 1))
    if not ids_cuentas_contables:
        ids_cuentas_contables = list(range(1, 8))

    # ========================================================
    # 4.1 CORE BANCARIO
    # ========================================================
    if area == 'core':
        # Clientes diarios
        ultimo_cliente = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_cliente.txt'), max(ids_clientes) if ids_clientes else 0)
        clientes, nuevo_id = generar_clientes(fecha_str, ultimo_cliente, 50)
        guardar_csv('core_bancario', 'clientes', fecha_str,
                    ['id_cliente','tipo_doc','num_doc','nombre','apellido','email','telefono','fecha_nacimiento','direccion','ciudad','provincia','segmento'],
                    clientes)
        escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_cliente.txt'), nuevo_id)

        # Transacciones diarias
        ultimo_trans = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_transaccion.txt'), 50000)
        transacciones, nuevo_id = generar_transacciones(fecha_str, ultimo_trans, ids_cuentas, 1000)
        guardar_csv('core_bancario', 'transacciones', fecha_str,
                    ['id_transaccion','id_cuenta','tipo_transaccion','monto','moneda','fecha','canal','estado','referencia'],
                    transacciones)
        escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_transaccion.txt'), nuevo_id)

        # Pagos diarios
        ultimo_pago = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_pago.txt'), 20000)
        pagos = []
        for i in range(20):
            pagos.append({
                'id_pago': ultimo_pago + i + 1,
                'id_cuenta': random.choice(ids_cuentas),
                'entidad': random.choice(['Edesur', 'Metrogas', 'Telecom', 'Visa', 'Mastercard']),
                'tipo_pago': random.choice(['Servicio', 'Tarjeta de crédito', 'Cuota de préstamo']),
                'monto': round(random.uniform(500, 50000), 2),
                'fecha': utils.random_datetime(fecha_iso, fecha_iso),
                'canal': random.choice(['Home Banking', 'Mobile Banking', 'Sucursal']),
                'estado': 'Exitoso' if random.random() < 0.98 else 'Fallido',
                'referencia': f"PAGO-{ultimo_pago + i + 1:06d}"
            })
        guardar_csv('core_bancario', 'pagos', fecha_str,
                    ['id_pago','id_cuenta','entidad','tipo_pago','monto','fecha','canal','estado','referencia'],
                    pagos)
        escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_pago.txt'), ultimo_pago + 20)

    # ========================================================
    # 4.2 CRM
    # ========================================================
    elif area == 'crm':
        # Interacciones diarias
        ultimo_int = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_interaccion.txt'), 20000)
        interacciones, nuevo_id = generar_interacciones(fecha_str, ultimo_int, ids_clientes, ids_campanas, 200)
        guardar_csv('crm', 'interacciones', fecha_str,
                    ['id_interaccion','id_campana','id_cliente','fecha','tipo_interaccion','dispositivo'],
                    interacciones)
        escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_interaccion.txt'), nuevo_id)

        # Leads diarios
        ultimo_lead = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_lead.txt'), 2000)
        leads, nuevo_id = generar_leads(fecha_str, ultimo_lead, ids_clientes, ids_campanas, 20)
        guardar_csv('crm', 'leads', fecha_str,
                    ['id_lead','id_campana','id_cliente','fecha_creacion','estado','producto_interes'],
                    leads)
        escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_lead.txt'), nuevo_id)

        # Campañas bajo demanda (10%)
        if random.random() < 0.10:
            ultimo_camp = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_campana.txt'), config.NUM_CAMPANAS)
            campana = {
                'id_campana': ultimo_camp + 1,
                'nombre': f"Campaña lanzada {fecha_iso}",
                'canal': random.choice(config.CANALES_CAMPANA),
                'segmento_objetivo': random.choice(config.SEGMENTOS_OBJETIVO),
                'fecha_inicio': fecha_iso,
                'fecha_fin': utils.random_date(fecha_iso, '2026-12-31'),
                'costo': round(random.uniform(10000, 500000), 2)
            }
            guardar_csv('crm', 'campanas', fecha_str,
                        ['id_campana','nombre','canal','segmento_objetivo','fecha_inicio','fecha_fin','costo'],
                        [campana])
            escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_campana.txt'), ultimo_camp + 1)

    # ========================================================
    # 4.3 RIESGOS
    # ========================================================
    elif area == 'riesgos':
        # Alertas de fraude diarias
        ultimo_alerta = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_alerta.txt'), 300)
        alertas, nuevo_id = generar_alertas(fecha_str, ultimo_alerta, ids_clientes, ids_cuentas, 5)
        guardar_csv('riesgos', 'alertas_fraude', fecha_str,
                    ['id_alerta','id_cliente','id_cuenta','tipo_alerta','monto','estado','fecha_deteccion'],
                    alertas)
        escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_alerta.txt'), nuevo_id)

        # Incidentes bajo demanda (5%)
        if random.random() < 0.05:
            ultimo_inc = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_incidente.txt'), 150)
            incidente = {
                'id_incidente': ultimo_inc + 1,
                'id_cliente': random.choice(ids_clientes),
                'descripcion': random.choice(['Fraude confirmado', 'Error de sistema', 'Fuga de datos', 'Acceso no autorizado']),
                'severidad': random.choice(['Baja', 'Media', 'Alta', 'Crítica']),
                'estado': 'Abierto',
                'fecha_incidente': utils.random_datetime(fecha_iso, fecha_iso)
            }
            guardar_csv('riesgos', 'incidentes', fecha_str,
                        ['id_incidente','id_cliente','descripcion','severidad','estado','fecha_incidente'],
                        [incidente])
            escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_incidente.txt'), ultimo_inc + 1)

        # Scoring mensual (día 1)
        if fecha.day == 1:
            ultimo_scoring = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_scoring.txt'), 0)
            scorings = []
            for i in range(100):
                scorings.append({
                    'id_scoring': ultimo_scoring + i + 1,
                    'id_cliente': random.choice(ids_clientes),
                    'score': random.randint(300, 850),
                    'riesgo': random.choice(['Bajo', 'Medio', 'Alto']),
                    'fecha_calculo': fecha_iso
                })
            guardar_csv('riesgos', 'scoring_crediticio', fecha_str,
                        ['id_scoring','id_cliente','score','riesgo','fecha_calculo'],
                        scorings)
            escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_scoring.txt'), ultimo_scoring + 100)

            # Morosidad mensual
            ultimo_mora = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_morosidad.txt'), 200)
            morosidades = []
            for i in range(20):
                morosidades.append({
                    'id_morosidad': ultimo_mora + i + 1,
                    'id_cliente': random.choice(ids_clientes),
                    'dias_mora': random.randint(1, 360),
                    'deuda_pendiente': round(random.uniform(5000, 500000), 2),
                    'fecha_reporte': fecha_iso
                })
            guardar_csv('riesgos', 'morosidad', fecha_str,
                        ['id_morosidad','id_cliente','dias_mora','deuda_pendiente','fecha_reporte'],
                        morosidades)
            escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_morosidad.txt'), ultimo_mora + 20)

    # ========================================================
    # 4.4 ATENCIÓN AL CLIENTE
    # ========================================================
    elif area == 'atencion':
        # Tickets diarios
        ultimo_ticket = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_ticket.txt'), 1000)
        tickets, nuevo_id = generar_tickets(fecha_str, ultimo_ticket, ids_clientes, 30)
        guardar_csv('atencion_cliente', 'tickets', fecha_str,
                    ['id_ticket','id_cliente','tipo_reclamo','descripcion','estado','fecha_creacion','fecha_resolucion'],
                    tickets)
        escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_ticket.txt'), nuevo_id)

        # Llamadas diarias
        ultimo_llamada = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_llamada.txt'), 3000)
        llamadas, nuevo_id = generar_llamadas(fecha_str, ultimo_llamada, ids_clientes, 100)
        guardar_csv('atencion_cliente', 'llamadas', fecha_str,
                    ['id_llamada','id_cliente','duracion_seg','resultado','fecha_llamada'],
                    llamadas)
        escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_llamada.txt'), nuevo_id)

        # Encuestas diarias
        ultimo_enc = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_encuesta.txt'), 1500)
        encuestas, nuevo_id = generar_encuestas(fecha_str, ultimo_enc, ids_clientes, 20)
        guardar_csv('atencion_cliente', 'encuestas', fecha_str,
                    ['id_encuesta','id_cliente','satisfaccion','comentario','fecha_encuesta'],
                    encuestas)
        escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_encuesta.txt'), nuevo_id)

    # ========================================================
    # 4.5 RRHH
    # ========================================================
    elif area == 'rrhh':
        # Ausencias diarias
        ultimo_aus = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_ausencia.txt'), 1200)
        ausencias, nuevo_id = generar_ausencias(fecha_str, ultimo_aus, ids_empleados, 5)
        guardar_csv('rrhh', 'ausencias', fecha_str,
                    ['id_ausencia','id_empleado','tipo_ausencia','dias','fecha_inicio','fecha_fin'],
                    ausencias)
        escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_ausencia.txt'), nuevo_id)

        # Empleados mensual (día 1)
        if fecha.day == 1:
            ultimo_emp = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_empleado.txt'), config.NUM_EMPLEADOS)
            nuevos_empleados = []
            for i in range(5):
                nuevos_empleados.append({
                    'id_empleado': ultimo_emp + i + 1,
                    'nombre': random.choice(['Juan', 'María', 'Carlos', 'Ana']),
                    'apellido': random.choice(['García', 'Rodríguez', 'Fernández']),
                    'cargo': random.choice(['Cajero', 'Oficial de negocios']),
                    'id_sucursal': random.choice(ids_sucursales) if ids_sucursales else 1,
                    'fecha_contratacion': fecha_iso,
                    'salario': round(random.uniform(50000, 200000), 2)
                })
            guardar_csv('rrhh', 'empleados', fecha_str,
                        ['id_empleado','nombre','apellido','cargo','id_sucursal','fecha_contratacion','salario'],
                        nuevos_empleados)
            escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_empleado.txt'), ultimo_emp + 5)

    # ========================================================
    # 4.6 CONTABILIDAD
    # ========================================================
    elif area == 'contabilidad':
        # Asientos diarios
        ultimo_asiento = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_asiento.txt'), 5000)
        asientos, nuevo_id = generar_asientos(fecha_str, ultimo_asiento, ids_cuentas_contables, 50)
        guardar_csv('contabilidad', 'asientos_contables', fecha_str,
                    ['id_asiento','id_cuenta_contable','fecha_contable','tipo_asiento','monto_debe','monto_haber','descripcion'],
                    asientos)
        escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_asiento.txt'), nuevo_id)

        # Presupuesto mensual (día 1)
        if fecha.day == 1:
            ultimo_pres = leer_ultimo_id(os.path.join(control_dir, 'ultimo_id_presupuesto.txt'), 50)
            presupuestos = []
            for i in range(5):
                presupuestos.append({
                    'id_presupuesto': ultimo_pres + i + 1,
                    'id_cuenta_contable': random.choice(ids_cuentas_contables) if ids_cuentas_contables else random.randint(1, 7),
                    'monto_presupuestado': round(random.uniform(50000, 1000000), 2),
                    'fecha_presupuesto': fecha_iso
                })
            guardar_csv('contabilidad', 'presupuesto', fecha_str,
                        ['id_presupuesto','id_cuenta_contable','monto_presupuestado','fecha_presupuesto'],
                        presupuestos)
            escribir_ultimo_id(os.path.join(control_dir, 'ultimo_id_presupuesto.txt'), ultimo_pres + 5)

    else:
        print(f"Área '{area}' no soportada. Use: core, crm, riesgos, atencion, rrhh, contabilidad")


# ============================================================
# 5. BLOQUE PRINCIPAL
# ============================================================
def main():
    parser = argparse.ArgumentParser(description='Genera archivos diarios incrementales por área')
    parser.add_argument('--area', type=str, required=True, help='Área: core, crm, riesgos, atencion, rrhh, contabilidad')
    parser.add_argument('--dias', type=int, default=1, help='Número de días retroactivos')
    args = parser.parse_args()

    hoy = datetime.date.today()
    for i in range(args.dias):
        fecha = hoy - datetime.timedelta(days=i)
        generar_area(fecha, args.area)

if __name__ == '__main__':
    main()