import json
from web3 import Web3
from solc import compile_standard

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
infura_url = "https://mainnet.infura.io/v3/e78980b5c49e414b8acb07a9d14b4be4"
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
print("ESTA ES LA CONEXION ETHEREUM")
print(w3.isConnected())
w3.eth.defaultAccount = w3.eth.accounts[0]
print(w3.eth.defaultAccount)

#Intancia del contrato
UsersContract = w3.eth.contract(abi=abi, bytecode=bytecode)

#Despliegue del contrato
tx_hash = UsersContract.constructor().transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Contract Address: ", tx_receipt.contractAddress)
