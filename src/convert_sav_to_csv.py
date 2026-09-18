from __future__ import annotations

import argparse
from pathlib import Path

import pyreadstat


def listar_archivos_sav(directorio: Path):
    """Devuelve los archivos .SAV del directorio, sin cambiar su contenido."""
    if not directorio.exists():
        raise FileNotFoundError(f"No existe la carpeta de entrada: {directorio}")

    archivos = sorted(
        [p for p in directorio.iterdir() if p.is_file() and p.suffix.lower() == ".sav"],
        key=lambda p: p.name.lower(),
    )
    return archivos


def convertir_sav_a_csv(archivo_sav: Path, carpeta_salida: Path) -> Path:
    """Convierte un archivo .SAV a .CSV preservando los datos exactamente."""
    df, _ = pyreadstat.read_sav(str(archivo_sav))

    carpeta_salida.mkdir(parents=True, exist_ok=True)
    salida = carpeta_salida / f"{archivo_sav.stem}.csv"
    df.to_csv(salida, index=False, encoding="utf-8-sig")
    return salida


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convierte archivos .SAV a .CSV sin modificar los datos; solo cambia el formato del archivo."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=Path("datos crudos"),
        help="Carpeta con archivos .SAV de entrada (por defecto: 'datos crudos').",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("datos_crudos_csv"),
        help="Carpeta donde se guardarán los .CSV (por defecto: 'datos_crudos_csv').",
    )
    args = parser.parse_args()

    archivos = listar_archivos_sav(args.input)
    if not archivos:
        raise FileNotFoundError(f"No se encontraron archivos .SAV en: {args.input}")

    print(f"Se encontraron {len(archivos)} archivos .SAV en {args.input}")
    print(f"Se guardarán en: {args.output}")

    for archivo in archivos:
        salida = convertir_sav_a_csv(archivo, args.output)
        print(f"- {archivo.name} -> {salida.name}")

    print(f"Conversión finalizada: {len(archivos)} archivos CSV creados en {args.output}")


if __name__ == "__main__":
    main()
