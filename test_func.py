lista =[ 1,2,3353,4,5]
print(lista[4])
print(len(lista))
print(lista[len(lista)-1])
print("novo negocio q eu to procurando",lista.index(3353))


class Academico:
    def __init__(self) -> None:
        self.nome = 'Rhian'


teste = Academico()
print(teste)
print(teste.nome)

dicionario = {
    'valor': 'key',
    'cla': 45,
    'porsche': 'panamera'
}

for chave in dicionario:
    print("chave do for", chave)


print(dicionario)
print(dicionario['valor'])
print(len(dicionario))
chave = next(iter(dicionario))
print(chave)
dicionario = {
    'cla': 45,
    'valor': 'key',
    'porsche': 'panamera'
}

chave = next(iter(dicionario))
print(chave)

dicionario = {
    'valor': 'key',
    'porsche': 'panamera'
}

chave = next(iter(dicionario))
print(chave)


# Exemplo de dicionário
meu_dicionario = {'a': 1, 'b': 2, 'c': 3}

# Removendo o item com a chave 'b'
del meu_dicionario['b']

print(f"Dicionário após a remoção: {meu_dicionario}")
print(type(meu_dicionario)== dict)


