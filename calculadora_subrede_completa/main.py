from flask import Flask, request, render_template_string

app = Flask(__name__)

# Template com CSS otimizado para eliminar rolagem e garantir responsividade
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberNet Framework | FIAP - Paulo André</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: 'Consolas', monospace; }
        .card-tech { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; margin-bottom: 20px; }
        .header-tech { border-left: 5px solid #238636; padding-left: 15px; color: #2ea043; margin-bottom: 25px; }

        /* Layout Flexbox para eliminar barra de rolagem horizontal */
        .bit-container { 
            display: flex; 
            flex-wrap: wrap; 
            justify-content: space-evenly; 
            gap: 20px; 
            padding: 20px; 
        }

        .octeto-group { display: flex; flex-direction: column; align-items: center; }
        .bit-row { display: flex; border: 1px solid #444c56; border-radius: 4px; overflow: hidden; }
        .bit-col { 
            display: flex; flex-direction: column; width: 42px; text-align: center; 
            border-right: 1px solid #444c56; 
        }
        .bit-col:last-child { border-right: none; }

        .info-top { font-size: 0.65rem; color: #768390; background: #21262d; padding: 2px 0; }
        .val-bin { font-size: 1.2rem; padding: 8px 0; font-weight: bold; }
        .bit-1 { background-color: #238636; color: white; }
        .bit-0 { background-color: #161b22; color: #484f58; }
        .peso-bot { font-size: 0.75rem; color: #58a6ff; padding: 4px 0; background: #0d1117; }
        .octeto-label { font-size: 0.8rem; color: #f2cc60; margin-top: 8px; font-weight: bold; }

        .resumo-box { border-left: 3px solid #58a6ff; padding-left: 10px; }
        .highlight-pulo { color: #f85149; font-size: 1.3rem; font-weight: bold; }

        /* Destaque da classe IPv4 (didática) */
        .classe-destaque {
            border-width: 3px;
            border-style: solid;
            border-radius: 10px;
            background: linear-gradient(165deg, #1c2128 0%, #161b22 55%, #0d1117 100%);
        }
        .classe-destaque-rotulo {
            font-size: 0.95rem;
            font-weight: 700;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            color: #8b949e;
            margin-bottom: 0.35rem;
        }
        .classe-destaque-valor {
            font-size: clamp(3.25rem, 11vw, 5rem);
            font-weight: 800;
            line-height: 1;
            margin: 0.2rem 0 0.45rem;
        }
        .classe-destaque-octeto { font-size: 1.15rem; color: #c9d1d9; }
        .classe-destaque-faixa {
            font-size: 1.05rem;
            color: #8b949e;
            margin-top: 0.65rem;
            max-width: 40rem;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.45;
        }
        .cv-a { border-color: #238636; }
        .cv-a .classe-destaque-valor { color: #3fb950; text-shadow: 0 0 28px rgba(63, 185, 80, 0.35); }
        .cv-b { border-color: #388bfd; }
        .cv-b .classe-destaque-valor { color: #79c0ff; text-shadow: 0 0 28px rgba(121, 192, 255, 0.25); }
        .cv-c { border-color: #d29922; }
        .cv-c .classe-destaque-valor { color: #e3b341; text-shadow: 0 0 28px rgba(227, 179, 65, 0.28); }
        .cv-d { border-color: #a371f7; }
        .cv-d .classe-destaque-valor { color: #d2a8ff; text-shadow: 0 0 24px rgba(210, 168, 255, 0.22); }
        .cv-e { border-color: #6e7681; }
        .cv-e .classe-destaque-valor { color: #b1bac4; }
        .cv-reservado, .cv-loopback, .cv-outros { border-color: #484f58; }
        .cv-reservado .classe-destaque-valor, .cv-loopback .classe-destaque-valor, .cv-outros .classe-destaque-valor { color: #f85149; }
    </style>
</head>
<body>
<div class="container py-5">
    <div class="header-tech">
        <h2>🛡️ FRAMEWORK DE REDES - ANÁLISE DIDÁTICA</h2>
        <p class="mb-0 text-secondary">Estudante: Paulo André Carminati | FIAP Cyber Defense 2026</p>
    </div>

    <div class="card-tech p-4 shadow">
        <form method="POST" class="row g-3">
            <div class="col-md-5">
                <label class="form-label small text-secondary">Endereço IPv4 (opcional)</label>
                <input type="text" name="ip" class="form-control bg-dark text-light border-secondary" 
                       placeholder="Ex.: 172.16.0.0 — deixe vazio se o exercício for só com máscara" value="{{ ip_pre }}">
                <div class="form-text text-secondary small">Sem IP: mostramos máscara, bits, tamanho do bloco e pulo. Rede/broadcast/hosts exigem um endereço no bloco.</div>
            </div>
            <div class="col-md-2">
                <label class="form-label small text-secondary">CIDR</label>
                <input type="number" name="cidr" class="form-control bg-dark text-light border-secondary" 
                       placeholder="22" min="0" max="32" value="{{ cidr_pre }}">
            </div>
            <div class="col-md-3">
                <label class="form-label small text-secondary">Ou máscara decimal</label>
                <input type="text" name="mask_decimal" class="form-control bg-dark text-light border-secondary" 
                       placeholder="Ex.: 255.255.255.240" value="{{ mask_dec_pre }}">
            </div>
            <div class="col-md-2 d-flex align-items-end">
                <button type="submit" class="btn btn-success w-100 fw-bold">DECOMPOR</button>
            </div>
        </form>
    </div>

    {% if res %}
    {% if res.somente_mascara %}
    <div class="classe-destaque cv-outros card-tech shadow mb-3 py-4 px-3 text-center">
        <div class="classe-destaque-rotulo">Modo só máscara (sem IP)</div>
        <div class="classe-destaque-valor">/{{ res.cidr }}</div>
        <div class="classe-destaque-octeto">Máscara: <span class="text-warning fw-bold">{{ res.mask }}</span></div>
        <div class="classe-destaque-faixa">Classe A/B/C depende do 1º octeto de um IP. Rede, broadcast e hosts só aparecem quando você informar um endereço dentro do bloco.</div>
    </div>
    {% else %}
    <div class="classe-destaque cv-{{ res.classe_variant }} card-tech shadow mb-3 py-4 px-3 text-center">
        <div class="classe-destaque-rotulo">Classe IPv4 clássica</div>
        <div class="classe-destaque-valor">{{ res.classe }}</div>
        <div class="classe-destaque-octeto">1º octeto do IP informado: <span class="text-warning fw-bold">{{ res.primeiro_octeto }}</span></div>
        <div class="classe-destaque-faixa">{{ res.classe_faixa }}</div>
    </div>
    {% endif %}

    <div class="card-tech shadow">
        <div class="p-3 border-bottom border-secondary text-info fw-bold">📊 DECOMPOSIÇÃO DO ARRAY DE 32 BITS</div>
        <div class="bit-container">
            {% for oct_idx in range(4) %}
            <div class="octeto-group">
                <div class="bit-row shadow-sm">
                    {% for bit_idx in range(8) %}
                        {% set total_idx = (oct_idx * 8) + bit_idx %}
                        {% set bit_val = res.bin_raw[total_idx] %}
                        <div class="bit-col">
                            <div class="info-top">#{{ total_idx + 1 }}</div>
                            <div class="info-top text-danger" style="font-size: 0.6rem;">2^{{ 31 - total_idx }}</div>
                            <div class="val-bin {{ 'bit-1' if bit_val == '1' else 'bit-0' }}">{{ bit_val }}</div>
                            <div class="peso-bot">{{ 2**(7 - bit_idx) }}</div>
                        </div>
                    {% endfor %}
                </div>
                <div class="octeto-label">OCTETO {{ oct_idx + 1 }}: {{ res.mask.split('.')[oct_idx] }}</div>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="row g-3">
        <div class="col-md-6">
            <div class="card-tech p-4 h-100 resumo-box">
                <h6 class="text-info border-bottom border-secondary pb-2 mb-3">📋 RESULTADOS DECIMAIS</h6>
                <p>MÁSCARA: <span class="text-warning fw-bold">{{ res.mask }}</span> <span class="text-secondary small">/ {{ res.cidr }}</span></p>
                {% if res.somente_mascara %}
                <p>REDE: <span class="text-secondary">—</span> <span class="small text-secondary">(informe um IP)</span></p>
                <p>PRIMEIRO IP ÚTIL (1º host): <span class="text-secondary">—</span></p>
                <p>ÚLTIMO IP ÚTIL (último host): <span class="text-secondary">—</span></p>
                <p>BROADCAST: <span class="text-secondary">—</span></p>
                {% else %}
                <p>REDE: {{ res.rede }}</p>
                <p>PRIMEIRO IP ÚTIL (1º host): <span class="text-success">{{ res.primeiro_host }}</span></p>
                <p>ÚLTIMO IP ÚTIL (último host): <span class="text-success">{{ res.ultimo_host }}</span></p>
                <p>BROADCAST: {{ res.broad }}</p>
                {% endif %}
                <p>VARIAÇÃO (PULO): <span class="highlight-pulo">{{ res.pulo }}</span></p>
                {% if not res.somente_mascara %}
                <p class="small text-secondary mb-0">Gateway comum em laboratório: costuma ser o 1º host ({{ res.primeiro_host }}). DNS não vem do IP/máscara; é configurado (ex.: 8.8.8.8 ou o do provedor).</p>
                {% else %}
                <p class="small text-secondary mb-0">Com só a máscara você calcula prefixo, bits de host, tamanho do bloco e incremento entre sub-redes; o professor costuma pedir isso antes de fixar um IP de rede.</p>
                {% endif %}
            </div>
        </div>
        <div class="col-md-6">
            <div class="card-tech p-4 h-100 resumo-box" style="border-left-color: #238636;">
                <h6 class="text-info border-bottom border-secondary pb-2 mb-3">🧮 CAPACIDADE E HOSTS</h6>
                <p>ZEROS (HOST BITS): <span class="text-light fw-bold">{{ res.zeros }}</span></p>
                <p>IPs NO BLOCO (rede → broadcast): 2^{{ res.zeros }} = <span class="text-warning fw-bold">{{ res.total }}</span></p>
                <p>IPs ÚTEIS (RFC comum, exclui rede e broadcast): <span class="text-success fw-bold" style="font-size: 1.2rem;">{{ res.uteis }}</span></p>
                {% if res.cidr == 31 %}
                <p class="small text-secondary mb-0">/31 (RFC 3021): os 2 endereços podem ser hosts em enlace ponto a ponto; sem rede/broadcast clássicos.</p>
                {% elif res.cidr == 32 %}
                <p class="small text-secondary mb-0">/32: um único endereço (host ou rota); sem sub-rede de múltiplos hosts.</p>
                {% endif %}
            </div>
        </div>
    </div>
    {% endif %}

    {% if erro %}
    <div class="alert alert-danger bg-dark text-danger border-danger shadow">{{ erro }}</div>
    {% endif %}
</div>
</body>
</html>
"""


def _classe_ipv4_didatica(o1):
    """Classificação didática pelo 1º octeto (IPv4 classful); CIDR tornou isso só referência histórica."""
    if o1 == 0:
        return "Reservado", "(0.0.0.0/8 — não roteável na Internet)"
    if o1 == 127:
        return "Loopback", "(127.0.0.0/8)"
    if 1 <= o1 <= 126:
        return "A", "faixa clássica 1–126 no 1º octeto"
    if 128 <= o1 <= 191:
        return "B", "faixa clássica 128–191 no 1º octeto"
    if 192 <= o1 <= 223:
        return "C", "faixa clássica 192–223 no 1º octeto"
    if 224 <= o1 <= 239:
        return "D", "multicast (224–239)"
    if 240 <= o1 <= 255:
        return "E", "experimental / reservado (240–255)"
    return "—", ""


def _classe_variant_css(classe):
    """Slug estável para classes CSS do banner de destaque."""
    return {
        "A": "a",
        "B": "b",
        "C": "c",
        "D": "d",
        "E": "e",
        "Reservado": "reservado",
        "Loopback": "loopback",
        "—": "outros",
    }.get(classe, "outros")


def mascara_dotted_para_cidr(mask_s):
    """Converte máscara IPv4 pontuada (bits de rede contíguos) em prefixo /0–/32."""
    try:
        parts = [int(p.strip()) for p in mask_s.strip().split(".")]
    except ValueError:
        return None
    if len(parts) != 4 or any(o < 0 or o > 255 for o in parts):
        return None
    val = (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]
    val &= 0xffffffff
    inv = (~val) & 0xffffffff
    if inv != 0 and (inv & (inv + 1)) != 0:
        return None
    return val.bit_count()


def _core_mascara(cidr):
    """Dados derivados só do CIDR (máscara, bitmap, capacidade, pulo)."""
    if not isinstance(cidr, int) or not (0 <= cidr <= 32):
        return None
    m_i = (0xffffffff << (32 - cidr)) & 0xffffffff
    fmt = lambda n: f"{(n >> 24) & 255}.{(n >> 16) & 255}.{(n >> 8) & 255}.{n & 255}"
    if cidr >= 24:
        pulo = 2 ** (32 - cidr)
    elif cidr >= 16:
        pulo = 2 ** (24 - cidr)
    else:
        pulo = 2 ** (16 - cidr)

    tamanho = 2 ** (32 - cidr)
    if cidr == 32:
        uteis = 1
    elif cidr == 31:
        uteis = 2
    elif tamanho > 2:
        uteis = tamanho - 2
    else:
        uteis = 0

    return {
        "mask": fmt(m_i),
        "bin_raw": bin(m_i)[2:].zfill(32),
        "zeros": 32 - cidr,
        "total": tamanho,
        "uteis": uteis,
        "pulo": pulo,
        "cidr": cidr,
        "_m_i": m_i,
    }


def processar_somente_mascara(cidr):
    """Exercício com máscara/CIDR sem endereço IP: sem rede/broadcast/hosts específicos."""
    c = _core_mascara(cidr)
    if c is None:
        return None
    out = {k: v for k, v in c.items() if k != "_m_i"}
    out["somente_mascara"] = True
    out["rede"] = out["broad"] = out["primeiro_host"] = out["ultimo_host"] = "—"
    return out


def processar(ip_s, cidr):
    c = _core_mascara(cidr)
    if c is None:
        return None
    try:
        parts = [int(p) for p in ip_s.split(".")]
        if len(parts) != 4 or any(p < 0 or p > 255 for p in parts):
            return None
        m_i = c["_m_i"]
        ip_i = (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]
        r_i = ip_i & m_i
        b_i = r_i | (0xffffffff ^ m_i)
        fmt = lambda n: f"{(n >> 24) & 255}.{(n >> 16) & 255}.{(n >> 8) & 255}.{n & 255}"
        tamanho = c["total"]
        if cidr == 32:
            primeiro_host = ultimo_host = fmt(r_i)
        elif cidr == 31:
            primeiro_host = fmt(r_i)
            ultimo_host = fmt(r_i + 1)
        elif tamanho > 2:
            primeiro_host = fmt(r_i + 1)
            ultimo_host = fmt(b_i - 1)
        else:
            primeiro_host = ultimo_host = "—"

        classe, classe_faixa = _classe_ipv4_didatica(parts[0])
        out = {k: v for k, v in c.items() if k != "_m_i"}
        out.update(
            {
                "somente_mascara": False,
                "rede": fmt(r_i),
                "broad": fmt(b_i),
                "primeiro_host": primeiro_host,
                "ultimo_host": ultimo_host,
                "classe": classe,
                "classe_faixa": classe_faixa,
                "classe_variant": _classe_variant_css(classe),
                "primeiro_octeto": parts[0],
            }
        )
        return out
    except Exception:
        return None


@app.route("/", methods=["GET", "POST"])
def home():
    res, erro = None, None
    ip_p, cidr_p, mask_dec_p = "", "", ""
    if request.method == "POST":
        ip_p = request.form.get("ip", "").strip()
        cidr_raw = request.form.get("cidr", "").strip()
        mask_dec_p = request.form.get("mask_decimal", "").strip()

        cidr_val = None
        if not cidr_raw and not mask_dec_p:
            erro = "Informe o CIDR (0 a 32) ou a máscara em decimal (ex.: 255.255.255.240)."
        else:
            if cidr_raw:
                try:
                    cidr_val = int(cidr_raw)
                except ValueError:
                    erro = "O CIDR deve ser um número inteiro entre 0 e 32."
            if erro is None and cidr_val is None and mask_dec_p:
                cidr_val = mascara_dotted_para_cidr(mask_dec_p)
                if cidr_val is None:
                    erro = (
                        "Máscara decimal inválida. Use uma máscara contígua "
                        "(ex.: 255.255.255.0), não valores como 255.0.255.0."
                    )
            if erro is None and cidr_raw and mask_dec_p:
                parsed = mascara_dotted_para_cidr(mask_dec_p)
                if parsed is None:
                    erro = "Máscara decimal inválida."
                elif parsed != cidr_val:
                    erro = (
                        "O CIDR não corresponde à máscara decimal. "
                        "Deixe um dos campos em branco ou ajuste os valores."
                    )

        if erro is None and cidr_val is not None and not (0 <= cidr_val <= 32):
            erro = "CIDR deve estar entre 0 e 32."

        if erro is None and cidr_val is not None:
            if ip_p:
                res = processar(ip_p, cidr_val)
                if res is None:
                    erro = "IP inválido. Use x.x.x.x com octetos de 0 a 255."
            else:
                res = processar_somente_mascara(cidr_val)

            if erro is None and res is not None:
                if cidr_raw:
                    cidr_p = cidr_raw
                else:
                    cidr_p = str(cidr_val)

    return render_template_string(
        HTML_TEMPLATE,
        res=res,
        erro=erro,
        ip_pre=ip_p,
        cidr_pre=cidr_p,
        mask_dec_pre=mask_dec_p,
    )


if __name__ == '__main__':
    app.run(debug=True)