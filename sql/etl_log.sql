-- 📄 Archivo: sql/etl_log.sql
-- Tabla de auditoría para registrar ejecuciones ETL

CREATE TABLE IF NOT EXISTS etl_log (
    id_log         INTEGER PRIMARY KEY AUTOINCREMENT,
    script         TEXT NOT NULL,
    fecha_ejecucion TEXT NOT NULL,
    filas_afectadas INTEGER DEFAULT 0,
    estado         TEXT NOT NULL,   -- 'EXITO' o 'ERROR'
    mensaje        TEXT
);