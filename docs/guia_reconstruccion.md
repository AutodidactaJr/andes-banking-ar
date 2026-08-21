## 📄 Documento 5: Guía de Reconstrucción desde Cero
---

# 🔄 Guía de Reconstrucción desde Cero — Andes Banking AR

**Versión:** 1.0  
**Fecha:**  
**Autor:** AutodidactaJr  
**Objetivo:** Explicar paso a paso cómo reconstruir todo el sistema on-premise desde cero, ya sea manualmente o usando el archivo de automatización.

---

## 1. Introducción

Esta guía describe cómo reconstruir el Data Warehouse de Andes Banking AR partiendo de una carpeta vacía o después de borrar los datos generados. El proceso consta de dos grandes fases:

1. **Carga inicial (maestros)**  
   Generar datos sintéticos batch y cargarlos en las bases de datos de área.

2. **Integración al Data Warehouse**  
   Extraer desde las bases de área, transformar y cargar en `andes_dw.db`.

Al final, ejecutamos el framework de calidad para verificar que todo quedó correcto.

---

## 2. Requisitos previos

- Python 3.10+ instalado.
- SQLite CLI (`sqlite3`) instalado y en el PATH.
- Carpeta del proyecto con la estructura correcta.
- Los generadores batch y diarios ya creados.
- Las bases de datos de área vacías o inexistentes.

---

## 3. Método 1: Automático con `run_all.bat`

### 3.1 Contenido del archivo

En la raíz del proyecto debe existir `run_all.bat`. Si no lo tienes, créalo con el contenido proporcionado anteriormente.

### 3.2 Ejecución

Abre CMD en la raíz del proyecto:

```cmd
cd C:\Users\nahu9\Documents\Andes-banking-ar
run_all.bat
```

### 3.3 Qué hace el archivo

1. Borra `andes_dw.db` si existe.
2. Crea las tablas staging, dimensiones y hechos.
3. Carga los datos maestros desde las bases de área a staging.
4. Carga dimensiones y hechos.
5. Genera 7 días diarios para todas las áreas.
6. Carga los diarios a las bases de área.
7. Actualiza el Data Warehouse con los diarios.
8. Ejecuta `calidad_dw_final.py`.

### 3.4 Ventajas

- Un solo comando.
- Orden garantizado.
- Reduce errores manuales.

---

## 4. Método 2: Manual paso a paso

Si prefieres controlar cada etapa, sigue estos pasos.

### 4.1 Paso 1: Generar datos maestros batch

Ejecuta los generadores batch en orden:

```cmd
python -m src.andes_bank.generators.generar_clientes
python -m src.andes_bank.generators.generar_sucursales
python -m src.andes_bank.generators.generar_cuentas
python -m src.andes_bank.generators.generar_tarjetas
python -m src.andes_bank.generators.generar_prestamos
python -m src.andes_bank.generators.generar_transacciones
python -m src.andes_bank.generators.generar_pagos
python -m src.andes_bank.generators.generar_campanas
python -m src.andes_bank.generators.generar_interacciones
python -m src.andes_bank.generators.generar_leads
python -m src.andes_bank.generators.generar_riesgos
python -m src.andes_bank.generators.generar_atencion_cliente
python -m src.andes_bank.generators.generar_rrhh
python -m src.andes_bank.generators.generar_contabilidad
```

### 4.2 Paso 2: Cargar CSV maestros a bases de área

```cmd
python python/etl/load_area_core.py
python python/etl/load_area_crm.py
python python/etl/load_area_riesgos.py
python python/etl/load_area_atencion.py
python python/etl/load_area_rrhh.py
python python/etl/load_area_contabilidad.py
```

### 4.3 Paso 3: Crear esquema del Data Warehouse

```cmd
del data\andes_dw.db
sqlite3 data\andes_dw.db ".read sql/staging.sql"
sqlite3 data\andes_dw.db ".read sql/dw_completo.sql"
sqlite3 data\andes_dw.db ".read sql/etl_log.sql"
sqlite3 data\andes_dw.db ".read sql/indices.sql"
```

### 4.4 Paso 4: Cargar staging

```cmd
python python/etl/load_staging.py
```

### 4.5 Paso 5: Cargar dimensiones

```cmd
python python/etl/load_dimensiones.py
```

### 4.6 Paso 6: Cargar hechos

```cmd
python python/etl/load_hechos.py
```

### 4.7 Paso 7: Generar datos diarios para todas las áreas (opcional)

```cmd
python -m src.andes_bank.generators.generar_diarios_area --area core --dias 7
python -m src.andes_bank.generators.generar_diarios_area --area crm --dias 7
python -m src.andes_bank.generators.generar_diarios_area --area riesgos --dias 7
python -m src.andes_bank.generators.generar_diarios_area --area atencion --dias 7
python -m src.andes_bank.generators.generar_diarios_area --area rrhh --dias 7
python -m src.andes_bank.generators.generar_diarios_area --area contabilidad --dias 7
```

### 4.8 Paso 8: Cargar diarios a bases de área

```cmd
python python/etl/load_diarios_area.py
```

### 4.9 Paso 9: Actualizar DW con diarios

```cmd
python python/etl/load_staging.py
python python/etl/load_dimensiones.py
python python/etl/load_hechos.py
```

### 4.10 Paso 10: Ejecutar calidad final

```cmd
python python/etl/calidad_dw_final.py
```

---

## 5. Verificación

Después de la reconstrucción, verifica:

- La base `andes_dw.db` existe.
- Las tablas `dim_*` y `fact_*` tienen datos.
- El reporte de calidad final muestra **0 problemas en el DW**.
- La tabla `etl_log` registra todas las ejecuciones.

Consulta rápida de conteos:

```cmd
sqlite3 data/andes_dw.db "SELECT 'dim_cliente' AS tabla, COUNT(*) FROM dim_cliente WHERE es_actual=1 UNION ALL SELECT 'fact_transacciones', COUNT(*) FROM fact_transacciones;"
```

---

## 6. Solución de problemas comunes

| Error | Posible causa | Solución |
|-------|---------------|----------|
| `no such table: stg_clientes` | No se ejecutó `staging.sql` | Ejecuta de nuevo el script SQL |
| `unable to open database file` | La carpeta `data` no existe o falta permiso | Crea la carpeta |
| `ModuleNotFoundError` | No se está en la raíz del proyecto | `cd` a la carpeta correcta |
| `FOREIGN KEY constraint failed` | FKs activas durante carga masiva | Asegurar `PRAGMA foreign_keys = OFF` en scripts |
| `No such file: ...csv` | Faltan generadores batch | Ejecutar generadores batch primero |

---

## 7. Conclusión

Con esta guía, cualquier persona puede reconstruir Andes Banking AR desde cero, ya sea automáticamente con `run_all.bat` o manualmente paso a paso. Esto garantiza reproducibilidad y profesionalismo.

---

**Fin del documento**

---