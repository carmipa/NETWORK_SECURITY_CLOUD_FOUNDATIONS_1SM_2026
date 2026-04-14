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
            <div class="col-md-6">
                <label class="form-label small text-secondary">Endereço IPv4 Base</label>
                <input type="text" name="ip" class="form-control bg-dark text-light border-secondary" 
                       placeholder="Ex: 172.16.0.0" value="{{ ip_pre }}" required>
            </div>
            <div class="col-md-3">
                <label class="form-label small text-secondary">Máscara (CIDR)</label>
                <input type="number" name="cidr" class="form-control bg-dark text-light border-secondary" 
                       placeholder="Ex: 22" min="0" max="32" value="{{ cidr_pre }}" required>
            </div>
            <div class="col-md-3 d-flex align-items-end">
                <button type="submit" class="btn btn-success w-100 fw-bold">DECOMPOR BITMAP</button>
            </div>
        </form>
    </div>

    {% if res %}
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
                <p>MÁSCARA: <span class="text-warning fw-bold">{{ res.mask }}</span></p>
                <p>REDE: {{ res.rede }}</p>
                <p>BROADCAST: {{ res.broad }}</p>
                <p>VARIAÇÃO (PULO): <span class="highlight-pulo">{{ res.pulo }}</span></p>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card-tech p-4 h-100 resumo-box" style="border-left-color: #238636;">
                <h6 class="text-info border-bottom border-secondary pb-2 mb-3">🧮 CAPACIDADE E HOSTS</h6>
                <p>ZEROS (HOST BITS): <span class="text-light fw-bold">{{ res.zeros }}</span></p>
                <p>CÁLCULO: 2^{{ res.zeros }} = {{ res.total }} IPs</p>
                <p>IPs ÚTEIS: <span class="text-success fw-bold" style="font-size: 1.2rem;">{{ res.uteis }}</span></p>
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


def processar(ip_s, cidr):
    try:
        # Conversão Bitwise
        parts = [int(p) for p in ip_s.split('.')]
        ip_i = (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]
        m_i = (0xffffffff << (32 - cidr)) & 0xffffffff
        r_i = ip_i & m_i
        b_i = r_i | (0xffffffff ^ m_i)

        fmt = lambda n: f"{(n >> 24) & 255}.{(n >> 16) & 255}.{(n >> 8) & 255}.{n & 255}"

        # Lógica de variação (pulo) por octeto relevante
        if cidr >= 24:
            pulo = 2 ** (32 - cidr)
        elif cidr >= 16:
            pulo = 2 ** (24 - cidr)
        else:
            pulo = 2 ** (16 - cidr)

        return {
            "mask": fmt(m_i), "rede": fmt(r_i), "broad": fmt(b_i),
            "bin_raw": bin(m_i)[2:].zfill(32), "zeros": 32 - cidr,
            "total": 2 ** (32 - cidr),
            "uteis": 2 ** (32 - cidr) - 2 if 2 ** (32 - cidr) > 2 else 0,
            "pulo": pulo
        }
    except Exception as e:
        return None


@app.route('/', methods=['GET', 'POST'])
def home():
    res, erro, ip_p, cidr_p = None, None, "", ""
    if request.method == 'POST':
        ip_p = request.form.get('ip', '').strip()
        cidr_raw = request.form.get('cidr', '').strip()

        # Validação robusta de entrada
        if ip_p and cidr_raw:
            try:
                cidr_val = int(cidr_raw)
                res = processar(ip_p, cidr_val)
                cidr_p = cidr_raw
                if res is None:
                    erro = "IP Inválido. Use o formato x.x.x.x"
            except ValueError:
                erro = "O CIDR deve ser um número inteiro."
        else:
            erro = "Por favor, preencha todos os campos."

    return render_template_string(HTML_TEMPLATE, res=res, erro=erro, ip_pre=ip_p, cidr_pre=cidr_p)


if __name__ == '__main__':
    app.run(debug=True)