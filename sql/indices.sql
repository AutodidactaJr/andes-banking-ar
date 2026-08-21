-- 📄 Archivo: sql/indices.sql
-- Índices para optimizar consultas frecuentes

-- Índices en fact_transacciones
CREATE INDEX IF NOT EXISTS idx_ft_fecha ON fact_transacciones(fecha_completa);
CREATE INDEX IF NOT EXISTS idx_ft_cuenta ON fact_transacciones(id_cuenta_sk);
CREATE INDEX IF NOT EXISTS idx_ft_cliente ON fact_transacciones(id_cliente_sk);
CREATE INDEX IF NOT EXISTS idx_ft_canal ON fact_transacciones(id_canal_sk);
CREATE INDEX IF NOT EXISTS idx_ft_tiempo ON fact_transacciones(id_tiempo_sk);

-- Índices en fact_pagos
CREATE INDEX IF NOT EXISTS idx_fp_fecha ON fact_pagos(fecha_completa);
CREATE INDEX IF NOT EXISTS idx_fp_cuenta ON fact_pagos(id_cuenta_sk);
CREATE INDEX IF NOT EXISTS idx_fp_cliente ON fact_pagos(id_cliente_sk);

-- Índices en fact_interacciones_campana
CREATE INDEX IF NOT EXISTS idx_fic_campana ON fact_interacciones_campana(id_campana_sk);
CREATE INDEX IF NOT EXISTS idx_fic_cliente ON fact_interacciones_campana(id_cliente_sk);
CREATE INDEX IF NOT EXISTS idx_fic_tiempo ON fact_interacciones_campana(id_tiempo_sk);

-- Índices en fact_leads
CREATE INDEX IF NOT EXISTS idx_fl_campana ON fact_leads(id_campana_sk);
CREATE INDEX IF NOT EXISTS idx_fl_cliente ON fact_leads(id_cliente_sk);

-- Índices en dimensiones (claves naturales)
CREATE INDEX IF NOT EXISTS idx_dim_cliente_nk ON dim_cliente(id_cliente_nk);
CREATE INDEX IF NOT EXISTS idx_dim_cuenta_nk ON dim_cuenta(id_cuenta_nk);
CREATE INDEX IF NOT EXISTS idx_dim_campana_nk ON dim_campana(id_campana_nk);