# MCF
the Morph Config with INI flavour.
Config is like .ini but sectors use OOP names.
Default sector is [] which is the root of the tree.
Usually when people define another section they can return back to default section.
Here every section is store inside root section and also sub sections are allowed

# example
```config
"User Home" = morph /home/<User Name>

```