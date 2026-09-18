# EPHC Paraguay — Repositorio de reproducción

Este repositorio está pensado para reproducir la limpieza y transformación de los archivos `.SAV` del EPHC del INE, siguiendo el flujo de trabajo del proyecto.

## Objetivo

- Convertir archivos `.SAV` a `.csv` sin modificar los datos.
- Unificar y limpiar los registros de diferentes trimestres.
- Generar un dataset final listo para análisis.
- Mantener una bitácora de decisiones de limpieza.

## Estructura del proyecto

```text
ephc_reproducible/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/                          # Archivos .SAV originales del INE
│   ├── raw_csv/                      # Archivos convertidos a CSV
│   └── clean/                        # Dataset limpios y procesados
├── notebooks/
│   └── Fase1_Herencia_Informalidad.ipynb
├── src/                              # Scripts y módulos reutilizables
│   ├── convert_sav_to_csv.py
│   └── 03_limpieza.py
├── output/                           # Resultados y gráficos generados
└── docs/                             # Documentación del proyecto
```

## Requisitos

- Python 3.10+
- pip
- Entorno virtual recomendado

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# o .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Preparación de datos

Colocá los archivos `.SAV` originales dentro de:

```text
data/raw/
```

## Flujo de reproducción

### 1) Convertir .SAV a .csv

```bash
python src/convert_sav_to_csv.py --input data/raw --output data/raw_csv
```

### 2) Ejecutar la limpieza principal

```bash
python src/03_limpieza.py data/raw data/clean
```

Esto generará:

- `data/clean/dataset_limpio.csv`
- `data/clean/bitacora_limpieza.csv`

## Dependencias

Ver archivo `requirements.txt`.

## Notas

- La conversión a CSV es solo de formato; no modifica los valores.
- La limpieza del dataset se hace con criterio estadístico y documental según el protocolo del proyecto.
- Si querés trabajar con un cuaderno interactivo, podés usar `Fase1_Herencia_Informalidad.ipynb` en la carpeta `notebooks/`.
- Los archivos han sido codificados para preservar confidencialidad.

## Reproducibilidad en Jupyter/Colab

Para reproducir el análisis en un Jupyter Notebook local o en Google Colab:

1. Asegúrate de que los archivos `.SAV` estén en `data/raw/`
2. Instala las dependencias: `pip install -r requirements.txt`
3. Abre el notebook: `notebooks/Fase1_Herencia_Informalidad.ipynb`
4. Ejecuta las celdas en orden (la configuración del entorno está en la primera celda)
5. Los gráficos y resultados se guardarán en `output/`

**Nota para Colab:** El notebook buscará automáticamente una carpeta compartida en Google Drive. Si no la encuentra, usará el almacenamiento local de la sesión.