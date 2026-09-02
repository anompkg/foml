from networkx import degree
from httplib2 import RelativeURIError
import json
import toml
import jsonpath_ng
from string import Formatter


class NameCollisionError(ValueError):
    pass


symbols = {
    "#": "Raw",
    "$": "Format",
    "!": "Executable",
    ".": "Local",
}


def is_foml_name(s):
    "Check if variable's name in toml named in foml style"
    for key, value in symbols.items():
        if s.startswith(key):
            return value
    return None


def decode_name(s):
    "Decode FOML name"
    sample = s
    meta = {}

    fmt = is_foml_name(sample)
    while fmt:
        sample = sample[1:]
        if fmt not in meta:
            meta[fmt] = True
        fmt = is_foml_name(sample)
    meta["name"] = sample
    return meta


class FOML:
    "Format Obvious Minimal Language."

    def __init__(self, filename="config.toml"):
        self.meta = {}
        self.load(filename)
        self.print()

    def load(self, filename):
        self.filename = filename
        self.json_data = toml.load(self.filename)

    def verify(self, d):
        for key, value in d.items():
            if isinstance(value, dict):
                self.verify(value)

    def print(self):
        print("config:", self.filename)
        print("foml:", self.json_data)


f = FOML()
