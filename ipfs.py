import ipfsapi
import io
import shutil
import json

try:
	api = ipfsapi.connect('127.0.0.1', 5001)
	print("Funciona IPFS")
	print(api)
except ipfsapi.exceptions.ConnectionError as ce:
	print("No Funciona IPFS")
	print(str(ce))

def subir_archivo(archivo):
	new_file = api.add(archivo)
	print(new_file[2]["Hash"])
	return new_file[2]["Hash"]

def cargar_archivos(arreglo,imagenes):
	print("CARGAR ARCHIVOS")
	tam = arreglo.__len__()
	for i in range(0,tam):
		print("hash" + repr(i))
		api.get(arreglo[i]['hash'] + "/imagen")
		api.get(arreglo[i]['hash'] + "/data.json")
		print("cargado")
		direccion_imagen = "static/images/clasificar/imagen"+repr(i)
		direccion_datos = "data/datos"+repr(i)+".json"
		shutil.move("imagen",direccion_imagen)
		shutil.move("data.json",direccion_datos)
		print("movido")
		imagenes['images'].append({
            arreglo[i]['hash'] : repr(i)
        })
		with open('images.json','w')as file:
			json.dump(imagenes,file,indent=4)
	print("salio del for")
	return "terminado"

def cargar_elecciones(arreglo,imagenes):
	print("CARGAR ARCHIVOS")
	tam = arreglo.__len__()
	for i in range(0,tam):
		print("hash" + repr(i))
		api.get(arreglo[i] + "/imagen")
		api.get(arreglo[i] + "/data.json")
		print("cargado")
		direccion_imagen = "static/images/elecciones/imagen"+repr(i)
		direccion_datos = "data/elecciones/datos"+repr(i)+".json"
		shutil.move("imagen",direccion_imagen)
		shutil.move("data.json",direccion_datos)
		print("movido")
		imagenes['images'].append({
            arreglo[i] : repr(i)
        })
		with open('images_eleccion.json','w')as file:
			json.dump(imagenes,file,indent=4)
	print("salio del for")
	return "terminado"