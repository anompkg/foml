# miniconf
the Morph Config with INI flavour.
Config is like .ini but sectors use OOP names.
Default sector is [] which is the root of the tree.
Usually when people define another section they can return back to default section.
Here every section is store inside root section and also sub sections are allowed

# example
```config
[Sector Name]
	KEY = VALUE
[User]
"Name" = "tfed"
"Home" = morph /home/<User.Name>

```
Note, it may seem that Home variable is using Name variable, but miniconf only cares about sectors and key with values.
The actual syntax showed here works in mfs and morph that will store its configs in miniconf format. 
So miniconf here will return plain text.
