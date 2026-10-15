"""Tira a pizza de linguagens das imagens 3D (ela só enxerga os repositórios públicos)."""
import glob
import re

ABRE = '<g transform="translate(40, 520)">'

for caminho in glob.glob("profile-3d-contrib/*.svg"):
    svg = open(caminho, encoding="utf-8").read()
    ini = svg.find(ABRE)
    if ini < 0:
        continue
    nivel, pos = 0, ini
    for tag in re.finditer(r"<g[\s>]|</g>", svg[ini:]):
        nivel += -1 if tag.group(0) == "</g>" else 1
        if nivel == 0:
            pos = ini + tag.end()
            break
    if pos > ini:
        open(caminho, "w", encoding="utf-8").write(svg[:ini] + svg[pos:])
        print("pizza removida:", caminho)
