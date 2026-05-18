"""Morph Config with INI flavour"""

import inspect, textwrap

class Miniconf:
    filepath = "config.mcf"

    def read(self):
        with open(self.filepath) as file:
            return[i.rstrip() for i in file.readlines()]

    def get_sector_name(s):
        sector = f"{s[1:-1]}"
        # [] Empty Sectors are redirecting to [Default] ones 
        sector = sector if sector else "Default"
        return sector


    def parse_miniconf(lines):
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
                    sectors[sector] += [inspect.cleandoc(i)]
            print(i)
        return sectors

    def __init__(self):
        lines = self.read()
        print(parse_Mconfig(lines))
