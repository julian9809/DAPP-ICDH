from web3 import Web3
import encriptamiento as ec
import generador_frase as gf

infura_url = "https://mainnet.infura.io/v3/e78980b5c49e414b8acb07a9d14b4be4"

global web3

web3 = Web3(Web3.HTTPProvider(infura_url))

print(web3.isConnected())

def crear_cuenta(password):
    try:
        account = web3.eth.account.create()
        address = account.address
        keystore = account.encrypt(password)
        encrypted_password = ec.hash_password(password)
        frase = gf.generar_frase()
        encrypted_phrase = ec.hash_phrase(frase)
        print(account)
        print(keystore)
        print(encrypted_password)
        datos = {'address': address,'password':encrypted_password, 'phrase': encrypted_phrase,"keystore" :keystore, "violence_images" :[], "no_violence_images" : []}
        resultado = [True, datos, frase]
    except Exception as e:
        resultado = [False, None]
    return resultado
