# 📄 Archivo: src/andes_bank/generators/utils.py
# Funciones auxiliares para los generadores

import random
import datetime
import csv
import os

from . import config

def set_seed(seed=None):
    """Fija la semilla para reproducibilidad."""
    random.seed(seed if seed is not None else config.SEED)

def random_date(start, end, as_string=True):
    """
    Genera una fecha aleatoria entre dos fechas.
    
    Args:
        start (str): fecha inicio en formato 'YYYY-MM-DD'.
        end (str): fecha fin en formato 'YYYY-MM-DD'.
        as_string (bool): si True devuelve string 'YYYY-MM-DD', si False devuelve datetime.date.
    
    Returns:
        str o datetime.date
    """
    start_dt = datetime.datetime.strptime(start, '%Y-%m-%d')
    end_dt = datetime.datetime.strptime(end, '%Y-%m-%d')
    delta = end_dt - start_dt
    random_days = random.randint(0, delta.days)
    date = start_dt + datetime.timedelta(days=random_days)
    if as_string:
        return date.strftime('%Y-%m-%d')
    return date

def random_datetime(start, end):
    """
    Genera una fecha y hora aleatoria entre dos fechas.
    Devuelve un string 'YYYY-MM-DD HH:MM:SS'.
    """
    start_dt = datetime.datetime.strptime(start, '%Y-%m-%d')
    end_dt = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(days=1)
    delta = end_dt - start_dt
    random_seconds = random.randint(0, int(delta.total_seconds()))
    dt = start_dt + datetime.timedelta(seconds=random_seconds)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def random_cuit():
    """Genera un CUIT ficticio con formato 30-XXXXXXXX-X."""
    digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    # Dígito verificador simplificado (no real)
    verificador = random.randint(0, 9)
    return f"30-{digits}-{verificador}"

def random_dni():
    """Genera un DNI argentino ficticio de 8 dígitos."""
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])

def write_csv(filename, fieldnames, rows):
    """
    Escribe una lista de diccionarios a un archivo CSV.
    
    Args:
        filename (str): ruta completa del archivo.
        fieldnames (list): lista de nombres de columnas.
        rows (list): lista de diccionarios.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Archivo generado: {filename} con {len(rows)} registros.")

def read_csv(filename):
    """
    Lee un archivo CSV y devuelve una lista de diccionarios.
    Útil para que generadores posteriores usen IDs existentes.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)