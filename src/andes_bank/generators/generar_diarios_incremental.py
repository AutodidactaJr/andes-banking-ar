# 📄 Archivo: src/andes_bank/generators/generar_diarios_incremental.py
# Generador incremental diario: genera solo registros nuevos por día

import argparse
import datetime
import os
import random
from . import config, utils

# ------------------------------------------------------------
# Funciones de control de IDs
# ------------------------------------------------------------
def leer_ultimo_id(archivo_control, default=0):
    """Lee el último ID desde un archivo de control. Si no existe, devuelve default."""
    if not os.path.exists(archivo_control):
        return default
    with open(archivo_control, 'r', encoding='utf-8') as f:
        contenido = f.read().strip()
        return int(contenido) if contenido.isdigit() else default

def escribir_ultimo_id(archivo_control, valor):
    """Escribe el último ID en un archivo de control."""
    with open(archivo_control, 'w', encoding='utf-8') as f:
        f.write(str(valor))

# ------------------------------------------------------------
# Generador diario de clientes
# ------------------------------------------------------------
def generar_clientes_diario(fecha_str, ultimo_id_cliente, cantidad):
    """
    Genera `cantidad` clientes nuevos con IDs consecutivos a partir de ultimo_id_cliente.
    Retorna (lista_clientes, nuevo_ultimo_id).
    """
    # Semilla basada en la fecha para variar los datos diarios
    random.seed(int(fecha_str.replace('_', '')))
    
    clientes = []
    nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Lucía', 'Pedro', 'Sofía', 'Jorge', 'Valentina']
    apellidos = ['García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez', 'Pérez', 'Gómez', 'Díaz', 'Sosa']
    provincias = list(config.PROVINCIAS.keys())

    for i in range(cantidad):
        id_cliente = ultimo_id_cliente + i + 1  # IDs consecutivos
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
    return clientes, ultimo_id_cliente + cantidad

# ------------------------------------------------------------
# Generador diario de transacciones
# ------------------------------------------------------------
def generar_transacciones_diario(fecha_str, ultimo_id_transaccion, ids_cuentas, cantidad):
    """
    Genera `cantidad` transacciones nuevas con IDs consecutivos y fecha del día.
    Retorna (lista_transacciones, nuevo_ultimo_id).
    """
    # Semilla distinta a clientes para variar
    random.seed(int(fecha_str.replace('_', '')) + 1)
    
    transacciones = []
    tipos = ['Depósito', 'Retiro', 'Transferencia enviada', 'Transferencia recibida', 'Consumo débito']
    canales = config.CANALES if hasattr(config, 'CANALES') else ['Home Banking', 'Mobile Banking', 'Sucursal', 'Cajero Automático', 'Posnet']

    for i in range(cantidad):
        id_transaccion = ultimo_id_transaccion + i + 1
        id_cuenta = random.choice(ids_cuentas) if ids_cuentas else random.randint(1, 8000)
        tipo = random.choice(tipos)
        signo = 1 if tipo in ['Depósito', 'Transferencia recibida'] else -1
        monto = round(random.uniform(100, 500000) * signo, 2)
        fecha = f"{fecha_str[:4]}-{fecha_str[5:7]}-{fecha_str[8:10]} {random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"
        canal = random.choice(canales)
        estado = 'Completada' if random.random() < 0.97 else 'Rechazada'
        referencia = f"TRX-{id_transaccion:06d}"
        transaccion = {
            'id_transaccion': id_transaccion,
            'id_cuenta': id_cuenta,
            'tipo_transaccion': tipo,
            'monto': monto,
            'moneda': 'ARS',
            'fecha': fecha,
            'canal': canal,
            'estado': estado,
            'referencia': referencia
        }
        transacciones.append(transaccion)
    return transacciones, ultimo_id_transaccion + cantidad

# ------------------------------------------------------------
# Función que genera un día completo
# ------------------------------------------------------------
def generar_dia(fecha):
    """Genera archivos diarios de clientes y transacciones para una fecha dada."""
    fecha_str = fecha.strftime('%Y_%m_%d')
    fecha_iso = fecha.strftime('%Y-%m-%d')

    # Rutas de archivos de control
    control_dir = os.path.join(config.BASE_DIR, 'data', 'control')
    os.makedirs(control_dir, exist_ok=True)
    control_cliente = os.path.join(control_dir, 'ultimo_id_cliente.txt')
    control_transaccion = os.path.join(control_dir, 'ultimo_id_transaccion.txt')

    # Leer últimos IDs
    ultimo_id_cliente = leer_ultimo_id(control_cliente, 0)
    ultimo_id_transaccion = leer_ultimo_id(control_transaccion, 0)

    # Obtener cuentas existentes desde core_bancario.db
    ruta_core_db = os.path.join(config.BASE_DIR, 'data', 'databases', 'core_bancario.db')
    ids_cuentas = []
    if os.path.exists(ruta_core_db):
        import sqlite3
        conn = sqlite3.connect(ruta_core_db)
        cur = conn.cursor()
        cur.execute("SELECT id_cuenta FROM cuentas LIMIT 8000")
        ids_cuentas = [row[0] for row in cur.fetchall()]
        conn.close()
    if not ids_cuentas:
        ids_cuentas = list(range(1, 8001))  # fallback

    # Generar clientes y transacciones diarios
    clientes_diarios, nuevo_id_cliente = generar_clientes_diario(fecha_str, ultimo_id_cliente, cantidad=50)
    transacciones_diarias, nuevo_id_transaccion = generar_transacciones_diario(fecha_str, ultimo_id_transaccion, ids_cuentas, cantidad=1000)

    # Guardar archivos CSV en subcarpetas
    core_raw_dir = os.path.join(config.RAW_DIR, 'core_bancario')
    archivo_clientes = os.path.join(core_raw_dir, 'clientes', f'clientes_{fecha_str}.csv')
    archivo_transacciones = os.path.join(core_raw_dir, 'transacciones', f'transacciones_{fecha_str}.csv')
    os.makedirs(os.path.dirname(archivo_clientes), exist_ok=True)
    os.makedirs(os.path.dirname(archivo_transacciones), exist_ok=True)

    fieldnames_clientes = ['id_cliente', 'tipo_doc', 'num_doc', 'nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento', 'direccion', 'ciudad', 'provincia', 'segmento']
    fieldnames_transacciones = ['id_transaccion', 'id_cuenta', 'tipo_transaccion', 'monto', 'moneda', 'fecha', 'canal', 'estado', 'referencia']
    utils.write_csv(archivo_clientes, fieldnames_clientes, clientes_diarios)
    utils.write_csv(archivo_transacciones, fieldnames_transacciones, transacciones_diarias)

    # Actualizar archivos de control
    escribir_ultimo_id(control_cliente, nuevo_id_cliente)
    escribir_ultimo_id(control_transaccion, nuevo_id_transaccion)

    print(f"Día {fecha_iso}: clientes nuevos={len(clientes_diarios)}, transacciones nuevas={len(transacciones_diarias)}")

# ------------------------------------------------------------
# Bloque principal con argumentos
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Genera archivos CSV diarios retroactivos.')
    parser.add_argument('--dias', type=int, default=1, help='Número de días a generar hacia atrás desde hoy')
    parser.add_argument('--cantidad-clientes', type=int, default=50, help='Clientes nuevos por día')
    parser.add_argument('--cantidad-transacciones', type=int, default=1000, help='Transacciones por día')
    args = parser.parse_args()

    hoy = datetime.date.today()
    for i in range(args.dias):
        fecha = hoy - datetime.timedelta(days=i)
        generar_dia(fecha)

if __name__ == '__main__':
    main()