import pymongo


def crear_conexion(conexion):
    if(conexion == None):
        try:
            conexion = pymongo.MongoClient('localhost',27017)
        except:
            conexion = None
    else:
        conexion = conexion
    return conexion

def definir_raiz(conexion):
    database = conexion.blockchain_database
    collection = database.users
    return database,collection
