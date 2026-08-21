# 📄 Archivo: src/andes_bank/generators/generar_clientes.py
# Generador de datos sintéticos de clientes

import random
import os
from . import config, utils

def generar_clientes():
    utils.set_seed()
    clientes = []
    ids = list(range(1, config.NUM_CLIENTES + 1))
    random.shuffle(ids)

    for id_cliente in ids:
        tipo_doc = 'DNI' if random.random() < 0.8 else 'CUIT'
        if tipo_doc == 'DNI':
            num_doc = utils.random_dni()
            fecha_nacimiento = utils.random_date('1950-01-01', '2005-12-31')
            anio = int(fecha_nacimiento[:4])
            edad = 2023 - anio
            if edad < 25:
                segmento = 'Joven'
            elif edad <= 60:
                segmento = random.choice(['Clásico', 'Premium'])
            else:
                segmento = 'Jubilado'
            apellido = random.choice(['García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez', 'Pérez', 'Gómez', 'Díaz', 'Sosa'])
            nombre = random.choice(['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Lucía', 'Pedro', 'Sofía', 'Jorge', 'Valentina'])
        else:
            num_doc = utils.random_cuit()
            fecha_nacimiento = ''
            apellido = ''
            nombre = f"Empresa {random.randint(1,1000)} SRL"
            segmento = random.choice(config.SEGMENTOS_PERSONA_JURIDICA)

        if random.random() < 0.02:
            email = ''
        else:
            if tipo_doc == 'DNI':
                base = nombre.lower() + '.' + apellido.lower()
                base = base.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                email = f"{base}.{num_doc[-4:]}@mail.com"
            else:
                razon = nombre.lower().replace(' ', '.')
                email = f"contacto@{razon}.com.ar"

        if random.random() < 0.02:
            telefono = ''
        else:
            telefono = '261' + ''.join([str(random.randint(0,9)) for _ in range(7)])

        provincia = random.choice(list(config.PROVINCIAS.keys()))
        ciudad = random.choice(config.PROVINCIAS[provincia])
        direccion = f"Calle {random.randint(1,2000)} N°{random.randint(100,999)}"

        cliente = {
            'id_cliente': id_cliente,
            'tipo_doc': tipo_doc,
            'num_doc': num_doc,
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento,
            'direccion': direccion,
            'ciudad': ciudad,
            'provincia': provincia,
            'segmento': segmento
        }
        clientes.append(cliente)

    # Introducir duplicados (1%)
    num_duplicados = int(config.NUM_CLIENTES * 0.01)
    for _ in range(num_duplicados):
        original = random.choice(clientes)
        duplicado = original.copy()
        duplicado['email'] = ''
        duplicado['telefono'] = ''
        clientes.append(duplicado)

    # Introducir error de fecha (0.5%)
    num_fechas_mal = int(config.NUM_CLIENTES * 0.005)
    for _ in range(num_fechas_mal):
        cliente = random.choice(clientes)
        if cliente['fecha_nacimiento']:
            partes = cliente['fecha_nacimiento'].split('-')
            cliente['fecha_nacimiento'] = f"{partes[2]}/{partes[1]}/{partes[0]}"

    fieldnames = ['id_cliente', 'tipo_doc', 'num_doc', 'nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento', 'direccion', 'ciudad', 'provincia', 'segmento']
    ruta = os.path.join(config.RAW_DIR, 'core_bancario', 'clientes', 'clientes.csv')
    utils.write_csv(ruta, fieldnames, clientes)

if __name__ == '__main__':
    generar_clientes()