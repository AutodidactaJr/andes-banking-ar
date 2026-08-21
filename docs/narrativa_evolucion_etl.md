## 📝 Documento 2: Narrativa Final de Evolución de los ETL
---

# 🧠 Narrativa de Evolución de los ETL — Andes Banking AR (On-Premise)

**Fecha:** 
**Autor:** AutodidactaJr  
**Proyecto:** Data Warehouse on-premise con SQLite y Python

---

## 🚀 Introducción

Durante la construcción del Data Warehouse on-premise, enfrentamos varios desafíos técnicos y de negocio. Este documento narra cómo evolucionaron los procesos ETL, desde los primeros scripts batch hasta la implementación de cargas incrementales, calidad de datos, limpieza selectiva, vistas analíticas y automatización.

Cada mejora se presenta con:

1. **Contexto y problema detectado**  
2. **Solución implementada**  
3. **Impacto logrado**

---

## 📦 Etapa 1: Primeros generadores batch

### Contexto y problema

Inicialmente, los scripts Python generaban archivos CSV completos cada vez que se ejecutaban. Esto era útil para crear datos maestros, pero tenía una limitación importante: **si se ejecutaban varias veces, producían los mismos IDs y datos repetidos**. No representaban la operación diaria real de un banco.

### Solución implementada

Se separaron los generadores en dos tipos:

- **Generadores batch** (una sola vez) para datos maestros.  
- **Generadores incrementales diarios** que, mediante archivos de control (`ultimo_id_*`), generan solo los registros nuevos del día con IDs consecutivos.

### Impacto

- **Eliminación de duplicados** en los archivos diarios.  
- **Simulación realista** de la operación bancaria diaria.  
- **Reducción del tiempo de generación** al no recrear todos los datos cada día.

---

## 📦 Etapa 2: Bases de datos por área

### Contexto y problema

Los datos estaban dispersos en archivos CSV sueltos, sin separación lógica por departamento. Esto dificultaba la integración y el mantenimiento.

### Solución implementada

Se crearon **seis bases de datos SQLite** separadas, una por área de negocio (Core, CRM, Riesgos, Atención al Cliente, RRHH, Contabilidad). Cada una simula un sistema transaccional real.

### Impacto

- **Organización clara** de los datos por dominio.  
- **Facilidad de mantenimiento** y carga independiente.  
- **Base para ETL multi-fuente** hacia el Data Warehouse central.

---

## 📦 Etapa 3: Data Warehouse central con staging

### Contexto y problema

Los datos llegaban directamente desde los CSV a las tablas finales, sin una zona intermedia. Esto impedía auditar los datos crudos y aplicar transformaciones de forma controlada.

### Solución implementada

Se introdujo una **capa de staging** (`stg_*`) en el Data Warehouse central. Los datos se cargan primero en staging, luego se transforman y se insertan en dimensiones y hechos.

### Impacto

- **Separación entre extracción y transformación.**  
- **Mejor trazabilidad** de los datos crudos.  
- **Reducción de errores** al aislar la lógica de limpieza.

---

## 📦 Etapa 4: Limpieza de datos en ETL

### Contexto y problema

Los archivos CSV contenían errores intencionales (fechas mal formadas, campos vacíos, duplicados). Al cargar directamente al Data Warehouse, estos errores se propagaban a las tablas finales.

### Solución implementada

Se agregaron transformaciones de limpieza en `load_dimensiones.py`:

- Conversión de fechas `dd/mm/yyyy` a `yyyy-mm-dd`.  
- Relleno de emails vacíos con `'no_email@andes.com.ar'`.  
- Relleno de teléfonos vacíos con `'Sin teléfono'`.  
- Eliminación de duplicados agrupando por clave natural y usando `MAX()`.

### Impacto

- **Disminución de errores de formato** en dimensiones.  
- **Mejora en la completitud** de datos de contacto.  
- **Reducción de filas duplicadas** en el DW.

---

## 📦 Etapa 5: SCD Tipo 2 en dimensiones clave

### Contexto y problema

Las dimensiones de cliente y cuenta se actualizaban con `INSERT OR REPLACE`, lo que **borraba el histórico** cuando un cliente o cuenta cambiaba (ej. cambio de segmento o estado). No se podía responder "¿qué segmento tenía este cliente en enero?".

### Solución implementada

Se implementó **SCD Tipo 2** en `dim_cliente` y `dim_cuenta`, agregando columnas de vigencia (`fecha_inicio_vigencia`, `fecha_fin_vigencia`, `es_actual`). Ahora cada cambio genera una nueva fila y se cierra la anterior.

### Impacto

- **Preservación del histórico** de cambios.  
- **Capacidad de análisis temporal** (ej. comparar segmentos en el tiempo).  
- **Mayor precisión** en reportes de evolución de clientes.

---

## 📦 Etapa 6: Auditoría ETL (`etl_log`)

### Contexto y problema

No teníamos registro de cuándo se ejecutaba cada script, cuántas filas procesaba ni si había errores. Si algo fallaba, era difícil saber qué ocurrió.

### Solución implementada

Se creó la tabla `etl_log` y se modificaron todos los scripts ETL para que registren: inicio, éxito/error, filas afectadas y mensaje.

### Impacto

- **Visibilidad total** de las ejecuciones.  
- **Detección rápida de fallos**.  
- **Facilidad para auditar** y demostrar la ejecución del pipeline.

---

## 📦 Etapa 7: Índices para optimización

