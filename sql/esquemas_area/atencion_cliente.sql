-- 📄 Archivo: sql/esquemas_area/atencion_cliente.sql
-- Esquema de la base de datos transaccional Atención al Cliente

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS tickets (
    id_ticket         INTEGER PRIMARY KEY,
    id_cliente        INTEGER,
    tipo_reclamo      TEXT,
    descripcion       TEXT,
    estado            TEXT,
    fecha_creacion    TEXT,
    fecha_resolucion  TEXT
);

CREATE TABLE IF NOT EXISTS llamadas (
    id_llamada        INTEGER PRIMARY KEY,
    id_cliente        INTEGER,
    duracion_seg      INTEGER,
    resultado         TEXT,
    fecha_llamada     TEXT
);

CREATE TABLE IF NOT EXISTS encuestas (
    id_encuesta       INTEGER PRIMARY KEY,
    id_cliente        INTEGER,
    satisfaccion      INTEGER,
    comentario        TEXT,
    fecha_encuesta    TEXT
);

-- Nuevas tablas
CREATE TABLE IF NOT EXISTS agentes (
    id_agente         INTEGER PRIMARY KEY,
    nombre            TEXT,
    apellido          TEXT,
    id_sucursal       INTEGER,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal) -- opcional, no ejecutar si no existe sucursales en esta base
);

CREATE TABLE IF NOT EXISTS sla_tickets (
    id_sla            INTEGER PRIMARY KEY,
    tipo_reclamo      TEXT,
    tiempo_objetivo_horas INTEGER
);