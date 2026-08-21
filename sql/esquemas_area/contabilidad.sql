-- 📄 Archivo: sql/esquemas_area/contabilidad.sql
-- Esquema de la base de datos transaccional Contabilidad

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS cuentas_contables (
    id_cuenta_contable INTEGER PRIMARY KEY,
    codigo_cuenta      TEXT,
    descripcion        TEXT,
    tipo_cuenta        TEXT
);

CREATE TABLE IF NOT EXISTS asientos_contables (
    id_asiento         INTEGER PRIMARY KEY,
    id_cuenta_contable INTEGER,
    fecha_contable     TEXT,
    tipo_asiento       TEXT,
    monto_debe         REAL,
    monto_haber        REAL,
    descripcion        TEXT
);

CREATE TABLE IF NOT EXISTS presupuesto (
    id_presupuesto     INTEGER PRIMARY KEY,
    id_cuenta_contable INTEGER,
    monto_presupuestado REAL,
    fecha_presupuesto  TEXT
);