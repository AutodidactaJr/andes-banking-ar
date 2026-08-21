-- ============================================================
-- ANDES BANKING AR - DATA WAREHOUSE COMPLETO (v3.0)
-- Incluye Plazos Fijos y Seguros
-- ============================================================

PRAGMA foreign_keys = ON;

-- DIMENSIONES
CREATE TABLE IF NOT EXISTS dim_cliente (
    id_cliente_sk       INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente_nk       INTEGER NOT NULL,
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
    fecha_inicio_vigencia TEXT DEFAULT (datetime('now')),
    fecha_fin_vigencia  TEXT,
    es_actual           INTEGER DEFAULT 1,
    fecha_carga         TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS dim_cuenta (
    id_cuenta_sk        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cuenta_nk        INTEGER NOT NULL,
    id_cliente_sk       INTEGER NOT NULL,
    id_sucursal_sk      INTEGER,
    tipo_cuenta         TEXT,
    moneda              TEXT,
    saldo               DECIMAL(18,2),
    fecha_apertura      TEXT,
    estado              TEXT,
    fecha_inicio_vigencia TEXT DEFAULT (datetime('now')),
    fecha_fin_vigencia  TEXT,
    es_actual           INTEGER DEFAULT 1,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_cliente_sk) REFERENCES dim_cliente(id_cliente_sk),
    FOREIGN KEY (id_sucursal_sk) REFERENCES dim_sucursal(id_sucursal_sk)
);

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

CREATE TABLE IF NOT EXISTS dim_canal (
    id_canal_sk         INTEGER PRIMARY KEY AUTOINCREMENT,
    canal_nombre        TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_producto (
    id_producto_sk      INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_nombre     TEXT NOT NULL UNIQUE,
    categoria           TEXT
);

CREATE TABLE IF NOT EXISTS dim_tiempo (
    id_tiempo_sk        INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha               TEXT NOT NULL UNIQUE,
    anio                INTEGER,
    mes                 INTEGER,
    dia                 INTEGER,
    nombre_mes          TEXT,
    nombre_dia_semana   TEXT
);

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

CREATE TABLE IF NOT EXISTS dim_empleado (
    id_empleado_sk      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_empleado_nk      INTEGER NOT NULL UNIQUE,
    nombre              TEXT,
    apellido            TEXT,
    cargo               TEXT,
    id_sucursal_sk      INTEGER,
    fecha_contratacion  TEXT,
    salario             REAL,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_sucursal_sk) REFERENCES dim_sucursal(id_sucursal_sk)
);

CREATE TABLE IF NOT EXISTS dim_tipo_reclamo (
    id_tipo_reclamo_sk  INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_reclamo_nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_tipo_riesgo (
    id_tipo_riesgo_sk   INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_riesgo_nombre  TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_cuenta_contable (
    id_cuenta_contable_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_cuenta       TEXT NOT NULL UNIQUE,
    descripcion         TEXT,
    tipo_cuenta         TEXT
);

-- Nueva dimensión para seguros
CREATE TABLE IF NOT EXISTS dim_seguro (
    id_seguro_sk        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_seguro_nk        INTEGER NOT NULL UNIQUE,
    tipo_seguro         TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now'))
);

-- HECHOS
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
    fecha_completa      TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_cliente_sk) REFERENCES dim_cliente(id_cliente_sk),
    FOREIGN KEY (id_cuenta_sk) REFERENCES dim_cuenta(id_cuenta_sk),
    FOREIGN KEY (id_sucursal_sk) REFERENCES dim_sucursal(id_sucursal_sk),
    FOREIGN KEY (id_canal_sk) REFERENCES dim_canal(id_canal_sk),
    FOREIGN KEY (id_tiempo_sk) REFERENCES dim_tiempo(id_tiempo_sk),
    FOREIGN KEY (id_producto_sk) REFERENCES dim_producto(id_producto_sk)
);

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
    FOREIGN KEY (id_canal_sk) REFERENCES dim_canal(id_canal_sk),
    FOREIGN KEY (id_tiempo_sk) REFERENCES dim_tiempo(id_tiempo_sk)
);

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

