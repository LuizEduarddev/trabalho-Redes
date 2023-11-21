dicionario = {
    "cliente1":{"arquivo":"a12835s, planeta dos macacos", "ip":"2183712"},
    "cliente2":{"arquivo":"3412pp, foto do macaco", "ip": "91238"}
    }

string = str()

number = int(0)
temp = len(dicionario)

def verificaTemp(string, number, tamanho):
    temp = number + 1
    if temp >= tamanho:
        return 
    else:
        string = string + ','

for chave, info in dicionario.items():
    number += 1
    string = string + f'{info["arquivo"]},ip{number}:{info["ip"]}'
    verificaTemp(string, number, temp)



print(string)