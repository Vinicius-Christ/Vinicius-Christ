"""Gera assets/linguagens.svg com as linguagens de todos os repositórios (inclusive os privados).

Uso: GH_TOKEN=<token com leitura dos repositórios> python3 scripts/linguagens.py
Os números vêm da API do GitHub (bytes de código por linguagem, contados pelo Linguist).
"""
import json
import os
import urllib.request

USUARIO = "Vinicius-Christ"
REPOS = ["Jarvis-Project", "EmotionalSense", "mc-panel", "CircuitosLogicos-Proj"]
# Linguagens do trabalho que não ficam no GitHub: aparecem sem porcentagem.
TRABALHO = [("Java", "#b07219"), ("SQL", "#e38c00"), ("DAX · Power BI", "#f2c811")]
CORES = {
    "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "C++": "#f34b7d", "Python": "#3572a5",
    "Rust": "#dea584", "CSS": "#8a5cf6", "Shell": "#89e051", "HTML": "#e34c26",
    "PowerShell": "#5391fe", "Batchfile": "#c1f12e",
}
NOMES = {"Batchfile": "Batch"}


def bytes_por_linguagem():
    total = {}
    for repo in REPOS:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{USUARIO}/{repo}/languages",
            headers={"Authorization": f"Bearer {os.environ['GH_TOKEN']}", "Accept": "application/vnd.github+json"},
        )
        for ling, n in json.load(urllib.request.urlopen(req)).items():
            total[ling] = total.get(ling, 0) + n
    return sorted(total.items(), key=lambda kv: -kv[1])


def svg(dados):
    soma = sum(n for _, n in dados)
    itens = [(NOMES.get(l, l), n * 100 / soma, CORES.get(l, "#94a3b8")) for l, n in dados]
    largura, barra_x, barra_w = 1000, 40, 920
    partes = []

    # Barra empilhada no topo, crescendo da esquerda para a direita
    x = barra_x
    for i, (_, pct, cor) in enumerate(itens):
        w = barra_w * pct / 100
        partes.append(
            f'<rect x="{x:.2f}" y="78" width="{w:.2f}" height="14" fill="{cor}">'
            f'<animate attributeName="width" values="0;0;{w:.2f}" keyTimes="0;{i * 0.08 / (1.2 + i * 0.08):.3f};1" dur="{1.2 + i * 0.08:.2f}s" fill="freeze"/></rect>'
        )
        x += w

    # Lista em duas colunas, cada linha com a própria barrinha
    col_w, lin_h, y0 = 440, 34, 128
    metade = (len(itens) + 1) // 2
    for i, (nome, pct, cor) in enumerate(itens):
        cx = 40 + (i // metade) * (col_w + 40)
        cy = y0 + (i % metade) * lin_h
        w = max(2, 215 * pct / itens[0][1])
        txt = f"{pct:.1f}%" if pct >= 0.1 else "&lt;0,1%"
        partes.append(
            f'<g class="lin" style="animation-delay:{0.3 + i * 0.07:.2f}s">'
            f'<circle cx="{cx + 6}" cy="{cy}" r="6" fill="{cor}"/>'
            f'<text x="{cx + 22}" y="{cy + 5}" class="nome">{nome}</text>'
            f'<rect x="{cx + 150}" y="{cy - 5}" width="215" height="10" rx="5" fill="#ffffff" fill-opacity=".06"/>'
            f'<rect x="{cx + 150}" y="{cy - 5}" width="{w:.1f}" height="10" rx="5" fill="{cor}">'
            f'<animate attributeName="width" values="0;0;{w:.1f}" keyTimes="0;{(0.3 + i * 0.07) / (1.7 + i * 0.07):.3f};1" dur="{1.7 + i * 0.07:.2f}s" fill="freeze"/></rect>'
            f'<text x="{cx + col_w}" y="{cy + 5}" class="pct" text-anchor="end">{txt.replace(".", ",")}</text></g>'
        )

    y_trab = y0 + metade * lin_h + 16
    chips, cx = [], 40 + 150
    for nome, cor in TRABALHO:
        w = 22 + len(nome) * 8.6
        chips.append(
            f'<rect x="{cx}" y="{y_trab - 15}" width="{w:.0f}" height="26" rx="13" fill="{cor}" fill-opacity=".16" stroke="{cor}" stroke-opacity=".6"/>'
            f'<text x="{cx + w / 2:.0f}" y="{y_trab + 3}" class="chip" text-anchor="middle">{nome}</text>'
        )
        cx += w + 10
    altura = y_trab + 34

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" height="{altura}" viewBox="0 0 {largura} {altura}" role="img" aria-label="Linguagens usadas nos meus projetos">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0b1a"/><stop offset=".6" stop-color="#160f2e"/><stop offset="1" stop-color="#0a2a33"/></linearGradient>
    <clipPath id="barra"><rect x="{barra_x}" y="78" width="{barra_w}" height="14" rx="7"/></clipPath>
    <style>
      text {{ font-family: 'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif; fill: #e2e8f0; }}
      .titulo {{ font-size: 22px; font-weight: 700; }}
      .sub {{ font-size: 13px; fill: #94a3b8; }}
      .nome {{ font-size: 15px; font-weight: 600; }}
      .pct {{ font-size: 14px; fill: #cbd5e1; font-variant-numeric: tabular-nums; }}
      .chip {{ font-size: 13px; font-weight: 600; }}
      .rot {{ font-size: 13px; fill: #94a3b8; }}
      .lin {{ animation: surge .6s ease-out backwards; }}
      @keyframes surge {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
      @media (prefers-reduced-motion: reduce) {{ .lin {{ animation: none; }} }}
    </style>
  </defs>
  <rect width="{largura}" height="{altura}" rx="16" fill="url(#bg)"/>
  <rect x=".5" y=".5" width="{largura - 1}" height="{altura - 1}" rx="16" fill="none" stroke="#8b5cf6" stroke-opacity=".35"/>
  <text x="40" y="44" class="titulo">Linguagens nos meus projetos</text>
  <text x="{largura - 40}" y="44" class="sub" text-anchor="end">todos os repositórios, inclusive os privados</text>
  <g clip-path="url(#barra)"><rect x="{barra_x}" y="78" width="{barra_w}" height="14" fill="#ffffff" fill-opacity=".06"/>{"".join(p for p in partes[:len(itens)])}</g>
  {"".join(partes[len(itens):])}
  <text x="40" y="{y_trab + 4}" class="rot">Também no trabalho:</text>
  {"".join(chips)}
</svg>
'''


if __name__ == "__main__":
    destino = os.path.join(os.path.dirname(__file__), "..", "assets", "linguagens.svg")
    open(destino, "w", encoding="utf-8").write(svg(bytes_por_linguagem()))
    print("gerado:", os.path.normpath(destino))
