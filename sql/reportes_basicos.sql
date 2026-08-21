-- 📄 Archivo: sql/reportes_basicos.sql
-- Consultas analíticas básicas para Andes Banking AR

-- ============================================================
-- 1. Cantidad de clientes por segmento
-- Responde: ¿Cómo se distribuyen los clientes en los segmentos?
-- ============================================================
SELECT segmento, COUNT(*) AS cantidad_clientes
FROM dim_cliente
GROUP BY segmento
ORDER BY cantidad_clientes DESC;

-- ============================================================
-- 2. Saldo promedio por tipo de cuenta
-- Responde: ¿Cuál es el saldo promedio en cada tipo de cuenta?
-- ============================================================
SELECT tipo_cuenta, 
       ROUND(AVG(saldo), 2) AS saldo_promedio,
       COUNT(*) AS num_cuentas
FROM dim_cuenta
GROUP BY tipo_cuenta
ORDER BY saldo_promedio DESC;

-- ============================================================
-- 3. Transacciones por mes en 2023
-- Responde: ¿Cómo evolucionaron las transacciones mensualmente en 2023?
-- ============================================================
SELECT substr(fecha_completa, 1, 7) AS mes,
       COUNT(*) AS num_transacciones,
       ROUND(SUM(monto), 2) AS monto_total
FROM fact_transacciones
WHERE substr(fecha_completa, 1, 4) = '2023'
GROUP BY mes
ORDER BY mes;

-- ============================================================
-- 4. Top 10 sucursales con más transacciones
-- Responde: ¿Qué sucursales tienen mayor actividad?
-- ============================================================
SELECT s.nombre, s.ciudad, s.provincia, COUNT(*) AS num_transacciones
FROM fact_transacciones f
INNER JOIN dim_sucursal s ON f.id_sucursal_sk = s.id_sucursal_sk
GROUP BY f.id_sucursal_sk
ORDER BY num_transacciones DESC
LIMIT 10;

-- ============================================================
-- 5. Clientes con más de una cuenta
-- Responde: ¿Cuántos clientes tienen múltiples cuentas y cuántas en promedio?
-- ============================================================
SELECT COUNT(*) AS clientes_con_multiples_cuentas
FROM (
    SELECT id_cliente_sk
    FROM dim_cuenta
    GROUP BY id_cliente_sk
    HAVING COUNT(*) > 1
);

-- También podemos ver el número promedio de cuentas por cliente (solo los que tienen al menos 1)
SELECT ROUND(AVG(num_cuentas), 2) AS promedio_cuentas_por_cliente
FROM (
    SELECT id_cliente_sk, COUNT(*) AS num_cuentas
    FROM dim_cuenta
    GROUP BY id_cliente_sk
);

-- ============================================================
-- 6. Monto total de pagos por tipo de pago
-- Responde: ¿Qué tipo de pago genera más movimiento de dinero?
-- ============================================================
SELECT tipo_pago, 
       COUNT(*) AS num_pagos,
       ROUND(SUM(monto), 2) AS monto_total
FROM fact_pagos
GROUP BY tipo_pago
ORDER BY monto_total DESC;

-- ============================================================
-- 7. Transacciones por canal (en 2023)
-- Responde: ¿Qué canal digital es el más utilizado?
-- ============================================================
SELECT c.canal_nombre, COUNT(*) AS num_transacciones,
       ROUND(SUM(f.monto), 2) AS monto_total
FROM fact_transacciones f
INNER JOIN dim_canal c ON f.id_canal_sk = c.id_canal_sk
WHERE substr(f.fecha_completa, 1, 4) = '2023'
GROUP BY c.canal_nombre
ORDER BY num_transacciones DESC;