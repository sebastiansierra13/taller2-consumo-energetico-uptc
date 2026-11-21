"""
Módulo de Preparación de Datos - Taller II
Especialización en Inteligencia Artificial - UPTC

Proceso integral de preparación de datos para la implementación
de modelos de predicción y optimización del consumo energético.
"""

import os
import sys
import csv
import math
from collections import Counter
from datetime import datetime


def cargar_datos(ruta_csv):
    """Fase I.1 y I.2: Carga de datos y dimensiones iniciales."""
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_csv}")
    
    print(f"Cargando dataset desde: {ruta_csv}...")
    with open(ruta_csv, mode="r", encoding="utf-8", errors="replace") as f:
        lector = csv.reader(f)
        encabezado = next(lector)
        filas = [row for row in lector]
        
    print(f"-> Total de filas: {len(filas):,}")
    print(f"-> Total de columnas: {len(encabezado)}")
    return encabezado, filas


def exploracion_inicial(encabezado, filas):
    """Fase I.3, I.4, I.5, I.6: Exploración inicial y detección de inconsistencias."""
    idx_sede = encabezado.index("sede")
    idx_periodo = encabezado.index("periodo_academico")
    
    # Conteo por sedes
    sedes = Counter([row[idx_sede] for row in filas])
    print("\n--- Distribución por Sede ---")
    for sede, cant in sedes.items():
        print(f"  * {sede}: {cant:,} registros")
        
    # Inconsistencias en periodo_academico
    periodos = Counter([row[idx_periodo] for row in filas])
    print("\n--- Inconsistencias detectadas en periodo_academico ---")
    for per, cant in periodos.items():
        print(f"  * '{per}': {cant:,}")


def limpieza_duitama(encabezado, filas):
    """
    Fase II: Limpieza y preparación inicial para la sede DUITAMA.
    - Filtrar sede DUITAMA
    - Comparar cantidad de registros
    - Detectar y remover valores negativos en variables físicas/emisiones
    - Verificar y remover duplicados
    """
    idx_id = encabezado.index("reading_id")
    idx_sede = encabezado.index("sede")
    
    # 8. Filtrar DUITAMA
    filas_duitama = [r for r in filas if r[idx_sede].strip().upper() == "DUITAMA"]
    print(f"\n--- Fase II: Filtrado Sede DUITAMA ---")
    print(f"  * Registros totales: {len(filas):,}")
    print(f"  * Registros Duitama: {len(filas_duitama):,} ({(len(filas_duitama)/len(filas))*100:.2f}%)")
    
    # 10. Detectar negativos
    vars_fisicas = [
        "energia_comedor_kwh",
        "energia_salones_kwh",
        "energia_laboratorios_kwh",
        "energia_auditorios_kwh",
        "energia_oficinas_kwh",
        "agua_litros",
        "co2_kg",
        "energia_total_kwh"
    ]
    indices_fisicas = {v: encabezado.index(v) for v in vars_fisicas}
    
    conteo_negativos = {v: 0 for v in vars_fisicas}
    filas_validas = []
    
    for row in filas_duitama:
        es_invalido = False
        for v, idx in indices_fisicas.items():
            val = row[idx]
            if val != "" and val is not None:
                try:
                    num = float(val)
                    if num < 0:
                        conteo_negativos[v] += 1
                        es_invalido = True
                except ValueError:
                    pass
        if not es_invalido:
            filas_validas.append(row)
            
    print("\n--- Valores negativos detectados en Duitama ---")
    for v, cant in conteo_negativos.items():
        print(f"  * {v}: {cant} negativos")
        
    # 11. Eliminar inválidos
    removidos = len(filas_duitama) - len(filas_validas)
    print(f"\n-> Registros inválidos eliminados: {removidos}")
    print(f"-> Registros restantes válidos: {len(filas_validas):,}")
    
    # 12 & 13. Duplicados (excluyendo reading_id)
    vistos = set()
    filas_sin_duplicados = []
    duplicados = 0
    for row in filas_validas:
        clave = tuple(row[i] for i in range(len(row)) if i != idx_id)
        if clave in vistos:
            duplicados += 1
        else:
            vistos.add(clave)
            filas_sin_duplicados.append(row)
            
    print(f"-> Registros duplicados detectados y eliminados: {duplicados}")
    print(f"-> Total limpio Duitama: {len(filas_sin_duplicados):,}")
    return filas_sin_duplicados


