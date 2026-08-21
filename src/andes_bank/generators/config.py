# 📄 Archivo: src/andes_bank/generators/config.py
# Configuración central para los generadores de datos sintéticos

import os

# Semilla para reproducibilidad
SEED = 42

# Rutas base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')

# Crear carpeta raw si no existe
os.makedirs(RAW_DIR, exist_ok=True)

# Volúmenes de datos
NUM_CLIENTES = 5000
NUM_SUCURSALES = 35
NUM_CUENTAS = 8000
NUM_TARJETAS = 10000
NUM_PRESTAMOS = 3000
NUM_TRANSACCIONES = 50000  # total repartido en 3 años
NUM_PAGOS = 20000

# Fechas
FECHA_INICIO = '2021-01-01'
FECHA_FIN = '2023-12-31'

# Segmentos de clientes
SEGMENTOS_PERSONA_FISICA = ['Clásico', 'Premium', 'Joven', 'Jubilado']
SEGMENTOS_PERSONA_JURIDICA = ['PyME', 'Corporativo']

# Provincias y ciudades de Argentina
PROVINCIAS = {
    'Mendoza': ['Mendoza', 'San Rafael', 'Godoy Cruz', 'Luján de Cuyo'],
    'San Juan': ['San Juan', 'Rawson', 'Chimbas'],
    'San Luis': ['San Luis', 'Villa Mercedes'],
    'Córdoba': ['Córdoba', 'Villa Carlos Paz', 'Río Cuarto'],
    'Santa Fe': ['Rosario', 'Santa Fe', 'Rafaela'],
    'Tucumán': ['San Miguel de Tucumán', 'Tafí Viejo'],
    'Salta': ['Salta', 'Tartagal'],
    'Jujuy': ['San Salvador de Jujuy'],
    'Entre Ríos': ['Paraná', 'Concordia'],
    'Corrientes': ['Corrientes'],
    'Neuquén': ['Neuquén', 'Cutral Co'],
    'Río Negro': ['San Carlos de Bariloche', 'General Roca']
}

# Tipos de cuentas
TIPOS_CUENTA = ['Caja de Ahorro ARS', 'Caja de Ahorro USD', 'Cuenta Corriente']

# Marcas de tarjetas
MARCAS_TARJETA = ['Visa', 'Mastercard', 'AndesCard']

# Canales de transacciones

CANALES = ['Sucursal', 'Home Banking', 'Mobile Banking', 'Cajero Automático', 'Posnet', 'QR']


# ============================================================
# Parámetros para CRM/Marketing
# ============================================================
NUM_CAMPANAS = 50
NUM_INTERACCIONES = 20000
NUM_LEADS = 2000

CANALES_CAMPANA = ['Email', 'SMS', 'Push', 'Redes Sociales']
SEGMENTOS_OBJETIVO = ['Clásico', 'Premium', 'Joven', 'Jubilado', 'PyME', 'Corporativo']
TIPOS_INTERACCION = ['Apertura', 'Clic', 'Conversión', 'Rebote']
DISPOSITIVOS = ['Desktop', 'Mobile', 'Tablet']
ESTADOS_LEAD = ['Nuevo', 'Contactado', 'Convertido', 'Perdido']
PRODUCTOS_INTERES = ['Caja de Ahorro', 'Tarjeta de Crédito', 'Préstamo Personal', 'Plazo Fijo', 'Seguro de Vida']

# ============================================================
# Parámetros para Riesgos
# ============================================================
NUM_ALERTAS_FRAUDE = 300
NUM_INCIDENTES = 150
NUM_MOROSIDAD = 200

# ============================================================
# Parámetros para Atención al Cliente
# ============================================================
NUM_TICKETS = 1000
NUM_LLAMADAS = 3000
NUM_ENCUESTAS = 1500

# ============================================================
# Parámetros para RRHH
# ============================================================
NUM_EMPLEADOS = 500
NUM_AUSENCIAS = 1200

# ============================================================
# Parámetros para Contabilidad
# ============================================================
NUM_ASIENTOS = 5000
NUM_CUENTAS_CONTABLES = 100
NUM_PRESUPUESTO = 50

# ============================================================
# Parámetros para generación diaria incremental
# ============================================================
DIARIO_CLIENTES = 50
DIARIO_TRANSACCIONES = 1000
DIARIO_PAGOS = 20
DIARIO_INTERACCIONES = 200
DIARIO_LEADS = 20
DIARIO_ALERTAS = 5
DIARIO_TICKETS = 30
DIARIO_LLAMADAS = 100
DIARIO_ENCUESTAS = 20
DIARIO_AUSENCIAS = 5
DIARIO_ASIENTOS = 50

MENSUAL_SCORING = 100
MENSUAL_MOROSIDAD = 20
MENSUAL_EMPLEADOS = 5
MENSUAL_PRESUPUESTO = 5

PROB_CAMPANA = 0.10
PROB_INCIDENTE = 0.05

# ============================================================
# Parámetros para Plazos Fijos y Seguros
# ============================================================
NUM_PLAZOS_FIJOS = 1000
NUM_SEGUROS = 800

# ============================================================
# Parámetros para RRHH - Salarios y Evaluaciones
# ============================================================
NUM_SALARIOS_HISTORIAL = 1500
NUM_EVALUACIONES = 500

# ============================================================
# Parámetros para Atención al Cliente - Agentes y SLA
# ============================================================
NUM_AGENTES = 100
NUM_SLA = 6   # Tipos de reclamo con SLA definido
TIEMPO_SLA = {
    'Reclamo': 48,
    'Consulta': 24,
    'Sugerencia': 72,
    'Error': 12,
    'Queja': 24,
    'Solicitud': 48
}

# ============================================================
# Parámetros para CRM - Oportunidades
# ============================================================
NUM_OPORTUNIDADES = 1200

