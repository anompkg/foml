"""Morph Config with INI flavour"""

import inspect, textwrap

class Miniconf:
    filepath = "config.mcf"
    lines = []
    sectors = {}

    def read(self):
        with open(self.filepath) as file:
            self.lines = [i.rstrip() for i in file.readlines()]

    def get_sector_name(self, line):
        sector = f"{line[1:-1]}"
        # [] Empty Sectors are redirecting to [Default] ones 
        sector = sector if sector else "Default"
        return sector


    def parse_miniconf(self):
        # Define Default sector
        sector = self.get_sector_name("[]")

        for i in self.lines:
            # If Sector Begins
            if len(i) > 1 and i[0] == "[" and i[-1] == "]":
                sector = self.get_sector_name(i)
                print(f"Sector '{sector}'!")
            else: # Otherwise its content
                if sector not in self.sectors:
                    self.sectors[sector] = []
                if i:
                    self.sectors[sector] += [inspect.cleandoc(i)]

    def __init__(self):
        self.read()
        self.parse_miniconf()

miniconf = Miniconf()
print(miniconf.filepath)
print(miniconf.lines)
print(miniconf.sectors)