def imputar_y_analizar(encabezado, filas_duitama):
    """
    Fase III: Análisis descriptivo e imputación con mediana / moda.
    """
    vars_energeticas = [
        "energia_comedor_kwh",
        "energia_salones_kwh",
        "energia_laboratorios_kwh",
        "energia_auditorios_kwh",
        "energia_oficinas_kwh",
        "energia_total_kwh",
        "potencia_total_kw",
        "agua_litros",
        "temperatura_exterior_c",
        "ocupacion_pct",
        "co2_kg",
    ]
    indices_ener = {v: encabezado.index(v) for v in vars_energeticas if v in encabezado}
    
    # Calcular estadísticas y medianas para numéricas
    print("\n--- Estadísticas Descriptivas (Duitama antes de imputar) ---")
    medianas = {}
    for var, idx in indices_ener.items():
        valores = []
        nulos = 0
        for r in filas_duitama:
            val = r[idx]
            if val == "" or val is None:
                nulos += 1
            else:
                try:
                    valores.append(float(val))
                except ValueError:
                    nulos += 1
        valores.sort()
        n = len(valores)
        mediana = valores[n // 2] if n % 2 != 0 else (valores[n // 2 - 1] + valores[n // 2]) / 2.0
        media = sum(valores) / n if n > 0 else 0
        min_v = valores[0] if n > 0 else 0
        max_v = valores[-1] if n > 0 else 0
        medianas[var] = mediana
        print(f"  * {var:25} | Nulos: {nulos:5} | Min: {min_v:8.3f} | Mediana: {mediana:8.3f} | Media: {media:8.3f} | Max: {max_v:8.3f}")

    # Imputar en filas
    for r in filas_duitama:
        for var, idx in indices_ener.items():
            if r[idx] == "" or r[idx] is None:
                r[idx] = str(medianas[var])
                
    print("\n-> Imputación numérica completada con éxito utilizando la mediana.")
    return filas_duitama


def preparar_conjunto_final(encabezado, filas_duitama, ruta_salida="data/consumos_duitama_preparado.csv"):
    """
    Fase IV: Selección de variables objetivo, features, exclusión y guardado del dataset final.
    """
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    
    target = "energia_total_kwh"
    features = [
        "energia_comedor_kwh",
        "energia_salones_kwh",
        "energia_laboratorios_kwh",
        "energia_auditorios_kwh",
        "energia_oficinas_kwh",
        "potencia_total_kw",
        "agua_litros",
        "temperatura_exterior_c",
        "ocupacion_pct",
        "hora",
        "dia_semana",
        "mes",
        "trimestre",
        "es_fin_semana",
        "es_festivo",
        "es_semana_parciales",
        "es_semana_finales",
        target
    ]
    
    indices_finales = [encabezado.index(col) for col in features]
    
    with open(ruta_salida, mode="w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(features)
        for row in filas_duitama:
            escritor.writerow([row[i] for i in indices_finales])
            
    print(f"\n=== Fase IV: Conjunto final preparado y guardado ===")
    print(f"-> Ruta de salida: {ruta_salida}")
    print(f"-> Total variables seleccionadas: {len(features)} (Target: {target}, Features: {len(features)-1})")
    print(f"-> Total registros preparados: {len(filas_duitama):,}")


def main():
    ruta_dataset = "consumos_uptc.csv" if os.path.exists("consumos_uptc.csv") else "../consumos_uptc.csv"
    print("=" * 65)
    print("  TALLER II - PREPARACIÓN DE DATOS DE CONSUMO ENERGÉTICO (UPTC)")
    print("=" * 65)
    
    encabezado, filas = cargar_datos(ruta_dataset)
    exploracion_inicial(encabezado, filas)
    filas_limpias = limpieza_duitama(encabezado, filas)
    filas_imputadas = imputar_y_analizar(encabezado, filas_limpias)
    preparar_conjunto_final(encabezado, filas_imputadas)
    
    print("\n[OK] Proceso completado exitosamente.")


if __name__ == "__main__":
    main()
