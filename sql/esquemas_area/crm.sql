-- 📄 Archivo: sql/esquemas_area/crm.sql
-- Esquema de la base de datos transaccional CRM

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS campanas (
    id_campana        INTEGER PRIMARY KEY,
    nombre            TEXT,
    canal             TEXT,
    segmento_objetivo TEXT,
    fecha_inicio      TEXT,
    fecha_fin         TEXT,
    costo             REAL
);

CREATE TABLE IF NOT EXISTS interacciones (
    id_interaccion    INTEGER PRIMARY KEY,
    id_campana        INTEGER,
    id_cliente        INTEGER,
    fecha             TEXT,
    tipo_interaccion  TEXT,
    dispositivo       TEXT,
    FOREIGN KEY (id_campana) REFERENCES campanas(id_campana)
);

CREATE TABLE IF NOT EXISTS leads (
    id_lead           INTEGER PRIMARY KEY,
    id_campana        INTEGER,
    id_cliente        INTEGER,
    fecha_creacion    TEXT,
    estado            TEXT,
    producto_interes  TEXT,
    FOREIGN KEY (id_campana) REFERENCES campanas(id_campana)
);

CREATE TABLE IF NOT EXISTS oportunidades (
    id_oportunidad    INTEGER PRIMARY KEY,
    id_cliente        INTEGER,
    producto_interes  TEXT,
    fecha_creacion    TEXT,
    estado            TEXT
);