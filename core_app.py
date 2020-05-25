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
from random import randint, uniform,random


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

global usuarios
usuarios = {}
usuarios['users'] = []

if os.path.isfile('users.json'):
    print("archivo existe")
    with open('users.json') as file:
        usuarios = json.load(file)
else:
    print("archivo no existe")
    with open('users.json','w')as file:
        json.dump(usuarios,file,indent=4)

cont = 0
pos = 0

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
    return render_template('inicio.html', account=account_user, verificacion="si")

@app.route('/inicio', methods=['POST'])
def begin():
    global cont
    cont  = 0
    print("reiniciar contador")
    return render_template('inicio.html')

@app.route('/formulario', methods=['POST'])
def metadata():
	return render_template('formulario.html')

@app.route('/carga', methods=['POST'])
def carga_imagen():
    global cont
    cont = 0
    print("reiniciar contador")
    return render_template('carga.html')

@app.route('/clasificar', methods=['POST'])
def clasificar():
    global cont
    cont2 = 0
    global pos
    tam_Usu = usuarios['users'].__len__()
    for i in range(0,tam_Usu):
        if usuarios['users'][i]['usuario'] == account_user:
            cont2 = cont2 + 1
            pos = i
        else:
            cont2  = cont2
    if cont2 != 0:
        cont = usuarios['users'][pos]['verificacion']
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
    print(ipfs.cargar_archivos(arreglo))
    print("iniciar clasificacion")
    return render_template('carga_exitosa.html')

@app.route('/clasificacion', methods=['POST'])
def clasificacion():
    data = request.form
    data_dictionary = data.copy()
    clas = data_dictionary["clasificacion"]
    print("CLASIFICACION = "+clas)
    global cont
    global pos
    hash = data_hash['hash'][cont-1]['hash']
    verificacion = crud.verificar_existencia(raiz, account_user, hash)
    print(verificacion)
    if verificacion == "no existe" and clas != "no_clasificado":
        print("insertando...")
        print(crud.insertar_seleccion(raiz, account_user, hash, clas))
    print(crud.mostrar_informacion(raiz, account_user))
    tam = data_hash['hash'].__len__()
    print("Contador" + repr(cont))
    if cont < tam:
        imagen = "../static/images/clasificar/imagen"+repr(cont)
        archivo = 'data/datos'+repr(cont)+'.json'
        with open(archivo) as file:
            datos = json.load(file)
        titulo = datos['name']
        fecha = datos['date']
        descripcion = datos['description']
        usuarios['users'].append({
            'usuario' : account_user,
            'verificacion' : cont
        })
        with open('users.json','w')as file:
            json.dump(usuarios,file,indent=4)
        cont = cont + 1
        return render_template('clasificacion.html', imagen=imagen, titulo=titulo, fecha=fecha, descripcion=descripcion)
    else:
        usuarios['users'].append({
                'usuario' : account_user,
                'verificacion' : cont
        })
        with open('users.json','w')as file:
            json.dump(usuarios,file,indent=4)
        cont = 0
        return render_template('clas_fin.html')

@app.route('/carga_ipfs', methods=['POST'])
def carga_ipfs():
	data_hash['hash'].append({
		'hash' : ipfs.subir_archivo('./imagenes')
	})
	with open('ipfs_hash.json','w')as file:
		json.dump(data_hash,file,indent=4)
	return render_template('carga.html')

@app.route('/inicio_ipfs', methods=['POST'])
def inicio_ipfs():
	data_hash['hash'].append({
		'hash' : ipfs.subir_archivo('./imagenes')
	})
	with open('ipfs_hash.json','w')as file:
		json.dump(data_hash,file,indent=4)
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

@app.route('/login', methods=['POST'])
def login_process():
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
