import re

text = "Here 'an example' sentence with an apostrophe's. It showing possession: John book. Mind your ps and qs."

# Busca apóstrofes en contracciones y posesivos
apostrophes = re.findall(r"\b\w+'\w+\b", text)

# Busca comillas simples usadas para citas
quotes = re.findall(r"'\b[^']+\b'", text)

print(f"Apóstrofes encontrados ({len(apostrophes)}):")
for match in apostrophes:
    print(match)

print(f"\nComillas simples encontradas ({len(quotes)}):")
for match in quotes:
    print(match)
