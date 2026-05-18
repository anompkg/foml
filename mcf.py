"""Morph Config with INI flavour"""

import inspect, textwrap

class Miniconf:
    filepath = "config.mcf"
    lines = []
    variables = {}

    def read(self):
        with open(self.filepath) as file:
            self.lines = [i.rstrip() for i in file.readlines()]

    def get_sector_name(self, line):
        return f"{line[1:-1]}"
    
    def get_varname(self, sector_name, varname):
        if not sector_name:
            return varname
        return f"{sector_name}.{varname}"
    

    def parse_miniconf(self):
        # Define Default sector
        sector = ""

        for i in self.lines:
            # If Sector Begins
            if len(i) > 1 and i[0] == "[" and i[-1] == "]":
                sector = self.get_sector_name(i)
                print(f"Sector '{sector}'!")
            elif not i:
                pass
            else:
                values = inspect.cleandoc(i).split("=", 1)
                key, value = values[0].strip(), values[1].strip()

                # Otherwise its content
                # if sector not in self.sectors:
                #     self.sectors[sector] = []
                self.variables[self.get_varname(sector, key)] = value

    def __init__(self):
        self.read()
        self.parse_miniconf()

miniconf = Miniconf()
print(miniconf.filepath)
print(miniconf.lines)
print(miniconf.variables)
