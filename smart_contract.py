import json
from web3 import Web3
from solc import compile_standard
import os
from os import remove

def transaction(usuario,hash):  
    contrato = {}
    contrato['contract'] = []   

    #Lectura del contrato inteligente escrito en Solidity

    f = open ('UsersContract.sol','r')
    contractFile = f.read()
    f.close()

    #Compilación del contrato

    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources":{
            "UsersContract.sol":{
                "content": contractFile
            }
        },
        "settings":{
            "outputSelection":{
                "*": {
                    "*": ["metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        }
    })

    #Obtención del bytecode del contrato
    bytecode = compiled_sol['contracts']['UsersContract.sol']['UsersContract']['evm']['bytecode']['object']
    f = open ('UsersContract.bytecode','w')
    f.write(bytecode)
    f.close()

    #Obtención del abi del contrato
    abi = json.loads(compiled_sol['contracts']['UsersContract.sol']['UsersContract']['metadata'])['output']['abi']
    textAbi = json.dumps(abi)
    f = open ('UsersContract.abi','w')
    f.write(textAbi)
    f.close()

    #Conexión a la red
    url = "HTTP://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(url))
    print("ESTA ES LA CONEXION ETHEREUM")
    print(web3.isConnected())
    web3.eth.defaultAccount = web3.eth.accounts[0]
    print('CUENTA = ' + web3.eth.defaultAccount)
    bloque = web3.eth.blockNumber
    print('BLOQUE = ' + repr(bloque))
    balance = web3.eth.getBalance(web3.eth.defaultAccount)
    print("BALANCE = "  + repr(web3.fromWei(balance, "ether")))
    print(web3.eth.accounts)

    #Intancia del contrato
    UsersContract = web3.eth.contract(abi=abi, bytecode=bytecode)
    print("SE CREA EL CONTRATO")

    #Despliegue del contrato
    tx_hash = UsersContract.constructor().transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print("Contract Address: ", tx_receipt.contractAddress)

    contract = tx_receipt.contractAddress    

    if os.path.isfile('contract.json'):
        remove("contract.json")
        contrato['contract'] = []
    else:
        contrato['contract'].append({
            'contract':contract
        })
        with open('contract.json','w')as file:
            json.dump(contrato,file,indent=4)

    user = web3.eth.contract(
        address=contract,
        abi=abi
    )
    tx_hash = user.functions.setUser(usuario).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(user.functions.getUser().call())
    return "exito"

    
