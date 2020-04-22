import pymongo
import conexion as cn


def establecer_conexion(conexion):
    conexion = cn.crear_conexion(conexion)
    database, raiz = cn.definir_raiz(conexion)
    return conexion, database, raiz

def insertar_usuario(raiz, datos):
    try:
        raiz.insert_one(datos)
        estado = True
    except:
        estado = False
    return estado

def obtener_passwords(raiz):
    lista_passwords = []
    for document in raiz.find():
        lista_passwords.append(document["password"])
    return lista_passwords

def obtener_frases(raiz, password):
    frases_resultado = []
    for i in range(len(password)):
        resultado = raiz.find({'password':password[i]})
        for x in resultado:
            resultado_frase = x["phrase"]
            frases_resultado.append(resultado_frase)
    return frases_resultado

def obtener_cuenta(raiz, frase):
    resultado = raiz.find({'phrase':frase})
    for i in resultado:
        resultado_cuenta =  i["address"]
    return resultado_cuenta