CREATE TABLE IF NOT EXISTS fact_reclamos (
    id_reclamo_sk       INTEGER PRIMARY KEY AUTOINCREMENT,
    id_reclamo_nk       INTEGER NOT NULL UNIQUE,
    id_cliente_sk       INTEGER NOT NULL,
    id_sucursal_sk      INTEGER,
    id_tipo_reclamo_sk  INTEGER NOT NULL,
    id_tiempo_sk        INTEGER NOT NULL,
    estado              TEXT,
    resolucion_dias     INTEGER,
    fecha_creacion      TEXT,
    fecha_resolucion    TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_cliente_sk) REFERENCES dim_cliente(id_cliente_sk),
    FOREIGN KEY (id_sucursal_sk) REFERENCES dim_sucursal(id_sucursal_sk),
    FOREIGN KEY (id_tipo_reclamo_sk) REFERENCES dim_tipo_reclamo(id_tipo_reclamo_sk),
    FOREIGN KEY (id_tiempo_sk) REFERENCES dim_tiempo(id_tiempo_sk)
);

CREATE TABLE IF NOT EXISTS fact_ausencias (
    id_ausencia_sk      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_ausencia_nk      INTEGER NOT NULL UNIQUE,
    id_empleado_sk      INTEGER NOT NULL,
    id_sucursal_sk      INTEGER,
    id_tiempo_sk        INTEGER NOT NULL,
    tipo_ausencia       TEXT,
    dias                INTEGER,
    fecha_inicio        TEXT,
    fecha_fin           TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_empleado_sk) REFERENCES dim_empleado(id_empleado_sk),
    FOREIGN KEY (id_sucursal_sk) REFERENCES dim_sucursal(id_sucursal_sk),
    FOREIGN KEY (id_tiempo_sk) REFERENCES dim_tiempo(id_tiempo_sk)
);

CREATE TABLE IF NOT EXISTS fact_scoring_crediticio (
    id_scoring_sk       INTEGER PRIMARY KEY AUTOINCREMENT,
    id_scoring_nk       INTEGER NOT NULL UNIQUE,
    id_cliente_sk       INTEGER NOT NULL,
    id_tiempo_sk        INTEGER NOT NULL,
    score               INTEGER,
    riesgo              TEXT,
    fecha_calculo       TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_cliente_sk) REFERENCES dim_cliente(id_cliente_sk),
    FOREIGN KEY (id_tiempo_sk) REFERENCES dim_tiempo(id_tiempo_sk)
);

CREATE TABLE IF NOT EXISTS fact_alertas_fraude (
    id_alerta_sk        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_alerta_nk        INTEGER NOT NULL UNIQUE,
    id_cliente_sk       INTEGER NOT NULL,
    id_cuenta_sk        INTEGER,
    id_tipo_riesgo_sk   INTEGER,
    id_tiempo_sk        INTEGER NOT NULL,
    tipo_alerta         TEXT,
    monto               REAL,
    estado              TEXT,
    fecha_deteccion     TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_cliente_sk) REFERENCES dim_cliente(id_cliente_sk),
    FOREIGN KEY (id_cuenta_sk) REFERENCES dim_cuenta(id_cuenta_sk),
    FOREIGN KEY (id_tipo_riesgo_sk) REFERENCES dim_tipo_riesgo(id_tipo_riesgo_sk),
    FOREIGN KEY (id_tiempo_sk) REFERENCES dim_tiempo(id_tiempo_sk)
);

