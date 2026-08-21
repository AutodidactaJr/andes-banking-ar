-- 📄 Archivo: sql/esquemas_area/core_bancario.sql
-- Esquema de la base de datos transaccional Core Bancario

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente       INTEGER PRIMARY KEY,
    tipo_doc         TEXT,
    num_doc          TEXT,
    nombre           TEXT,
    apellido         TEXT,
    email            TEXT,
    telefono         TEXT,
    fecha_nacimiento TEXT,
    direccion        TEXT,
    ciudad           TEXT,
    provincia        TEXT,
    segmento         TEXT
);

CREATE TABLE IF NOT EXISTS sucursales (
    id_sucursal     INTEGER PRIMARY KEY,
    nombre          TEXT,
    direccion       TEXT,
    ciudad          TEXT,
    provincia       TEXT,
    region          TEXT,
    fecha_apertura  TEXT
);

CREATE TABLE IF NOT EXISTS cuentas (
    id_cuenta       INTEGER PRIMARY KEY,
    id_cliente      INTEGER,
    tipo_cuenta     TEXT,
    moneda          TEXT,
    saldo           REAL,
    fecha_apertura  TEXT,
    estado          TEXT,
    id_sucursal     INTEGER,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal)
);

CREATE TABLE IF NOT EXISTS tarjetas (
    id_tarjeta          INTEGER PRIMARY KEY,
    id_cliente          INTEGER,
    id_cuenta           INTEGER,
    marca               TEXT,
    tipo                TEXT,
    numero              TEXT,
    limite              REAL,
    fecha_emision       TEXT,
    fecha_vencimiento   TEXT,
    estado              TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_cuenta) REFERENCES cuentas(id_cuenta)
);

CREATE TABLE IF NOT EXISTS prestamos (
    id_prestamo         INTEGER PRIMARY KEY,
    id_cliente          INTEGER,
    tipo                TEXT,
    monto               REAL,
    tasa_interes        REAL,
    plazo_meses         INTEGER,
    cuota               REAL,
    fecha_desembolso    TEXT,
    saldo_pendiente     REAL,
    estado              TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE IF NOT EXISTS transacciones (
    id_transaccion      INTEGER PRIMARY KEY,
    id_cuenta           INTEGER,
    tipo_transaccion    TEXT,
    monto               REAL,
    moneda              TEXT,
    fecha               TEXT,
    canal               TEXT,
    estado              TEXT,
    referencia          TEXT,
    FOREIGN KEY (id_cuenta) REFERENCES cuentas(id_cuenta)
);

CREATE TABLE IF NOT EXISTS pagos (
    id_pago         INTEGER PRIMARY KEY,
    id_cuenta       INTEGER,
    entidad         TEXT,
    tipo_pago       TEXT,
    monto           REAL,
    fecha           TEXT,
    canal           TEXT,
    estado          TEXT,
    referencia      TEXT,
    FOREIGN KEY (id_cuenta) REFERENCES cuentas(id_cuenta)
);

CREATE TABLE IF NOT EXISTS plazos_fijos (
    id_plazo_fijo INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    monto DECIMAL(18,2),
    tasa_interes DECIMAL(5,2),
    fecha_constitucion DATE,
    fecha_vencimiento DATE,
    estado TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE IF NOT EXISTS seguros (
    id_seguro INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    tipo_seguro TEXT,
    prima_mensual DECIMAL(18,2),
    fecha_contratacion DATE,
    estado TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);