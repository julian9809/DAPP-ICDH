import uuid
import hashlib

def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()



def check_all_passwords(user_password, all_passwords):
    correct_password = []
    estado = False
    for i in range(len(all_passwords)):
        if check_password(all_passwords[i], user_password):
            print('You entered the right password')
            estado = True
            correct_password.append(all_passwords[i])
    return [estado, correct_password]

def hash_phrase(frase):
    print(frase)
    return hashlib.sha256(frase.encode()).hexdigest()

def check_phrase(frase_password, frase_hashed):
    resultado_frase = False
    print('check')
    print(frase_password)
    print(frase_hashed)
    if(frase_password == frase_hashed):
        resultado_frase = True
    return resultado_frase

def check_all_frases(frases, frase_user):
    frase_usuario = hash_phrase(frase_user)
    for i in range(len(frases)):
        resultado = check_phrase(frases[i],frase_usuario)
        if(resultado):
            return [True, frase_usuario]
    return [False]
