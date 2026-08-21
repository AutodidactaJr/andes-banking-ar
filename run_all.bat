@echo off
cd /d C:\Users\nahu9\Documents\Andes-banking-ar

echo ============================================================
echo  RECONSTRUCCION TOTAL - ANDES BANKING AR
echo ============================================================

echo.
echo [1/11] Creando carpetas necesarias...
if not exist data\raw\core_bancario\plazos_fijos mkdir data\raw\core_bancario\plazos_fijos
if not exist data\raw\core_bancario\seguros mkdir data\raw\core_bancario\seguros
if not exist data\raw\rrhh\salarios_historial mkdir data\raw\rrhh\salarios_historial
if not exist data\raw\rrhh\evaluaciones mkdir data\raw\rrhh\evaluaciones
if not exist data\raw\atencion_cliente\agentes mkdir data\raw\atencion_cliente\agentes
if not exist data\raw\atencion_cliente\sla_tickets mkdir data\raw\atencion_cliente\sla_tickets
if not exist data\raw\crm\oportunidades mkdir data\raw\crm\oportunidades
if not exist data\control mkdir data\control

echo.
echo [2/11] Generando datos maestros batch...
python -m src.andes_bank.generators.generar_clientes
python -m src.andes_bank.generators.generar_sucursales
python -m src.andes_bank.generators.generar_cuentas
python -m src.andes_bank.generators.generar_tarjetas
python -m src.andes_bank.generators.generar_prestamos
python -m src.andes_bank.generators.generar_transacciones
python -m src.andes_bank.generators.generar_pagos
python -m src.andes_bank.generators.generar_plazos_fijos
python -m src.andes_bank.generators.generar_seguros
python -m src.andes_bank.generators.generar_campanas
python -m src.andes_bank.generators.generar_interacciones
python -m src.andes_bank.generators.generar_leads
python -m src.andes_bank.generators.generar_oportunidades
python -m src.andes_bank.generators.generar_riesgos
python -m src.andes_bank.generators.generar_atencion_cliente
python -m src.andes_bank.generators.generar_agentes
python -m src.andes_bank.generators.generar_sla_tickets
python -m src.andes_bank.generators.generar_rrhh
python -m src.andes_bank.generators.generar_salarios_historial
python -m src.andes_bank.generators.generar_evaluaciones
python -m src.andes_bank.generators.generar_contabilidad

echo.
echo [3/11] Cargando CSV maestros a bases de area...
python python/etl/load_area_core.py
python python/etl/load_area_crm.py
python python/etl/load_area_riesgos.py
python python/etl/load_area_atencion.py
python python/etl/load_area_rrhh.py
python python/etl/load_area_contabilidad.py

echo.
echo [4/11] Borrando base de datos actual...
if exist data\andes_dw.db del /q data\andes_dw.db

echo.
echo [5/11] Creando esquema (staging, dimensiones, hechos, auditoria, indices)...
sqlite3 data\andes_dw.db ".read sql/staging.sql"
sqlite3 data\andes_dw.db ".read sql/dw_completo.sql"
sqlite3 data\andes_dw.db ".read sql/etl_log.sql"
sqlite3 data\andes_dw.db ".read sql/indices.sql"

echo.
echo [6/11] Cargando staging...
python python/etl/load_staging.py

echo.
echo [7/11] Cargando dimensiones con limpieza selectiva y SCD2...
python python/etl/load_dimensiones.py

echo.
echo [8/11] Cargando hechos...
python python/etl/load_hechos.py

echo.
echo [9/11] Generando datos diarios para todas las areas (7 dias retroactivos)...
python -m src.andes_bank.generators.generar_diarios_area --area core --dias 7
python -m src.andes_bank.generators.generar_diarios_area --area crm --dias 7
python -m src.andes_bank.generators.generar_diarios_area --area riesgos --dias 7
python -m src.andes_bank.generators.generar_diarios_area --area atencion --dias 7
python -m src.andes_bank.generators.generar_diarios_area --area rrhh --dias 7
python -m src.andes_bank.generators.generar_diarios_area --area contabilidad --dias 7

echo.
echo [10/11] Cargando archivos diarios y actualizando Data Warehouse...
python python/etl/load_diarios_area.py
python python/etl/load_staging.py
python python/etl/load_dimensiones.py
python python/etl/load_hechos.py

echo.
echo [11/11] Ejecutando calidad de datos final...
python python/etl/calidad_dw_final.py

echo.
echo ============================================================
echo  PROCESO COMPLETADO EXITOSAMENTE
echo ============================================================
pause