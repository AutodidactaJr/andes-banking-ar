-- 📄 Archivo: sql/dimensiones.sql
-- Script para crear las tablas de dimensiones del Data Warehouse (actualizado)

PRAGMA foreign_keys = ON;

-- ============================================================
-- Dimensión: dim_cliente
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_cliente (
    id_cliente_sk       INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente_nk       INTEGER NOT NULL UNIQUE,
    tipo_doc            TEXT,
    num_doc             TEXT,
    nombre              TEXT,
    apellido            TEXT,
    email               TEXT,
    telefono            TEXT,
    fecha_nacimiento    TEXT,
    direccion           TEXT,
    ciudad              TEXT,
    provincia           TEXT,
    segmento            TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- Dimensión: dim_cuenta
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_cuenta (
    id_cuenta_sk        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cuenta_nk        INTEGER NOT NULL UNIQUE,
    id_cliente_sk       INTEGER NOT NULL,
    id_sucursal_sk      INTEGER,  -- columna nueva
    tipo_cuenta         TEXT,
    moneda              TEXT,
    fecha_apertura      TEXT,
    estado              TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_cliente_sk) REFERENCES dim_cliente(id_cliente_sk),
    FOREIGN KEY (id_sucursal_sk) REFERENCES dim_sucursal(id_sucursal_sk)
);

-- ============================================================
-- Dimensión: dim_tarjeta
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_tarjeta (
    id_tarjeta_sk       INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tarjeta_nk       INTEGER NOT NULL UNIQUE,
    id_cliente_sk       INTEGER NOT NULL,
    id_cuenta_sk        INTEGER,
    marca               TEXT,
    tipo                TEXT,
    numero              TEXT,
    limite              REAL,
    fecha_emision       TEXT,
    fecha_vencimiento   TEXT,
    estado              TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_cliente_sk) REFERENCES dim_cliente(id_cliente_sk),
    FOREIGN KEY (id_cuenta_sk) REFERENCES dim_cuenta(id_cuenta_sk)
);

-- ============================================================
-- Dimensión: dim_sucursal
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_sucursal (
    id_sucursal_sk      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_sucursal_nk      INTEGER NOT NULL UNIQUE,
    nombre              TEXT,
    direccion           TEXT,
    ciudad              TEXT,
    provincia           TEXT,
    region              TEXT,
    fecha_apertura      TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- Dimensión: dim_canal
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_canal (
    id_canal_sk         INTEGER PRIMARY KEY AUTOINCREMENT,
    canal_nombre        TEXT NOT NULL UNIQUE
);

-- ============================================================
-- Dimensión: dim_producto
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_producto (
    id_producto_sk      INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_nombre     TEXT NOT NULL UNIQUE,
    categoria           TEXT
);

-- ============================================================
-- Dimensión: dim_tiempo
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_tiempo (
    id_tiempo_sk        INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha               TEXT NOT NULL UNIQUE,
    anio                INTEGER,
    mes                 INTEGER,
    dia                 INTEGER,
    nombre_mes          TEXT,
    nombre_dia_semana   TEXT
);

-- ============================================================
-- Dimensión: dim_campana
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_campana (
    id_campana_sk       INTEGER PRIMARY KEY AUTOINCREMENT,
    id_campana_nk       INTEGER NOT NULL UNIQUE,
    nombre              TEXT,
    canal               TEXT,
    segmento_objetivo   TEXT,
    fecha_inicio        TEXT,
    fecha_fin           TEXT,
    costo               REAL,
    fecha_carga         TEXT DEFAULT (datetime('now'))
);