from flask import Flask, flash, request, redirect, render_template, jsonify, url_for, send_from_directory, json
from os import remove
import registro as rg
import crud
import login as lg
import os
from werkzeug.utils import secure_filename
import ipfs
import metadata as mt
import shutil
import csv
from random import randint, uniform,random
import pandas as pd
import file_csv
import recommendation as rec
#import smart_contract


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./imagenes"
ALLOWED_EXTENSIONS = set(["jpg","jpeg","png"])
global data_hash
data_hash = {}
data_hash['hash'] = []

if os.path.isfile('ipfs_hash.json'):
    print("archivo existe")
    with open('ipfs_hash.json') as file:
        data_hash = json.load(file)
else:
    if os.path.isfile('users.json'):
        remove('users.json')
    print("archivo no existe")
    with open('ipfs_hash.json','w')as file:
        json.dump(data_hash,file,indent=4)

def allowed_file(filename):
	return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS

global imagenes
imagenes = {}
imagenes['images'] = []

global imagenes_eleccion
imagenes_eleccion = {}
imagenes_eleccion['images'] = []

if os.path.isfile('users.csv'):
    print("archivo existe")
else:
    print("archivo no existe")
    with open('users.csv', 'w') as csvfile:
        fieldnames = ['idUser', 'user']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

if os.path.isfile('images.csv'):
    print("archivo existe")
