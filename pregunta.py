"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------

Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.


"""
import pandas as pd
import re

def formato(header):
    """Formatea los títulos a minúsculas y reemplaza espacios por guiones bajos."""
    return header.lower().replace(" ", "_")

def ingest_data():

    #
    # Inserte su código aquí
    #

    with open("clusters_report.txt", "r") as file:
        lineas = file.readlines()

    title1 = re.sub(r"\s{2,}", "-", lineas[0]).strip().split("-")
    title2 = re.sub(r"\s{2,}", "-", lineas[1]).strip().split("-")
    title1.pop()  
    title2.pop(0)
        
    encabezados = [
            title1[0],  # cluster
            title1[1] + " " + title2[0],  # cantidad_de_palabras_clave
            title1[2] + " " + title2[1],  # porcentaje_de_palabras_clave
            title1[3]  # principales_palabras_clave
        ]
    
    # Aplicar el formato a los encabezados
    encabezados = [formato(h) for h in encabezados]

    # Lectura del archivo usando pandas con las columnas y anchos establecidos
    df = pd.read_fwf(
        "clusters_report.txt",
        widths=[9, 16, 16, 80],  # Ancho de las columnas
        header=None,
        names=encabezados,  # Encabezados formateados
        skip_blank_lines=False,
        converters={
            encabezados[2]: lambda x: x.rstrip(" %").replace(",", ".")  # Para formato de porcentaje
        },
    ).drop([0, 1, 2, 3], axis=0)  # Eliminamos las filas no útiles

    # Procesamos la columna de palabras clave
    col4 = df[encabezados[3]]
    df = df[df[encabezados[0]].notna()].drop(encabezados[3], axis=1)
    df = df.astype(
        {
            encabezados[0]: int,
            encabezados[1]: int,
            encabezados[2]: float,
        }
    )

    # Concatenación de las palabras clave
    column4 = []
    text = ""
    for lin in col4:
        if isinstance(lin, str):
            text += lin + " "
        else:
            text = ", ".join([" ".join(x.split()) for x in text.split(",")])
            column4.append(text.rstrip("."))
            text = ""
            continue

    df[encabezados[3]] = column4
    return df

print(ingest_data())

