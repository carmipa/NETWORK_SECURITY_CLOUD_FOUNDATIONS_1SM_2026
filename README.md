<div align="center">

# 🌐 Network Security Cloud Foundations - 1SM 2026
**Fundamentos de Redes de Computadores e Internet**

![Networking Banner](https://img.shields.io/badge/FIAP-1SM_2026-ED145B?style=for-the-badge&logo=fiap)
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</div>

---

## 📖 Sobre o Projeto
Este repositório armazena os materiais e conceitos abordados na disciplina **Network Security Cloud Foundations**, focando nos princípios arquitetônicos das **Redes de Computadores** e da **Internet**, englobando desde protocolos fundamentais até a organização lógica de IPs e portas de comunicação.

---

## 🚀 Tecnologias e Conceitos Abordados

<div align="center">
  <img src="https://img.shields.io/badge/TCP/IP-000000?style=for-the-badge&logo=Transmission-Control-Protocol" />
  <img src="https://img.shields.io/badge/DNS-005571?style=for-the-badge&logo=Cloudflare" />
  <img src="https://img.shields.io/badge/DHCP-FFD166?style=for-the-badge&logo=quicklook" />
  <img src="https://img.shields.io/badge/Prompt_de_Comando-4D4D4D?style=for-the-badge&logo=windows-terminal" />
</div>

### 📌 Resumo Lógico (Glossário Network)
Baseado no material da disciplina (`Material_01_Glossario_Network(1).ppt`), exploramos os seguintes fundamentos:
- **Redes de Computadores**: Conjunto de dispositivos conectados compartilhando dados e recursos.
- **Protocolo TCP/IP**: A base da comunicação na Internet (Transfer Control Protocol & Internet Protocol).
- **Endereçamento IP, MAC-ADDRESS & Mascaras (Sub-redes)**: 
  - *Classe A*: 255.0.0.0
  - *Classe B*: 255.255.0.0
  - *Classe C*: 255.255.255.0
- **Serviços Críticos**:
  - `DNS` (Domain Name System): Traduz o nome do host (domínio) para o IP do seu provedor.
  - `DHCP` (Dynamic Host Configuration Protocol): Atribui IPs e configurações de rede de forma automática.
  - `Default Gateway`: A porta de saída que interliga a residência/LAN à malha da Internet.
- **Ferramentas de Diagnóstico**: Uso de comandos clássicos como `ipconfig /all` e `ping`.

---

## 🗺️ Diagrama de Topologia de Rede (Mermaid)

Aqui está um diagrama de arquitetura de rede básica baseada nos ensinamentos das aulas:

```mermaid
graph TD
    subgraph Internet
        WWW[Internet / Web]
        DNS[Servidor DNS]
    end

    subgraph "LAN - Rede Local Corporativa/Residencial"
        Router[Roteador / Default Gateway / DHCP]
        Switch[Switch Ethernet]
        HostA[Dispositivo 1 - IP Dinâmico]
        HostB[Dispositivo 2 - IP Dinâmico]
        HostC[Dispositivo 3 - Wi-Fi]
    end

    Router -- "Conexão de Saída" --> WWW
    Router -- "Tradução de Nomes" --> DNS
    Router -- "Cabo Físico" --> Switch
    Switch --> HostA & HostB
    Router -. "Wi-Fi" .-> HostC

    classDef inet fill:#2d3436,stroke:#74b9ff,stroke-width:2px,color:#fff;
    classDef lan fill:#0984e3,stroke:#fff,stroke-width:2px,color:#fff;
    class WWW,DNS inet;
    class Router,Switch,HostA,HostB,HostC lan;
```

---

## 🛠️ Comandos de Terminais Essenciais
Aqui temos uma lista dos comandos úteis abordados:

| Ícone | Comando Windows | Descrição da Funcionalidade |
|:---:|---|---|
| 🔍 | `ipconfig` / `ipconfig /all` | Permite a leitura das configurações de rede ativas (IP, Máscara, Gateway, MAC).|
| ⚡ | `ping <endereço>` | Dispara pacotes para testar a conectividade com outro IP ou host na rede. |
| 🛡️ | `telnet` / `ssh` | Protocolos utilizados para executar acesso remoto (e promover segurança, no caso do SSH). |

---

## 📎 Referências do Projeto
> *Nota: Os conceitos acima foram extraídos e adaptados a partir do material principal da disciplina depositado no repositório (`aulas/Material_01_Glossario_Network(1).ppt`).*

<br>

<div align="center">
  <i>Desenvolvido ao longo do 1º Semestre de 2026 na FIAP.</i><br>
  <a href="https://github.com/FIAP" target="_blank">
    <img src="https://img.shields.io/badge/FIAP-Study_Repository-black?style=flat-square&logo=github">
  </a>
</div>
