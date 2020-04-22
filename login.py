import encriptamiento as ec

def verificar_password(pasword, lista_passwords):
    resultado_verificacion = ec.check_all_passwords(pasword, lista_passwords)
    return resultado_verificacion

def verificar_frase(frase_usuario, frase_sistema):
    resultado_verificacion = ec.check_all_frases(frase_sistema, frase_usuario)
    return resultado_verificacion
