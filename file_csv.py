import csv
import pandas as pd
import os

def insertar_datos(archivo,columnas,dato):
    cont = 0
    id = 0
    with open(archivo) as File:
        reader = csv.DictReader(File)
        for row in reader:
            id = id+1
            if row[columnas[1]] == dato:
                cont = cont+1
    print("EL RESULTADO DEL CONTADOR ES "+repr(cont))
    id = id+1
    if cont == 0:
        fieldnames = columnas
        datos = [[id,dato]]
        data = pd.DataFrame(datos, columns=fieldnames)
        data.to_csv(archivo, index=None, mode="a", header=not os.path.isfile(archivo))
    return "Datos agregados"

def insertar_eleccion(eleccion,columnas,cuenta,hash):
    idUser = ""
    idImage = ""
    election = 0
    with open("users.csv") as File:
        reader = csv.DictReader(File)
        for row in reader:
            if row['user'] == cuenta:
                idUser = row['idUser']
    with open("images.csv") as File:
        reader = csv.DictReader(File)
        for row in reader:
            if row['image'] == hash:
                idImage = row['idImage']
    archivo = "election.csv"
    if eleccion == "violenta":
        election = 1
    fieldnames = columnas
    datos = [[idUser,idImage,election]]
    data = pd.DataFrame(datos, columns=fieldnames)
    data.to_csv(archivo, index=None, mode="a", header=not os.path.isfile(archivo))
    return "Elección guardada"

def obtener_imagen(id_image):
    imagen = ""
    with open("images.csv") as File:
        reader = csv.DictReader(File)
        for row in reader:
            if row['idImage'] == id_image:
                imagen = row['image']
    return imagen
