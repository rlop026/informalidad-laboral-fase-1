# EPHC Paraguay — Informalidad laboral juvenil

Este repositorio reproduce el análisis de determinantes de la informalidad laboral juvenil en Paraguay a partir de la Encuesta Permanente de Hogares Continua (EPHC) del INE. El flujo está orientado a la limpieza, unificación, validación y exportación de un dataset listo para análisis exploratorio y modelado posterior.

## Objetivo del proyecto

- Reproducir la preparación de los archivos `.SAV` del INE.
- Unificar trimestres de la EPHC en un dataset consistente.
- Definir y documentar las decisiones de limpieza en una bitácora.
- Generar un dataset analítico para estudiar la informalidad laboral entre personas ocupadas no agropecuarias de 18 a 29 años.
- Mantener un cuaderno de análisis reproducible (`notebooks/Fase1_Informalidad_Juvenil.ipynb`) con resultados, gráficos y hallazgos.

## Pregunta de investigación

¿Qué factores se asocian con la probabilidad de que una persona ocupada no agropecuaria de 18 a 29 años en Paraguay tenga un empleo informal, y cuál es el peso relativo de los atributos individuales, la estructura del puesto de trabajo, el territorio y el contexto del hogar?

## Fuente de datos

- Instituto Nacional de Estadística (INE) de Paraguay
- Encuesta Permanente de Hogares Continua (EPHC)
- Base REG02, trimestres de 2024 a 2026
- Población analítica: personas ocupadas no agropecuarias de 18 a 29 años

## Estructura del repositorio

```text
ephc_reproducible/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                          # Archivos .SAV originales del INE
│   ├── raw_csv/                      # Archivos convertidos a CSV
│   └── clean/                        # Datasets limpios y procesados
├── docs/
├── notebooks/
│   └── Fase1_Informalidad_Juvenil.ipynb
├── output/                           # Resultados, tablas y gráficos exportados
├── scripts/
│   └── convert_sav_to_csv.py
├── src/
│   └── convert_sav_to_csv.py
└── contexto_proyecto_informalidad_juvenil.md
```

## Requisitos

- Python 3.10+
- pip
- Entorno virtual recomendado
- Archivos `.SAV` descargados en `data/raw/`

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# o .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Preparación de datos

Colocar los archivos originales `.SAV` en:

```text
data/raw/
```

## Flujo de reproducción

### 1) Convertir archivos `.SAV` a `.csv`

```bash
python src/convert_sav_to_csv.py --input data/raw --output data/raw_csv
```

Esto crea una copia en CSV manteniendo el contenido original sin transformar los valores.

### 2) Ejecutar el notebook principal

Abrir y ejecutar en orden:

```text
notebooks/Fase1_Informalidad_Juvenil.ipynb
```

El notebook incluye:

- inventario de archivos
- validación de variables compartidas
- apilamiento de trimestres
- limpieza y recodificación
- diagnóstico exploratorio
- comparación de asociaciones por dimensión
- exportación de resultados y bitácora

### 3) Exportar resultados finales

El notebook genera salidas como:

- `output/dataset_limpio.csv`
- `output/bitacora_limpieza.csv`
- gráficos y tablas analíticas en `output/`

## Outputs esperados

Tras ejecutar la preparación y el notebook, se espera producir al menos:

- dataset consolidado limpio para análisis
- bitácora de decisiones de limpieza
- visualizaciones de exploración descriptiva
- resumen de asociaciones y variables relevantes

## Dependencias

Ver archivo `requirements.txt`.

## Principales decisiones de limpieza

La limpieza del proyecto incluye decisiones documentadas como:

- conversión de códigos de no respuesta a nulos
- descarte de registros fuera del universo de análisis
- resolución del panel rotativo conservando la primera aparición por persona
- agregados del hogar para medir contexto del hogar
- recodificación de variables relevantes para la estructura del puesto y la informalidad
- validación de variables antes de la concatenación de archivos

## Notas metodológicas

- La conversión de `.SAV` a CSV es solo de formato; no modifica los valores.
- La limpieza se basa en criterios estadísticos y documentales del proyecto.
- El notebook se diseñó para reproducir de forma transparente todo el proceso, con registro de decisiones y resultados.
- Los trabajos de análisis posterior pueden continuar con regresión logística, chi-cuadrado, pruebas no paramétricas y bootstrapping.

## Reproducibilidad en Jupyter/Colab

Para reproducir el análisis en un entorno local o en Google Colab:

1. Asegurarse de que los archivos `.SAV` estén en `data/raw/`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Abrir el notebook: `notebooks/Fase1_Informalidad_Juvenil.ipynb`
4. Ejecutar las celdas en orden
5. Revisar los resultados exportados en `output/`

**Nota para Colab:** el notebook puede detectar una carpeta compartida en Google Drive y usarla como entrada si existe; si no, trabaja con el almacenamiento local de la sesión.

## Documentación adicional

- `contexto_proyecto_informalidad_juvenil.md`: contexto del proyecto, objetivo, decisiones metodológicas y guía de continuidad.
- `docs/`: puede alojar reportes, tablas y documentación complementaria.