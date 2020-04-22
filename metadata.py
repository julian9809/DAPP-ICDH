from datetime import date

def fecha_auto():
    today = date.today()
    mes = int("{}".format(today.month))
    dia = int("{}".format(today.day))
    if mes < 10:
        mes = "0" + "{}".format(today.month)
    else:
        mes = "{}".format(today.month)
    if dia < 10:
        dia = "0" + "{}".format(today.day)
    else:
        dia = "{}".format(today.day)
    año = "{}".format(today.year)
    fecha = año +"-"+ mes +"-"+ dia
    return fecha

def llenado_auto():
    fecha = fecha_auto()
    nombre = "Imagen historica"
    descripcion = "La imagen representa sucesos historicos de Colombia"
    data = {
		'date' : fecha,
		'description' : descripcion,
		'name' : nombre
	}
    return data
