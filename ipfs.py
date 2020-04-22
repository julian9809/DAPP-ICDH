import ipfsapi
import io
import shutil

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

def cargar_archivos(arreglo):
	print("CARGAR ARCHIVOS")
	tam = arreglo.__len__()
	for i in range(0,tam):
		print("hash" + repr(i))
		api.get(arreglo[i]['hash'] + "/imagen")
		api.get(arreglo[i]['hash'] + "/data.json")
		print("cargado")
		shutil.move("imagen","static/images/clasificar/imagen"+repr(i))
		shutil.move("data.json","data/datos"+repr(i)+".json")
		print("movido")
	print("salio del for")
	return "terminado"
