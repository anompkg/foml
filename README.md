# foml
Foml is a language for storing requests and URLs inside TOML.
FOML's name stands for "Format tOML".

# example
```config config.foml
[user]
	"name" = "anom"

	# $ at the begining of names makes variable formatable.	

	# You can use global path
	"$home" = "/home/{user.name}"  # global name

	# You can also access variables "localy" that are in the same [Sector] 
	# "$home" = "/home/{.name}"  # relative/local name
	# Symbols at the begging of name provide context
	# . Dot in this context mean local.
```

Run in `python` or even `uv run python`
```python main.py
import foml

fml = foml.load("config.foml")

print( fml["home"] )
# Output: /home/anom

```

