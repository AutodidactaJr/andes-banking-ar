## 📄 Documento 3: Tablas Omitidas en la Fase On-Premise
---

# 📋 Tablas Omitidas en la Simulación On-Premise

**Versión:** 1.0  
**Fecha:** 
**Autor:** AutodidactaJr  
**Proyecto:** Andes Banking AR

---

## 1. Introducción

En la fase on-premise, simulamos las bases de datos de las áreas principales del banco. Sin embargo, un banco real tiene **muchas más tablas** en cada sistema transaccional. Omitimos deliberadamente algunas para:

- Mantener el alcance manejable para aprendizaje.
- Evitar saturar el proyecto con tablas de bajo valor analítico.
- Enfocar la práctica en integración de silos y modelado dimensional.
- Optimizar recursos del hardware local (4 GB RAM, HDD).

Este documento lista las tablas omitidas, justifica su exclusión y describe cómo se incorporarían en una versión más completa o en la nube.

---

## 2. Tablas omitidas por área

### 🟢 Core Bancario

| Tabla omitida | Razón de omisión | Valor si se agrega |
|---------------|------------------|--------------------|
| `plazos_fijos` | No era esencial para practicar ETL básico | Análisis de inversiones |
| `seguros` | Amplitud excesiva para el MVP | Ventas cruzadas |
| `inversiones` | Complejidad adicional | Portafolio de clientes |
| `parametros_tasas` | Configuración interna | Simulación de tasas |
| `auditoria_core` | Redundante con `etl_log` | Trazabilidad fina |
| `usuarios_sistema` | Seguridad operativa | Gestión de accesos |

### 🟠 CRM / Marketing

| Tabla omitida | Razón de omisión | Valor si se agrega |
|---------------|------------------|--------------------|
| `oportunidades` | Requiere pipeline de ventas | Análisis de conversión |
| `segmentos_definidos` | Ya se maneja en atributos | Segmentación formal |
| `actividades` | Detalle operativo excesivo | Historial de contacto |
| `presupuesto_marketing` | No necesario para el DW | Control de gastos |

### 🔴 Riesgos

| Tabla omitida | Razón de omisión | Valor si se agrega |
|---------------|------------------|--------------------|
| `modelos_riesgo` | Definición técnica | Explicabilidad |
| `variables_modelo` | Datos intermedios | Auditoría de scoring |
| `polizas_riesgo` | Operación específica | Coberturas |
| `seguimiento_alertas` | Gestión de casos | Control de fraude |

### 🟡 Atención al Cliente

| Tabla omitida | Razón de omisión | Valor si se agrega |
|---------------|------------------|--------------------|
| `agentes` | Requiere RRHH | Productividad |
| `cola_tickets` | Asignación interna | Eficiencia |
| `historial_reclamos` | Seguimiento detallado | Trazabilidad |
| `acuerdos_servicio` | SLA | Cumplimiento |

### 🔵 RRHH

| Tabla omitida | Razón de omisión | Valor si se agrega |
|---------------|------------------|--------------------|
| `salarios_historial` | Historial de cambios | Análisis de costos |
| `evaluaciones` | Desempeño | Talento |
| `vacaciones` | Planificación | Ausentismo |
| `formacion` | Capacitación | Desarrollo |
| `nominas` | Pago mensual | Costo laboral |

### ⚫ Contabilidad

| Tabla omitida | Razón de omisión | Valor si se agrega |
|---------------|------------------|--------------------|
| `facturas` | Proceso comercial | Cuentas por cobrar/pagar |
| `centros_costo` | Asignación interna | Rentabilidad por área |
| `impuestos` | Cumplimiento fiscal | Provisión |
| `conciliaciones` | Control bancario | Integridad |

---

## 3. Criterios generales de omisión

1. **Valor analítico bajo**  
   Tablas puramente operativas o de configuración no aportan a los KPIs.

2. **Complejidad de generación**  
   Algunas tablas requerirían generadores más complejos sin beneficio educativo inmediato.

3. **Redundancia con otras tablas**  
   Ej. `auditoria_core` se solapa con `etl_log`.

4. **Limitaciones de hardware**  
   Más tablas → más tiempo de procesamiento y almacenamiento.

5. **Enfoque en integración**  
   Preferimos consolidar 6 áreas con pocas tablas, que practicar una sola área exhaustivamente.

---

## 4. Cómo se incorporarían en una versión completa

### En una fase on-premise ampliada

- **Agregar tablas priorizadas** (plazos fijos, seguros, agentes, salarios_historial).
- **Crear generadores batch para cada nueva tabla**.
- **Actualizar esquemas SQL** (`area.sql`).
- **Modificar scripts de carga** (`load_area_*.py`).
- **Extender el Data Warehouse** con nuevas dimensiones/hechos si aportan a KPIs.
- **Actualizar calidad y documentación**.

### En la nube (AWS/Azure + Databricks)

- **Realismo extremo**: crear todas las tablas que un banco real tendría.
- **Procesamiento distribuido** permite manejar mayor volumen.
- **Ingesta desde múltiples fuentes** (APIs, streaming, archivos) sin afectar la PC local.
- **Data Lakehouse** con Delta Lake para gobernar y consultar eficientemente.

---

## 5. Conclusión

La omisión de tablas fue una decisión deliberada para mantener el alcance educativo y técnico. Sin embargo, el diseño modular del proyecto permite **agregar nuevas tablas de forma incremental** sin romper lo existente. En una futura versión cloud, se puede ampliar el sistema a realismo extremo.

---

**Fin del documento**

---