CREATE TABLE IF NOT EXISTS fact_asientos_contables (
    id_asiento_sk       INTEGER PRIMARY KEY AUTOINCREMENT,
    id_asiento_nk       INTEGER NOT NULL UNIQUE,
    id_cuenta_contable_sk INTEGER NOT NULL,
    id_tiempo_sk        INTEGER NOT NULL,
    id_sucursal_sk      INTEGER,
    tipo_asiento        TEXT,
    monto_debe          REAL,
    monto_haber         REAL,
    descripcion         TEXT,
    fecha_contable      TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_cuenta_contable_sk) REFERENCES dim_cuenta_contable(id_cuenta_contable_sk),
    FOREIGN KEY (id_tiempo_sk) REFERENCES dim_tiempo(id_tiempo_sk),
    FOREIGN KEY (id_sucursal_sk) REFERENCES dim_sucursal(id_sucursal_sk)
);

-- NUEVOS HECHOS
CREATE TABLE IF NOT EXISTS fact_plazos_fijos (
    id_plazo_sk         INTEGER PRIMARY KEY AUTOINCREMENT,
    id_plazo_nk         INTEGER NOT NULL UNIQUE,
    id_cliente_sk       INTEGER NOT NULL,
    id_tiempo_sk        INTEGER,
    monto               REAL,
    tasa_interes        REAL,
    fecha_vencimiento   TEXT,
    estado              TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_cliente_sk) REFERENCES dim_cliente(id_cliente_sk),
    FOREIGN KEY (id_tiempo_sk) REFERENCES dim_tiempo(id_tiempo_sk)
);

CREATE TABLE IF NOT EXISTS fact_seguros (
    id_seguro_sk        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_seguro_nk        INTEGER NOT NULL UNIQUE,
    id_cliente_sk       INTEGER NOT NULL,
    id_seguro_tipo_sk   INTEGER,
    id_tiempo_sk        INTEGER,
    prima_mensual       REAL,
    estado              TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_cliente_sk) REFERENCES dim_cliente(id_cliente_sk),
    FOREIGN KEY (id_seguro_tipo_sk) REFERENCES dim_seguro(id_seguro_sk),
    FOREIGN KEY (id_tiempo_sk) REFERENCES dim_tiempo(id_tiempo_sk)
);

CREATE TABLE IF NOT EXISTS fact_salarios_historial (
    id_salario_sk   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_salario_nk   INTEGER NOT NULL UNIQUE,
    id_empleado_sk  INTEGER NOT NULL,
    salario         REAL,
    fecha_inicio    TEXT,
    fecha_fin       TEXT,
    fecha_carga     TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_empleado_sk) REFERENCES dim_empleado(id_empleado_sk)
);

CREATE TABLE IF NOT EXISTS fact_evaluaciones (
    id_evaluacion_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    id_evaluacion_nk INTEGER NOT NULL UNIQUE,
    id_empleado_sk  INTEGER NOT NULL,
    anio            INTEGER,
    puntaje         INTEGER,
    comentario      TEXT,
    fecha_carga     TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_empleado_sk) REFERENCES dim_empleado(id_empleado_sk)
);

CREATE TABLE IF NOT EXISTS dim_agente (
    id_agente_sk      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_agente_nk      INTEGER NOT NULL UNIQUE,
    nombre            TEXT,
    apellido          TEXT,
    id_sucursal_sk    INTEGER,
    fecha_carga       TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_sucursal_sk) REFERENCES dim_sucursal(id_sucursal_sk)
);

CREATE TABLE IF NOT EXISTS dim_sla (
    id_sla_sk         INTEGER PRIMARY KEY AUTOINCREMENT,
    id_sla_nk         INTEGER NOT NULL UNIQUE,
    tipo_reclamo      TEXT,
    tiempo_objetivo_horas INTEGER,
    fecha_carga       TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS fact_oportunidades (
    id_oportunidad_sk   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_oportunidad_nk   INTEGER NOT NULL UNIQUE,
    id_cliente_sk       INTEGER NOT NULL,
    id_tiempo_sk        INTEGER,
    producto_interes    TEXT,
    estado              TEXT,
    fecha_creacion      TEXT,
    fecha_carga         TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (id_cliente_sk) REFERENCES dim_cliente(id_cliente_sk),
    FOREIGN KEY (id_tiempo_sk) REFERENCES dim_tiempo(id_tiempo_sk)
);