lista =[ 1,2,3,4,5]
print(lista[4])
print(len(lista))
print(lista[len(lista)-1])

class Academico:
    def __init__(self) -> None:
        self.nome = 'Rhian'


teste = Academico()
print(teste)
print(teste.nome)

dicionario = {
    'valor': 'key',
    'cla': 45
}

print(dicionario)
print(dicionario['valor'])
print(len(dicionario))