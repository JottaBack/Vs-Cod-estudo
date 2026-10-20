alunos = ['Alice', 'Bob', 'Charlie']
numeros = [1, 2, 3]
mistura = ['Alice', 25, True]

#lista de analise de dados

lista_de_dados = [9, 5, 3, 8,]
media = sum(lista_de_dados) / len(lista_de_dados)
print(f"A média dos dados é: {media}")

#automação mensagens 
nomes = ['anderson', 'maria', 'joão']

for nome in nomes:
    print(f"Olá, {nome}! Bem-vindo ao nosso programa de treinamento.")

#filtrar infors
clientes = ['anderson', 'maria', 'joão', 'pedro', 'lucas']
clientes_com_j =  []

for cliente in clientes:
    if cliente.startswith('j'):
        clientes_com_j.append(cliente)


print(f"Clientes com a letra 'j': {clientes_com_j}")

#