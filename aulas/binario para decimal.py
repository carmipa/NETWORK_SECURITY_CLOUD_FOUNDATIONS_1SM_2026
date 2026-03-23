binario = input("Digite um número binário: ")

tamanho = len(binario)
decimal = 0
posicao = tamanho - 1
soma_texto = ""

print("\nTABELA DE CONVERSÃO DO BINÁRIO PARA DECIMAL")
print("-" * 50)
print("BINÁRIO | PESO (2^n) | RESULTADO")
print("-" * 50)

for digito in binario:
    potencia = 2 ** posicao
    valor = int(digito) * potencia

    print(f"{digito:^7} | {('2^' + str(posicao)):^11} | {valor:^9}")

    decimal = decimal + valor

    if soma_texto == "":
        soma_texto = str(valor)
    else:
        soma_texto = soma_texto + " + " + str(valor)

    posicao = posicao - 1

print("-" * 50)
print("Soma:", soma_texto)
print("Decimal:", decimal)