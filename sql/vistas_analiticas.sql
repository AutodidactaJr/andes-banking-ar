-- 📄 Archivo: sql/vistas_analiticas.sql
-- Vistas analíticas para Power BI

-- ============================================================
-- Vista 1: Clientes por segmento y provincia
-- ============================================================
CREATE VIEW IF NOT EXISTS v_clientes_segmento AS
SELECT
    cl.segmento,
    cl.provincia,
    COUNT(DISTINCT cl.id_cliente_sk) AS cantidad_clientes
FROM dim_cliente cl
WHERE cl.es_actual = 1
GROUP BY cl.segmento, cl.provincia;

-- ============================================================
-- Vista 2: Transacciones mensuales por canal
-- ============================================================
CREATE VIEW IF NOT EXISTS v_transacciones_mensuales AS
SELECT
    ti.anio,
    ti.mes,
    ca.canal_nombre,
    COUNT(*) AS num_transacciones,
    ROUND(SUM(ft.monto), 2) AS monto_total
FROM fact_transacciones ft
INNER JOIN dim_tiempo ti ON ft.id_tiempo_sk = ti.id_tiempo_sk
INNER JOIN dim_canal ca ON ft.id_canal_sk = ca.id_canal_sk
GROUP BY ti.anio, ti.mes, ca.canal_nombre;

-- ============================================================
-- Vista 3: Conversión de campañas
-- ============================================================
CREATE VIEW IF NOT EXISTS v_campanas_conversion AS
SELECT
    dc.nombre AS campana,
    dc.canal,
    dc.segmento_objetivo,
    COUNT(DISTINCT fic.id_interaccion_sk) AS total_interacciones,
    SUM(CASE WHEN fic.tipo_interaccion = 'Conversión' THEN 1 ELSE 0 END) AS conversiones,
    ROUND(
        (SUM(CASE WHEN fic.tipo_interaccion = 'Conversión' THEN 1 ELSE 0 END) * 100.0) 
        / NULLIF(COUNT(DISTINCT fic.id_interaccion_sk), 0), 2
    ) AS tasa_conversion
FROM fact_interacciones_campana fic
INNER JOIN dim_campana dc ON fic.id_campana_sk = dc.id_campana_sk
GROUP BY dc.id_campana_sk, dc.nombre, dc.canal, dc.segmento_objetivo;

-- ============================================================
-- Vista 4: Morosidad y riesgo
-- ============================================================
CREATE VIEW IF NOT EXISTS v_morosidad_riesgo AS
SELECT
    cl.id_cliente_sk,
    cl.nombre,
    cl.apellido,
    mo.dias_mora,
    mo.deuda_pendiente,
    sc.riesgo,
    sc.score
FROM dim_cliente cl
LEFT JOIN (
    SELECT id_cliente_sk, MAX(dias_mora) AS dias_mora, MAX(deuda_pendiente) AS deuda_pendiente
    FROM fact_morosidad
    GROUP BY id_cliente_sk
) mo ON cl.id_cliente_sk = mo.id_cliente_sk
LEFT JOIN (
    SELECT id_cliente_sk, MAX(score) AS score, MAX(riesgo) AS riesgo
    FROM fact_scoring_crediticio
    GROUP BY id_cliente_sk
) sc ON cl.id_cliente_sk = sc.id_cliente_sk
WHERE cl.es_actual = 1;

-- ============================================================
-- Vista 5: Reclamos por tipo y sucursal
-- ============================================================
CREATE VIEW IF NOT EXISTS v_reclamos_resumen AS
SELECT
    su.nombre AS sucursal,
    tr.tipo_reclamo_nombre,
    COUNT(*) AS num_reclamos,
    ROUND(AVG(fr.resolucion_dias), 2) AS promedio_resolucion
FROM fact_reclamos fr
INNER JOIN dim_cliente cl ON fr.id_cliente_sk = cl.id_cliente_sk
LEFT JOIN dim_sucursal su ON fr.id_sucursal_sk = su.id_sucursal_sk
INNER JOIN dim_tipo_reclamo tr ON fr.id_tipo_reclamo_sk = tr.id_tipo_reclamo_sk
GROUP BY su.nombre, tr.tipo_reclamo_nombre;

-- ============================================================
-- Vista 6: Ausencias por sucursal
-- ============================================================
CREATE VIEW IF NOT EXISTS v_ausencias_empleados AS
SELECT
    su.nombre AS sucursal,
    COUNT(*) AS num_ausencias,
    SUM(fa.dias) AS total_dias
FROM fact_ausencias fa
INNER JOIN dim_empleado de ON fa.id_empleado_sk = de.id_empleado_sk
LEFT JOIN dim_sucursal su ON de.id_sucursal_sk = su.id_sucursal_sk
GROUP BY su.nombre;

-- ============================================================
-- Vista 7: KPI general para resumen ejecutivo
-- ============================================================
CREATE VIEW IF NOT EXISTS v_kpi_general AS
SELECT
    (SELECT COUNT(DISTINCT id_cliente_sk) FROM dim_cliente WHERE es_actual = 1) AS total_clientes,
    (SELECT COUNT(*) FROM fact_transacciones) AS total_transacciones,
    (SELECT ROUND(SUM(monto), 2) FROM fact_transacciones) AS monto_total,
    (SELECT ROUND(AVG(saldo), 2) FROM dim_cuenta WHERE es_actual = 1) AS saldo_promedio,
    (SELECT ROUND((SUM(CASE WHEN tipo_interaccion = 'Conversión' THEN 1 ELSE 0 END) * 100.0) / NULLIF(COUNT(*), 0), 2) 
     FROM fact_interacciones_campana) AS tasa_conversion_general;