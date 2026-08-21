-- 📄 Archivo: sql/hechos.sql
-- Script para crear las tablas de hechos del Data Warehouse

PRAGMA foreign_keys = ON;

-- ============================================================
-- Hecho: fact_transacciones
-- Cada fila representa una transacción financiera individual
-- ============================================================
CREATE TABLE IF NOT EXISTS fact_transacciones (
    id_transaccion_sk   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_transaccion_nk   INTEGER NOT NULL UNIQUE,
    id_cliente_sk       INTEGER NOT NULL,
    id_cuenta_sk        INTEGER NOT NULL,
    id_sucursal_sk      INTEGER,
    id_canal_sk         INTEGER NOT NULL,
    id_tiempo_sk        INTEGER NOT NULL,
    id_producto_sk      INTEGER,
    tipo_transaccion    TEXT,
    monto               REAL,
    moneda              TEXT,
    estado              TEXT,
    referencia          TEXT,
    fecha_completa      TEXT,  -- Fecha y hora original de la transacción
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_cliente_sk) REFERENCES dim_cliente(id_cliente_sk),
    FOREIGN KEY (id_cuenta_sk) REFERENCES dim_cuenta(id_cuenta_sk),
    FOREIGN KEY (id_sucursal_sk) REFERENCES dim_sucursal(id_sucursal_sk),
    FOREIGN KEY (id_canal_sk) REFERENCES dim_canal(id_canal_sk),
    FOREIGN KEY (id_producto_sk) REFERENCES dim_producto(id_producto_sk)
);

-- ============================================================
-- Hecho: fact_pagos
-- Pagos de servicios y cuotas de préstamos
-- ============================================================
CREATE TABLE IF NOT EXISTS fact_pagos (
    id_pago_sk          INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pago_nk          INTEGER NOT NULL UNIQUE,
    id_cliente_sk       INTEGER NOT NULL,
    id_cuenta_sk        INTEGER,
    id_canal_sk         INTEGER NOT NULL,
    id_tiempo_sk        INTEGER NOT NULL,
    entidad             TEXT,
    tipo_pago           TEXT,
    monto               REAL,
    estado              TEXT,
    referencia          TEXT,
    fecha_completa      TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_cliente_sk) REFERENCES dim_cliente(id_cliente_sk),
    FOREIGN KEY (id_cuenta_sk) REFERENCES dim_cuenta(id_cuenta_sk),
    FOREIGN KEY (id_canal_sk) REFERENCES dim_canal(id_canal_sk)
);

-- ============================================================
-- Hecho: fact_interacciones_campana
-- ============================================================
CREATE TABLE IF NOT EXISTS fact_interacciones_campana (
    id_interaccion_sk   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_interaccion_nk   INTEGER NOT NULL UNIQUE,
    id_campana_sk       INTEGER NOT NULL,
    id_cliente_sk       INTEGER NOT NULL,
    id_tiempo_sk        INTEGER,
    tipo_interaccion    TEXT,
    dispositivo         TEXT,
    fecha_completa      TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_campana_sk) REFERENCES dim_campana(id_campana_sk),
    FOREIGN KEY (id_cliente_sk) REFERENCES dim_cliente(id_cliente_sk),
    FOREIGN KEY (id_tiempo_sk) REFERENCES dim_tiempo(id_tiempo_sk)
);

-- ============================================================
-- Hecho: fact_leads
-- ============================================================
CREATE TABLE IF NOT EXISTS fact_leads (
    id_lead_sk          INTEGER PRIMARY KEY AUTOINCREMENT,
    id_lead_nk          INTEGER NOT NULL UNIQUE,
    id_campana_sk       INTEGER NOT NULL,
    id_cliente_sk       INTEGER,
    id_tiempo_sk        INTEGER,
    estado              TEXT,
    producto_interes    TEXT,
    fecha_creacion      TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_campana_sk) REFERENCES dim_campana(id_campana_sk),
    FOREIGN KEY (id_cliente_sk) REFERENCES dim_cliente(id_cliente_sk),
    FOREIGN KEY (id_tiempo_sk) REFERENCES dim_tiempo(id_tiempo_sk)
);
