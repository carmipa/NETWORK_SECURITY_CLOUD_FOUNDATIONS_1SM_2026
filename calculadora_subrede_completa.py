import os
from weasyprint import HTML

# Conteúdo HTML com CSS para estilização técnica e limpa
html_content = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: A4;
            margin: 15mm;
            background-color: #f4f7f6;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #2c3e50;
            line-height: 1.6;
            background-color: #f4f7f6;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 100%;
        }
        .header {
            background-color: #1a2a3a;
            color: #ffffff;
            padding: 20px;
            border-radius: 8px 8px 0 0;
            margin-bottom: 20px;
        }
        h1 { margin: 0; font-size: 18pt; }
        h2 { color: #2980b9; border-left: 5px solid #2980b9; padding-left: 10px; font-size: 15pt; margin-top: 25px; }
        h3 { color: #16a085; font-size: 13pt; }
        code {
            background-color: #e8ecef;
            padding: 2px 4px;
            border-radius: 4px;
            font-family: 'Courier New', Courier, monospace;
        }
        .code-block {
            background-color: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            border-radius: 6px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 9pt;
            white-space: pre-wrap;
            margin: 15px 0;
            border: 1px solid #333;
        }
        .note {
            background-color: #d1ecf1;
            border-left: 5px solid #0c5460;
            color: #0c5460;
            padding: 10px;
            margin: 15px 0;
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        th, td {
            border: 1px solid #bdc3c7;
            padding: 10px;
            text-align: left;
        }
        th { background-color: #ecf0f1; color: #34495e; }
        .footer {
            margin-top: 30px;
            font-size: 8pt;
            color: #7f8c8d;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Framework de Cálculo de Redes IPv4</h1>
            <p>Versão Automatizada em Python para Cyber Defesa</p>
        </div>

        <p>Este documento detalha a implementação de uma calculadora de sub-redes profissional, projetada para converter a lógica de "Arrays de Bits" e potências de 2 em um utilitário robusto para o dia a dia.</p>

        <h2>1. Lógica do Sistema (Backend)</h2>
        <p>Diferente de calculadoras simples, este sistema opera com <strong>Bitwise Operations</strong>. Ele trata o endereço IP como um inteiro de 32 bits, permitindo manipulações precisas de máscaras, broadcasts e identificação de intervalos de rede (o "pulo").</p>
        
        <div class="note">
            <strong>Tratamento de Exceções:</strong> O código inclui blocos <code>try-except</code> para capturar <code>ValueError</code> (IPs malformados ou CIDR fora de 0-32) e lógica condicional para evitar cálculos impossíveis como divisões por zero.
        </div>

        <h2>2. Código-Fonte: subnet_master.py</h2>
        <div class="code-block">
import math

def ip_to_int(ip):
    # Converte String em Array de Octetos e depois em 32 bits
    octetos = [int(o) for o in ip.split('.')]
    return (octetos[0] << 24) + (octetos[1] << 16) + (octetos[2] << 8) + octetos[3]

def int_to_ip(n):
    # Converte os 32 bits de volta para o formato decimal pontuado
    return f"{(n >> 24) & 0xff}.{(n >> 16) & 0xff}.{(n >> 8) & 0xff}.{n & 0xff}"

def exibir_analise(ip_str, cidr):
    try:
        if not (0 <= cidr <= 32):
            raise ValueError("O CIDR deve estar entre 0 e 32.")
        
        # Lógica de Bitmasking (Mascara de Bits)
        ip_int = ip_to_int(ip_str)
        mask_int = (0xffffffff << (32 - cidr)) & 0xffffffff
        rede_int = ip_int & mask_int
        broad_int = rede_int | (0xffffffff ^ mask_int)
        
        # Cálculo de Capacidade baseado nos "Zeros" (Host Bits)
        bits_host = 32 - cidr
        total_ips = 2**bits_host
        
        print("-" * 30)
        print(f"ANÁLISE PARA: {ip_str}/{cidr}")
        print(f"Máscara Decimal: {int_to_ip(mask_int)}")
        print(f"Endereço Rede:   {int_to_ip(rede_int)}")
        print(f"Endereço Broad:  {int_to_ip(broad_int)}")
        print(f"Cálculo Host:    2^{bits_host} = {total_ips} IPs")
        print(f"IPs Úteis:       {total_ips - 2 if total_ips > 2 else 0}")
        print("-" * 30)
        
    except ValueError as ve:
        print(f"[!] Erro de Valor: {ve}")
    except Exception as e:
        print(f"[!] Erro Inesperado: {e}")

def menu():
    while True:
        print("\\n=== MENU CALCULADORA DE REDE ===")
        print("1. Calcular por IP/CIDR (Ex: 172.19.0.0/21)")
        print("2. Descobrir CIDR por número de IPs desejados")
        print("0. Sair")
        
        opcao = input("\\nEscolha uma opção: ")
        
        if opcao == '0': break
        
        try:
            if opcao == '1':
                entrada = input("Digite o IP/CIDR (ex 172.19.0.0/20): ")
                ip, barra = entrada.split('/')
                exibir_analise(ip.strip(), int(barra))
            elif opcao == '2':
                n_hosts = int(input("Quantos hosts você precisa? "))
                # Logaritmo para achar a potência de 2 necessária
                cidr_sugerido = 32 - math.ceil(math.log2(n_hosts + 2))
                print(f"\\n[+] Use a máscara /{cidr_sugerido}")
            else:
                print("[!] Opção inválida.")
        except Exception:
            print("[!] Entrada mal formatada. Tente novamente.")

if __name__ == "__main__":
    menu()
        </div>

        <h2>3. Tabela de Referência Rápida</h2>
        <table>
            <thead>
                <tr>
                    <th>Barra (CIDR)</th>
                    <th>Máscara Decimal</th>
                    <th>Variação (Pulo)</th>
                    <th>Total de IPs</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>/20</td><td>255.255.240.0</td><td>16</td><td>4.096</td></tr>
                <tr><td>/21</td><td>255.255.248.0</td><td>8</td><td>2.048</td></tr>
                <tr><td>/22</td><td>255.255.252.0</td><td>4</td><td>1.024</td></tr>
                <tr><td>/23</td><td>255.255.254.0</td><td>2</td><td>512</td></tr>
            </tbody>
        </table>

        <div class="footer">
            Documento gerado para Paulo André Carminati - FIAP Cyber Defense 2026.
        </div>
    </div>
</body>
</html>
"""

# Salvar HTML e converter para PDF
output_pdf = "Calculadora_Subnet_Python_v1.pdf"
with open("temp.html", "w", encoding="utf-8") as f:
    f.write(html_content)

HTML(filename="temp.html").write_pdf(output_pdf)
os.remove("temp.html")