else:
    print("archivo no existe")
    with open('images.csv', 'w') as csvfile:
        fieldnames = ['idImage', 'image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

if os.path.isfile('election.csv'):
    print("archivo existe")
else:
    print("archivo no existe")
    with open('election.csv', 'w') as csvfile:
        fieldnames = ['idUser', 'IdImage','election']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

if os.path.isfile('images.json'):
    print("archivo existe")
    with open('images.json') as file:
        imagenes = json.load(file)
else:
    print("archivo no existe")
    with open('images.json','w')as file:
        json.dump(imagenes,file,indent=4)

if os.path.isfile('images_eleccion.json'):
    print("archivo existe")
    with open('images_eleccion.json') as file:
        imagenes_eleccion = json.load(file)
else:
    print("archivo no existe")
    with open('images_eleccion.json','w')as file:
        json.dump(imagenes_eleccion,file,indent=4)

global elecciones
elecciones = {}
elecciones['election'] = []

global elections
elections = {}
elections['election'] = []

if os.path.isfile('election.json'):
    print("archivo existe")
    remove("election.json")
else:
    print("archivo no existe")
    with open('election.json','w')as file:
        json.dump(elecciones,file,indent=4)

visu_cont = 0
cont_ima = 0
cont_ima_elec = 0
control = ""

conexion = None
conexion, database ,raiz = crud.establecer_conexion(conexion)

account_user = ""

print("MongoDB")
print(database.name)
print(raiz.name)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/user', methods=['POST'])
def user():
    data = request.form
    data_dictionary = data.copy()
    print(data_dictionary)
    global account_user
    account_user = data_dictionary["account"]
    fieldnames = ['idUser','user']
    print(file_csv.insertar_datos("users.csv",fieldnames,account_user))
    return render_template('inicio.html', account=account_user, verificacion="si")

@app.route('/inicio', methods=['POST'])
def begin():
    return render_template('inicio.html')

@app.route('/formulario', methods=['POST'])
def metadata():
	return render_template('formulario.html')

@app.route('/carga', methods=['POST'])
def carga_imagen():
    return render_template('carga.html')

@app.route('/clasificar', methods=['POST'])
def clasificar():
    return render_template('cargar_imagenes.html')

@app.route('/cargar_imagenes', methods=['POST'])
def cargar_imagenes():
    folder = ['static/images/clasificar','data']
    for i in range(0,2):
        print("PRUEBA BORRADO")
        print(folder[i])
        for the_file in os.listdir(folder[i]):
            file_path = os.path.join(folder[i], the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
    arreglo = data_hash['hash']
    print(ipfs.cargar_archivos(arreglo,imagenes))
    print("iniciar clasificacion")
    return render_template('carga_exitosa.html')

@app.route('/clasificacion', methods=['POST'])
def clasificacion():
    global cont_ima
    print("CONTADOR"+repr(cont_ima))
    data = request.form
    data_dictionary = data.copy()
    clas = data_dictionary["clasificacion"]
    print("CLASIFICACION = "+clas)
    hash = data_hash['hash'][cont_ima-1]['hash']
    print("ESTE ES EL HASH"+hash)
    verificacion = crud.verificar_existencia(raiz, account_user, hash)
    print(verificacion)
    if verificacion == "no existe" and clas != "no_clasificado":
        print("insertando...")
        print(crud.insertar_seleccion(raiz, account_user, hash, clas))
    print(crud.mostrar_informacion(raiz, account_user))
    fieldnames = ['idUser', 'IdImage','election']
    print(file_csv.insertar_eleccion(clas,fieldnames,account_user,hash))
    tam = data_hash['hash'].__len__()
    if cont_ima < tam:
        imagen = "../static/images/clasificar/imagen"+repr(cont_ima)
        archivo = 'data/datos'+repr(cont_ima)+'.json'
        with open(archivo) as file:
            datos = json.load(file)
        titulo = datos['name']
        fecha = datos['date']
        descripcion = datos['description']
        cont_ima = cont_ima + 1
        return render_template('clasificacion.html', imagen=imagen, titulo=titulo, fecha=fecha, descripcion=descripcion)
    else:
        cont_ima = 0
        return render_template('clas_fin.html')

@app.route('/carga_ipfs', methods=['POST'])
def carga_ipfs():
    hash = ipfs.subir_archivo('./imagenes')
    data_hash['hash'].append({
        'hash':hash
    })
    with open('ipfs_hash.json','w')as file:
        json.dump(data_hash,file,indent=4)
    fieldnames = ['idImage','image']
    print(file_csv.insertar_datos("images.csv",fieldnames,hash))
    return render_template('carga.html')

@app.route('/inicio_ipfs', methods=['POST'])
def inicio_ipfs():
    hash = ipfs.subir_archivo('./imagenes')
    data_hash['hash'].append({
        'hash':hash
    })
    with open('ipfs_hash.json','w')as file:
        json.dump(data_hash,file,indent=4)
    fieldnames = ['idImage','image']
    print(file_csv.insertar_datos("images.csv",fieldnames,hash))
    return render_template('inicio.html')

@app.route('/exito', methods=['POST'])
def exito_carga():
	with open('imagenes/data.json','w')as file:
		json.dump(mt.llenado_auto(),file,indent=4)
	return render_template('exito.html')

@app.route('/uploader', methods=['POST'])
def uploader():
	data = request.form
	data_dictionary = data.copy()
	print(data_dictionary)
	eleccion = data_dictionary["eleccion"]
	print(eleccion)
	if request.method == "POST":
		if "imagenes" not in request.files:
			return render_template('carga.html', error="Error al subir la imagen, intentelo de nuevo")
		f = request.files["imagenes"]
		if f.filename == "":
			return render_template('carga.html', error="Por favor suba una imagen")
		if f and allowed_file(f.filename):
			filename = secure_filename(f.filename)
			f.save(os.path.join(app.config['UPLOAD_FOLDER'],"imagen"))
			if(eleccion == "no"):
				return render_template('advertencia_metadata.html')
			else:
				return render_template('formulario.html')
		return render_template('carga.html', error="Formato no permitido")

@app.route('/formulario_carga', methods=['POST'])
def form():
	data = request.form
	data_dictionary = data.copy()
	nombre = data_dictionary["name"]
	descripcion = data_dictionary["description"]
	if nombre != "" or descripcion != "":
		with open('imagenes/data.json','w')as file:
			json.dump(data,file,indent=4)
		return render_template('exito.html')

@app.route('/visualizacion', methods=['POST'])
def visualizacion():
    folder = ['static/images/elecciones','data/elecciones']
    for i in range(0,2):
        print("PRUEBA BORRADO")
        print(folder[i])
        for the_file in os.listdir(folder[i]):
            file_path = os.path.join(folder[i], the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
    global control
    if control == "":
        if os.path.isfile('election.json'):
            elecciones['election'] = []
            remove("election.json")
        else:
            print("archivo no existe")
            with open('election.json','w')as file:
                json.dump(elecciones,file,indent=4)    
    return render_template('visualizar.html')

@app.route('/visualizar', methods=['POST'])
def visualizar():
    global visu_cont
    global control
    print("CONTROL " + control)
    if control == "":
        if os.path.isfile('election.json'):
            elecciones['election'] = []
            remove("election.json")
        else:
            print("archivo no existe")
            with open('election.json','w')as file:
                json.dump(elecciones,file,indent=4) 
        control = rec.recomendaciones(account_user,elecciones)
    print("VISUALIZAR "+repr(visu_cont))
    imagen = ""
    pos = 0
    print("visualizar")
    with open('election.json')as file:
        elections = json.load(file)
    print("VERIFICACION")
    tam = elections['election'].__len__()
    print("TAMAÑO "+repr(tam))
    if visu_cont < tam:
        print("VISU_CONT "+repr(visu_cont))
        imagen = file_csv.obtener_imagen(elections['election'][visu_cont]['imagen'])
        puntaje = float(elections['election'][visu_cont]['puntaje'])
        puntaje = "{:.1f}".format(puntaje*100)
        visu_cont = visu_cont+1
        with open('ipfs_hash.json')as file:
            data_hash = json.load(file)
            tam = data_hash['hash'].__len__()
            for i in range(tam):
                if data_hash['hash'][i]['hash'] == imagen:
                    pos = i
        imagen = "../static/images/clasificar/imagen"+repr(pos)
        print(imagen)
        archivo = 'data/datos'+repr(pos)+'.json'
        with open(archivo) as file:
            datos = json.load(file)
        titulo = datos['name']
        fecha = datos['date']
        descripcion = datos['description']
        return render_template('visualizacion.html', imagen=imagen, titulo=titulo,
        fecha=fecha, descripcion=descripcion, puntaje = puntaje)
    else:
        print("REINICIAR CONTADOR")
        visu_cont = 0
        return render_template('inicio.html')

@app.route('/visualizar_eleccion', methods=['POST'])
def election():
    listaElecciones = []
    listaElecciones = crud.elecciones(raiz,account_user)
    global cont_ima_elec
    if cont_ima_elec == 0:
        print(ipfs.cargar_elecciones(listaElecciones,imagenes_eleccion))    
    tam = listaElecciones.__len__()
    print(cont_ima_elec)
    if cont_ima_elec < tam:
        imagen = "../static/images/elecciones/imagen"+repr(cont_ima_elec)
        archivo = 'data/elecciones/datos'+repr(cont_ima_elec)+'.json'
        with open(archivo) as file:
            datos = json.load(file)
        titulo = datos['name']
        fecha = datos['date']
        descripcion = datos['description']
        cont_ima_elec = cont_ima_elec + 1
        print(cont_ima_elec)
        return render_template('elecciones.html', imagen=imagen, titulo=titulo, fecha=fecha, descripcion=descripcion)
    else:
        cont_ima_elec = 0
        return render_template('visualizar.html')

@app.route('/login', methods=['POST'])
def login_process():
    global control
    global visu_cont
    visu_cont = 0
    data = request.form

    data_dictionary = data.copy()
    print(data_dictionary)

    password_user = data_dictionary["password"]
    phrase_user = data_dictionary["frase"]
    lista_passwords = crud.obtener_passwords(raiz)

    resultado_password = lg.verificar_password(password_user,lista_passwords)
    print(resultado_password[0])
    if(resultado_password[0]):
        print(resultado_password[1])
        phrase_password = crud.obtener_frases(raiz, resultado_password[1])
        print(phrase_password)
        resultado_frase = lg.verificar_frase(phrase_user, phrase_password)
        print(resultado_frase)
        if(resultado_frase[0]):
            cuenta = crud.obtener_cuenta(raiz, resultado_frase[1])
            print("ESTA ES LA CUENTA:" + cuenta)
            if cuenta != account_user:
                control = ""
            return jsonify({ 'response' :  'Success' , 'address' : cuenta})
        else:
            print('sali en else interno')
            return jsonify({'response' : 'Error'})
    else:
        print('sali else externo')
        return jsonify({'response' : 'Error'})

@app.route('/register', methods=['POST'])
def register_process():
    data = request.form

    data_dictionary = data.copy()
    print(data_dictionary)
    password_user = data_dictionary["password"]
    respuesta_crear = rg.crear_cuenta(password_user)
    if(respuesta_crear[0]):
        estado_registro = crud.insertar_usuario(raiz, respuesta_crear[1])
        if(estado_registro):
            return jsonify({ 'response' :  'Success' , 'phrase' : respuesta_crear[2] ,'address' : respuesta_crear[1]["address"]})
        else:
            return jsonify({'response' : 'Error'})
    else:
        return jsonify({'response' : 'Error'})


if __name__ == '__main__':
	app.run(debug=True)


"""
conexion = None
conexion, database ,raiz = crud.establecer_conexion(conexion)

print(database.name)
print(raiz.name)

password = "universidady"


usuario_creado = rg.crear_cuenta(password)

print(usuario_creado)

if(usuario_creado[0] == True):
    estado_insercion = crud.insertar_usuario(raiz,usuario_creado[1])
    print(estado_insercion)
else:
    print("No se pudo insertar usuario")

lista_passwords = crud.obtener_passwords(raiz)
resultado_verificacion = lg.verificar_usuario(password,lista_passwords)
print(resultado_verificacion)
"""
