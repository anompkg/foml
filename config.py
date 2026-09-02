import json
import toml
import jsonpath_ng
from string import Formatter


class ConfigError(ValueError):
    pass


class Morph:
    def __init__(self, filename="config.toml"):
        self.json_data = toml.load(filename)

        self.check()

        self.jsonpath_expr = jsonpath_ng.parse("$.math.pi")
        self.print()

    def check(self):
        self.entities = {}
        self._collect_entities(self.json_data)
        print("entities:", self.entities)
        self.json_data = self._check_table(self.json_data)

    def _collect_entities(self, data, path=()):
        """
        Build a lookup table containing every entity by dotted path.

        For example:

            [math]
            pi = 3.14

        becomes:

            math.pi -> ("pi", 3.14)
        """
        for key, value in data.items():
            name = key[1:] if key.startswith("$") else key
            full_path = ".".join((*path, name))

            if full_path in self.entities:
                raise ConfigError(
                    f"Duplicate entity: {full_path!r}"
                )

            if key.startswith("$") and not isinstance(value, str):
                raise ConfigError(
                    f"{full_path!r}: morph variables must contain strings; "
                    f"got {type(value).__name__}"
                )

            self.entities[full_path] = {
                "key": key,
                "value": value,
                "path": path,
            }

            if isinstance(value, dict):
                self._collect_entities(value, (*path, name))

    def _check_table(self, data, path=()):
        result = {}

        # Detect pi and "$pi" in the same table.
        names = {}

        for key in data:
            name = key[1:] if key.startswith("$") else key

            if name in names:
                raise ConfigError(
                    f"Duplicate entity in {'.'.join(path) or '<root>'}: "
                    f"{names[name]!r} and {key!r}"
                )

            names[name] = key

        for key, value in data.items():
            if isinstance(value, dict):
                value = self._check_table(value, (*path, key))

            elif key.startswith("$"):
                value = self._resolve_format(
                    value,
                    current_path=path,
                    stack=[]
                )

            result[key] = value

        return result

    def _find_entity(self, reference, current_path):
        """
        Resolve a reference.

        Lookup order:

        1. Relative to the current table
        2. Absolute dotted path
        3. Unique entity name anywhere in the config
        """
        reference = reference.lstrip("$#")

        # Try relative paths first.
        for index in range(len(current_path), -1, -1):
            candidate = ".".join(
                (*current_path[:index], reference)
            )

            if candidate in self.entities:
                return candidate

        # Try the reference as an absolute path.
        if reference in self.entities:
            return reference

        # Finally, allow a unique short name.
        matches = [
            path
            for path in self.entities
            if path.rsplit(".", 1)[-1] == reference
        ]

        if len(matches) == 1:
            return matches[0]

        if not matches:
            raise ConfigError(
                f"Unknown entity referenced: {reference!r}"
            )

        raise ConfigError(
            f"Ambiguous entity reference {reference!r}: "
            + ", ".join(matches)
        )

    def _raw_value(self, entity_path):
        return self.entities[entity_path]["value"]

    def _default_value(self, entity_path, stack):
        """
        Default behavior:

        - Regular variable: return its raw value.
        - Morph variable: process its format string.
        """
        entity = self.entities[entity_path]
        key = entity["key"]
        value = entity["value"]

        if not key.startswith("$"):
            return value

        return self._resolve_format(
            value,
            current_path=entity["path"],
            stack=stack + [entity_path]
        )

    def _resolve_reference(self, field, current_path, stack):
        """
        Resolve one placeholder:

            {name}      default behavior
            {$name}     force format processing
            {#name}     force raw value
        """
        if field.startswith("$"):
            mode = "format"
            reference = field[1:]

        elif field.startswith("#"):
            mode = "raw"
            reference = field[1:]

        else:
            mode = "default"
            reference = field

        entity_path = self._find_entity(reference, current_path)

        if entity_path in stack:
            start = stack.index(entity_path)
            cycle = " -> ".join(
                [*stack[start:], entity_path]
            )
            raise ConfigError(f"Circular reference: {cycle}")

        if mode == "raw":
            return self._raw_value(entity_path)

        value = self._default_value(entity_path, stack)

        if mode == "format":
            if not isinstance(value, str):
                raise ConfigError(
                    f"Cannot format {reference!r}: "
                    f"expected string, got {type(value).__name__}"
                )

            return self._resolve_format(
                value,
                current_path=self.entities[entity_path]["path"],
                stack=stack + [entity_path]
            )

        return value

    def _resolve_format(self, template, current_path, stack):
        formatter = Formatter()
        replacements = {}

        for _, field_name, _, _ in formatter.parse(template):
            if field_name is None:
                continue

            if field_name not in replacements:
                replacements[field_name] = self._resolve_reference(
                    field_name,
                    current_path,
                    stack
                )

        return template.format(**replacements)

    def print(self):
        print(json.dumps(self.json_data))

        extracted_data = self.jsonpath_expr.find(self.json_data)

        print(
            f"The variable extracted_data is of type "
            f"{type(extracted_data)} and it has "
            f"{len(extracted_data)} elements."
        )

        if extracted_data:
            print(
                f"The value of extracted_data is "
                f"{extracted_data[0].value}"
            )
            print(
                f"The value of extracted_data is "
                f"{extracted_data}"
            )


m = Morph()


