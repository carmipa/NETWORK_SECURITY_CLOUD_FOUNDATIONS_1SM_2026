import math

def calcular_rede(ip_str, cidr):
    # Converte o IP para uma lista de inteiros
    octetos = [int(o) for o in ip_str.split('.')]
    
    # Representação do IP em um único número de 32 bits
    ip_32bits = (octetos[0] << 24) + (octetos[1] << 16) + (octetos[2] << 8) + octetos[3]
    
    # Cálculo da máscara de sub-rede
    mask_32bits = (0xffffffff << (32 - cidr)) & 0xffffffff
    
    # Cálculo do endereço de rede e broadcast
    rede_32bits = ip_32bits & mask_32bits
    broadcast_32bits = rede_32bits | (0xffffffff ^ mask_32bits)
    
    # Funções auxiliares para converter de volta para decimal pontuado
    def int_to_ip(n):
        return f"{(n >> 24) & 0xff}.{(n >> 16) & 0xff}.{(n >> 8) & 0xff}.{n & 0xff}"

    def int_to_bin(n):
        b = bin(n)[2:].zfill(32)
        return f"{b[0:8]}.{b[8:16]}.{b[16:24]}.{b[24:32]}"

    # Informações calculadas
    num_ips = 2**(32 - cidr)
    ips_uteis = num_ips - 2 if num_ips > 2 else 0

    print("-" * 50)
    print(f"ANÁLISE DE REDE: {ip_str}/{cidr}")
    print("-" * 50)
    print(f"Máscara Decimal:    {int_to_ip(mask_32bits)}")
    print(f"Máscara Binária:    {int_to_bin(mask_32bits)}")
    print(f"Endereço de Rede:   {int_to_ip(rede_32bits)}")
    print(f"Endereço Broadcast: {int_to_ip(broadcast_32bits)}")
    print("-" * 50)
    print(f"Total de Endereços: {num_ips}")
    print(f"Hosts (IPs Úteis):  {ips_uteis}")
    print(f"Variação (Pulo):    {2**(32-cidr) // 256 if cidr <= 24 else 2**(32-cidr)}")
    print("-" * 50)

# Exemplo baseado no seu exercício da FIAP
calcular_rede("172.19.0.0", 21)