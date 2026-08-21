-- ============================================================
-- STAGING COMPLETO (incluye plazos fijos y seguros)
-- ============================================================

CREATE TABLE IF NOT EXISTS stg_clientes (
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

CREATE TABLE IF NOT EXISTS stg_sucursales (
    id_sucursal     INTEGER PRIMARY KEY,
    nombre          TEXT,
    direccion       TEXT,
    ciudad          TEXT,
    provincia       TEXT,
    region          TEXT,
    fecha_apertura  TEXT
);

CREATE TABLE IF NOT EXISTS stg_cuentas (
    id_cuenta       INTEGER PRIMARY KEY,
    id_cliente      INTEGER,
    tipo_cuenta     TEXT,
    moneda          TEXT,
    saldo           REAL,
    fecha_apertura  TEXT,
    estado          TEXT,
    id_sucursal     INTEGER
);

CREATE TABLE IF NOT EXISTS stg_tarjetas (
    id_tarjeta          INTEGER PRIMARY KEY,
    id_cliente          INTEGER,
    id_cuenta           INTEGER,
    marca               TEXT,
    tipo                TEXT,
    numero              TEXT,
    limite              REAL,
    fecha_emision       TEXT,
    fecha_vencimiento   TEXT,
    estado              TEXT
);

CREATE TABLE IF NOT EXISTS stg_prestamos (
    id_prestamo         INTEGER PRIMARY KEY,
    id_cliente          INTEGER,
    tipo                TEXT,
    monto               REAL,
    tasa_interes        REAL,
    plazo_meses         INTEGER,
    cuota               REAL,
    fecha_desembolso    TEXT,
    saldo_pendiente     REAL,
    estado              TEXT
);

CREATE TABLE IF NOT EXISTS stg_transacciones (
    id_transaccion      INTEGER PRIMARY KEY,
    id_cuenta           INTEGER,
    tipo_transaccion    TEXT,
    monto               REAL,
    moneda              TEXT,
    fecha               TEXT,
    canal               TEXT,
    estado              TEXT,
    referencia          TEXT
);

CREATE TABLE IF NOT EXISTS stg_pagos (
    id_pago         INTEGER PRIMARY KEY,
    id_cuenta       INTEGER,
    entidad         TEXT,
    tipo_pago       TEXT,
    monto           REAL,
    fecha           TEXT,
    canal           TEXT,
    estado          TEXT,
    referencia      TEXT
);

-- NUEVAS STAGING
CREATE TABLE IF NOT EXISTS stg_plazos_fijos (
    id_plazo_fijo     INTEGER PRIMARY KEY,
    id_cliente        INTEGER,
    monto             REAL,
    tasa_interes      REAL,
    fecha_constitucion TEXT,
    fecha_vencimiento TEXT,
    estado            TEXT
);

CREATE TABLE IF NOT EXISTS stg_seguros (
    id_seguro         INTEGER PRIMARY KEY,
    id_cliente        INTEGER,
    tipo_seguro       TEXT,
    prima_mensual     REAL,
    fecha_contratacion TEXT,
    estado            TEXT
);

-- CRM
CREATE TABLE IF NOT EXISTS stg_campanas (
    id_campana        INTEGER PRIMARY KEY,
    nombre            TEXT,
    canal             TEXT,
    segmento_objetivo TEXT,
    fecha_inicio      TEXT,
    fecha_fin         TEXT,
    costo             REAL
);

CREATE TABLE IF NOT EXISTS stg_interacciones (
    id_interaccion    INTEGER PRIMARY KEY,
    id_campana        INTEGER,
    id_cliente        INTEGER,
    fecha             TEXT,
    tipo_interaccion  TEXT,
    dispositivo       TEXT
);

CREATE TABLE IF NOT EXISTS stg_leads (
    id_lead           INTEGER PRIMARY KEY,
    id_campana        INTEGER,
    id_cliente        INTEGER,
    fecha_creacion    TEXT,
    estado            TEXT,
    producto_interes  TEXT
);

-- Riesgos
CREATE TABLE IF NOT EXISTS stg_scoring_crediticio (
    id_scoring       INTEGER PRIMARY KEY,
    id_cliente       INTEGER,
    score            INTEGER,
    riesgo           TEXT,
    fecha_calculo    TEXT
);

CREATE TABLE IF NOT EXISTS stg_alertas_fraude (
    id_alerta        INTEGER PRIMARY KEY,
    id_cliente       INTEGER,
    id_cuenta        INTEGER,
    tipo_alerta      TEXT,
    monto            REAL,
    estado           TEXT,
    fecha_deteccion  TEXT
);

CREATE TABLE IF NOT EXISTS stg_incidentes (
    id_incidente     INTEGER PRIMARY KEY,
    id_cliente       INTEGER,
    descripcion      TEXT,
    severidad        TEXT,
    estado           TEXT,
    fecha_incidente  TEXT
);

CREATE TABLE IF NOT EXISTS stg_morosidad (
    id_morosidad     INTEGER PRIMARY KEY,
    id_cliente       INTEGER,
    dias_mora        INTEGER,
    deuda_pendiente  REAL,
    fecha_reporte    TEXT
);

-- Atención al Cliente
CREATE TABLE IF NOT EXISTS stg_tickets (
    id_ticket         INTEGER PRIMARY KEY,
    id_cliente        INTEGER,
    tipo_reclamo      TEXT,
    descripcion       TEXT,
    estado            TEXT,
    fecha_creacion    TEXT,
    fecha_resolucion  TEXT
);

CREATE TABLE IF NOT EXISTS stg_llamadas (
    id_llamada        INTEGER PRIMARY KEY,
    id_cliente        INTEGER,
    duracion_seg      INTEGER,
    resultado         TEXT,
    fecha_llamada     TEXT
);

CREATE TABLE IF NOT EXISTS stg_encuestas (
    id_encuesta       INTEGER PRIMARY KEY,
    id_cliente        INTEGER,
    satisfaccion      INTEGER,
    comentario        TEXT,
    fecha_encuesta    TEXT
);

-- RRHH
CREATE TABLE IF NOT EXISTS stg_empleados (
    id_empleado        INTEGER PRIMARY KEY,
    nombre             TEXT,
    apellido           TEXT,
    cargo              TEXT,
    id_sucursal        INTEGER,
    fecha_contratacion TEXT,
    salario            REAL
);

CREATE TABLE IF NOT EXISTS stg_ausencias (
    id_ausencia        INTEGER PRIMARY KEY,
    id_empleado        INTEGER,
    tipo_ausencia      TEXT,
    dias               INTEGER,
    fecha_inicio       TEXT,
    fecha_fin          TEXT
);

-- Contabilidad
CREATE TABLE IF NOT EXISTS stg_cuentas_contables (
    id_cuenta_contable INTEGER PRIMARY KEY,
    codigo_cuenta      TEXT,
    descripcion        TEXT,
    tipo_cuenta        TEXT
);

CREATE TABLE IF NOT EXISTS stg_asientos_contables (
    id_asiento         INTEGER PRIMARY KEY,
    id_cuenta_contable INTEGER,
    fecha_contable     TEXT,
    tipo_asiento       TEXT,
    monto_debe         REAL,
    monto_haber        REAL,
    descripcion        TEXT
);

CREATE TABLE IF NOT EXISTS stg_presupuesto (
    id_presupuesto     INTEGER PRIMARY KEY,
    id_cuenta_contable INTEGER,
    monto_presupuestado REAL,
    fecha_presupuesto  TEXT
);

CREATE TABLE IF NOT EXISTS stg_salarios_historial (
    id_salario      INTEGER PRIMARY KEY,
    id_empleado     INTEGER,
    salario         REAL,
    fecha_inicio    TEXT,
    fecha_fin       TEXT
);

CREATE TABLE IF NOT EXISTS stg_evaluaciones (
    id_evaluacion   INTEGER PRIMARY KEY,
    id_empleado     INTEGER,
    anio            INTEGER,
    puntaje         INTEGER,
    comentario      TEXT
);

CREATE TABLE IF NOT EXISTS stg_agentes (
    id_agente      INTEGER PRIMARY KEY,
    nombre         TEXT,
    apellido       TEXT,
    id_sucursal    INTEGER
);

CREATE TABLE IF NOT EXISTS stg_sla_tickets (
    id_sla        INTEGER PRIMARY KEY,
    tipo_reclamo  TEXT,
    tiempo_objetivo_horas INTEGER
);

CREATE TABLE IF NOT EXISTS stg_oportunidades (
    id_oportunidad   INTEGER PRIMARY KEY,
    id_cliente       INTEGER,
    producto_interes TEXT,
    fecha_creacion   TEXT,
    estado           TEXT
);