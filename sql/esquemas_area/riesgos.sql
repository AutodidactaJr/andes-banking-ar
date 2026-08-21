-- 📄 Archivo: sql/esquemas_area/riesgos.sql
-- Esquema de la base de datos transaccional Riesgos

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS scoring_crediticio (
    id_scoring       INTEGER PRIMARY KEY,
    id_cliente       INTEGER,
    score            INTEGER,
    riesgo           TEXT,
    fecha_calculo    TEXT
);

CREATE TABLE IF NOT EXISTS alertas_fraude (
    id_alerta        INTEGER PRIMARY KEY,
    id_cliente       INTEGER,
    id_cuenta        INTEGER,
    tipo_alerta      TEXT,
    monto            REAL,
    estado           TEXT,
    fecha_deteccion  TEXT
);

CREATE TABLE IF NOT EXISTS incidentes (
    id_incidente     INTEGER PRIMARY KEY,
    id_cliente       INTEGER,
    descripcion      TEXT,
    severidad        TEXT,
    estado           TEXT,
    fecha_incidente  TEXT
);

CREATE TABLE IF NOT EXISTS morosidad (
    id_morosidad     INTEGER PRIMARY KEY,
    id_cliente       INTEGER,
    dias_mora        INTEGER,
    deuda_pendiente  REAL,
    fecha_reporte    TEXT
);