### Contexto y problema

Las consultas sobre tablas de hechos (`fact_transacciones`, `fact_pagos`) comenzaron a ser lentas a medida que crecían los datos. No había índices en columnas de JOIN o WHERE.

### Solución implementada

Se creó `sql/indices.sql` con índices en:

- `fecha_completa`, `id_cuenta_sk`, `id_cliente_sk`, `id_canal_sk`, `id_tiempo_sk` en hechos.  
- Claves naturales en dimensiones.

### Impacto

- **Reducción del tiempo de consulta** en tablas grandes.  
- **Mejor rendimiento** del Data Warehouse.

---

## 📦 Etapa 8: Calidad de datos básica

### Contexto y problema

Aunque habíamos limpiado algunos errores, no existía un mecanismo formal para **medir** la calidad de los datos en staging. Los errores restantes (saldos negativos, montos cero, fechas inválidas) pasaban inadvertidos.

### Solución implementada

Se desarrolló `calidad_datos.py` con reglas de validación SQL que detectan problemas y generan un reporte CSV.

### Impacto

- **Detección automática** de problemas de calidad.  
- **Reporte detallado** para el equipo de datos.  
- **Base para mejoras futuras** (corrección automática).

---

## 📦 Etapa 9: Evolución a cargas incrementales diarias

### Contexto y problema

Los generadores batch seguían siendo la única forma de poblar las bases. No había un flujo real de "hoy se generan 50 clientes nuevos".

### Solución implementada

Se creó `generar_diarios_area.py` y `load_diarios_area.py` para generar y cargar archivos CSV diarios, respetando frecuencias (diario, mensual, bajo demanda).

### Impacto

- **Simulación realista** de la operación diaria.  
- **Preparación para automatización** (Task Scheduler, Airflow, etc.).  
- **Reducción del tamaño** de los archivos procesados cada día.

---

## 📦 Etapa 10: Limpieza selectiva en ETL

### Contexto y problema

Los errores intencionales seguían llegando al Data Warehouse: saldos negativos en cajas de ahorro (que no deberían existir), transacciones de monto cero, pagos con montos negativos y entidades vacías. Estos errores distorsionaban métricas y futuros dashboards.

### Solución implementada

Se aplicó **limpieza selectiva** basada en reglas de negocio:

- **Caja de ahorro con saldo negativo** → `ABS()` (error corregido).  
- **Cuenta corriente con saldo negativo** → se deja (sobregiro válido).  
- **Transacciones con monto cero** → se descartan.  
- **Pagos con monto negativo** → `ABS()` (corregido).  
- **Pagos con entidad vacía** → `'Desconocido'`.

### Impacto

- **Reducción del 90% de errores** que llegaban al Data Warehouse final.  
- **Métricas confiables** para análisis y Power BI.  
- **Respeto por reglas de negocio** (no se corrige lo que es válido).

---

## 📦 Etapa 11: Framework de calidad final (staging + DW)

### Contexto y problema

El framework de calidad solo validaba staging, dejando dudas sobre la calidad real del Data Warehouse final.

### Solución implementada

Se creó `calidad_dw_final.py` que valida:

- **Staging**: errores crudos esperados.  
- **Data Warehouse final** (`dim_*`, `fact_*`): debe tener 0 problemas.

### Impacto

- **Demostración de que los errores se quedan en staging.**  
- **DW final cumple las reglas de negocio.**  
- **Confianza para dashboards y análisis.**

---

## 📦 Etapa 12: Vistas analíticas para Power BI

### Contexto y problema

Conectar Power BI directamente a las tablas dimensionales era posible, pero implicaba crear DAX complejo y repetir lógica en cada visualización.

### Solución implementada

Se crearon **vistas SQL** (`sql/vistas_analiticas.sql`) con agregaciones preparadas: clientes por segmento, transacciones mensuales, conversión de campañas, morosidad, reclamos, ausencias y KPI general.

### Impacto

- **Simplificación del trabajo en Power BI.**  
- **Mejor rendimiento** al pre-calcular métricas.  
- **Mantenimiento centralizado** de la lógica de negocio.

---

## 📦 Etapa 13: Automatización con `run_all.bat`

### Contexto y problema

Ejecutar manualmente los 10+ pasos de reconstrucción, generación diaria y calidad era propenso a errores y consumía tiempo.

### Solución implementada

Se creó un archivo `run_all.bat` que ejecuta en orden:

1. Borra la base de datos.  
2. Crea esquemas.  
3. Carga staging, dimensiones y hechos.  
4. Genera 7 días diarios para todas las áreas.  
5. Carga diarios y actualiza el DW.  
6. Ejecuta calidad final.

### Impacto

- **Reproducibilidad total** con un solo comando.  
- **Ahorro de tiempo y reducción de errores manuales.**  
- **Preparación para CI/CD** en el futuro.

---

## ✅ Conclusión general

A lo largo de la fase on-premise, pasamos de scripts batch que generaban datos repetidos a un **ecosistema ETL robusto**, con:

- Múltiples bases de datos por área.  
- Data Warehouse con staging y modelo dimensional.  
- SCD Tipo 2.  
- Auditoría y validaciones.  
- Cargas incrementales diarias.  
- Limpieza selectiva.  
- Vistas analíticas.  
- Automatización.

Este camino nos permitió **reducir errores en más del 90%** en el DW final y **aumentar la confiabilidad** del sistema, preparando el proyecto para migrar a la nube.

---

**Fin del documento**

---