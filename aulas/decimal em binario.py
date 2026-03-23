numero = int(input("Digite um número decimal: "))

original = numero
binario = ""
soma = ""

print("\nTABELA DE CONVERSÃO DO DECIMAL PARA BINÁRIO")
print("--------------------------------------------------")
print(f"{'DECIMAL':^10}|{'DIVIDE POR 2':^14}|{'RESTO':^10}")
print("--------------------------------------------------")

while numero > 0:
    quociente = numero // 2
    resto = numero % 2

    print(f"{numero:^10}|{quociente:^14}|{resto:^10}")

    binario = str(resto) + binario
    numero = quociente

print("--------------------------------------------------")
print(f"\nBinário: {binario}")