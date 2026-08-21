-- 📄 Archivo: sql/esquemas_area/rrhh.sql
-- Esquema de la base de datos transaccional RRHH

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS empleados (
    id_empleado        INTEGER PRIMARY KEY,
    nombre             TEXT,
    apellido           TEXT,
    cargo              TEXT,
    id_sucursal        INTEGER,
    fecha_contratacion TEXT,
    salario            REAL
);

CREATE TABLE IF NOT EXISTS ausencias (
    id_ausencia        INTEGER PRIMARY KEY,
    id_empleado        INTEGER,
    tipo_ausencia      TEXT,
    dias               INTEGER,
    fecha_inicio       TEXT,
    fecha_fin          TEXT
);

-- Nuevas tablas
CREATE TABLE IF NOT EXISTS salarios_historial (
    id_salario         INTEGER PRIMARY KEY,
    id_empleado        INTEGER,
    salario            REAL,
    fecha_inicio       TEXT,
    fecha_fin          TEXT,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);

CREATE TABLE IF NOT EXISTS evaluaciones (
    id_evaluacion      INTEGER PRIMARY KEY,
    id_empleado        INTEGER,
    anio               INTEGER,
    puntaje            INTEGER,
    comentario         TEXT,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);