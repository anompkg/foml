"""Morph Config with INI flavour"""


mcf = "config.mcf"

def readfile(filepath):
    with open(filepath) as config:
        return[i.rstrip() for i in config.readlines()]

lines = readfile(mcf)

def get_sector_name(s):
    sector = f"{s[1:-1]}"
    # [] Empty Sectors are redirecting to [Default] ones 
    sector = sector if sector else "Default"
    return sector


def parse_Mconfig(lines):
    sectors = {}
    
    # Define Default sector
    sector = get_sector_name("[]")

    for i in lines:
        # If Sector Begins
        if len(i) > 1 and i[0] == "[" and i[-1] == "]":
            sector = get_sector_name(i)
            print(f"Sector '{sector}'!")
        else: # Otherwise its content
            if sector not in sectors:
                sectors[sector] = []
            if i:
                sectors[sector] += [i]
        print(i)
    return sectors

print(parse_Mconfig(lines))
