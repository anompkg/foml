"""Morph Config with INI flavour"""


mcf = "config.mcf"

def readMConfig(mcf):
    with open(mcf) as config:
        print("Your config:")
        return ["[Default]"] +  [i.rstrip() for i in config.readlines()]

lines = readMConfig(mcf)

sectors = {}

for i in lines:
    if len(i) > 1 and i[0] == "[" and i[-1] == "]":
        sector = f"{i[1:-1]}"
        if sector == "":
            sector = "Default"
        print(f"Sector '{sector}'!")
    else:
        if sector not in sectors:
            sectors[sector] = []
        if i != "":
            sectors[sector] += [i]
    print(i)

print(sectors)
