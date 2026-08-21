<p align="center">
  <img src="docs/assets/branding/andes-banking-banner.png" alt="Andes Banking AR - End-to-End Data Platform">
</p>

## 📄 README.md para Andes Banking AR

```markdown
# 🏦 Andes Banking AR

**Data Warehouse on-premise para un banco simulado, construido con Python y SQLite.**

![On-Premise](https://img.shields.io/badge/On--Premise-SQLite%20%2B%20Python-blue)
![ETL](https://img.shields.io/badge/ETL-Python-orange)
![SCD2](https://img.shields.io/badge/SCD%20Tipo%202-Dimensiones-green)
![Calidad](https://img.shields.io/badge/Calidad%20de%20datos-Framework-red)

## 📖 Descripción

Andes Banking AR es un proyecto educativo que simula la modernización de datos de un banco tradicional argentino. La fase on-premise implementa un **Data Warehouse central** que integra datos de seis áreas departamentales:

- 🟢 Core Bancario
- 🟠 CRM / Marketing
- 🔴 Riesgos
- 🟡 Atención al Cliente
- 🔵 RRHH
- ⚫ Contabilidad

Cada área tiene su propia base de datos SQLite (simulando silos transaccionales). Mediante **procesos ETL en Python** se integran en un único Data Warehouse con modelo dimensional Kimball, SCD Tipo 2, limpieza selectiva y auditoría.

## 🏗️ Arquitectura

```
CSV crudos → Bases de datos de área (silos) → Staging → Dimensiones/Hechos → Data Warehouse
```

- **Generadores batch** crean datos sintéticos con errores intencionales.
- **Generadores diarios incrementales** simulan la operación bancaria real.
- **ETL** extrae, transforma y carga los datos en el DW.
- **Framework de calidad** valida staging y DW final.

## 🛠️ Tecnologías

- Python 3.10+
- SQLite 3.x
- Windows CMD
- Git / GitHub

## 📁 Estructura del repositorio

```
andes-banking-ar/
├── docs/                         # Documentación
├── python/etl/                   # Scripts ETL
├── sql/                          # Scripts SQL (esquemas, vistas, calidad)
├── src/andes_bank/generators/    # Generadores de datos
├── run_all.bat                   # Reconstrucción total
└── README.md
```

## 🚀 Cómo reconstruir el proyecto

1. Clonar el repositorio:
   ```cmd
   git clone https://github.com/AutodidactaJr/andes-banking-ar.git
   cd andes-banking-ar
   ```

2. Ejecutar el flujo completo:
   ```cmd
   run_all.bat
   ```

   El batch:
   - Genera datos maestros batch.
   - Carga bases de datos de área.
   - Crea el Data Warehouse.
   - Ejecuta ETL (staging, dimensiones, hechos).
   - Genera datos diarios incrementales.
   - Ejecuta calidad de datos final.

3. Verificar resultados:
   ```
   Data Warehouse final: 0 problemas de calidad.
   ```

## 🧪 Calidad de datos

El framework de calidad valida tanto **staging** (errores crudos esperados) como el **Data Warehouse final** (debe tener 0 problemas). Reglas incluyen:

- Nulos en campos críticos
- Duplicados
- Saldos negativos en cajas de ahorro
- Montos cero en transacciones
- Referencias inexistentes

## 📚 Documentación

- [Modelo de datos](docs/modelo_datos.md)
- [Narrativa de evolución](docs/narrativa_evolucion_etl.md)
- [Linaje de datos](docs/linaje_datos.md)
- [Guía de reconstrucción](docs/guia_reconstruccion.md)
- [Tablas omitidas](docs/tablas_omitidas.md)
- [SQL Server + SSIS](docs/sql_server_ssis.md)
- [Arquitectura AWS](docs/migracion_aws_arquitectura.md)

## 👤 Autor

**AutodidactaJr**  
GitHub: [https://github.com/AutodidactaJr](https://github.com/AutodidactaJr)

## 📝 Licencia

Este proyecto es de uso educativo. Los datos son sintéticos y no representan información real de clientes.
