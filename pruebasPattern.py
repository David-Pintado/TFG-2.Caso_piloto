from textblob import Word

# Verbo de ejemplo en inglés
verb_en = "run"

# Crear un objeto Word con el verbo en inglés
word = Word(verb_en)

# Obtener todas las formas conjugadas del verbo en inglés
conjugations_en = word.conjugate()
print(f"Todas las formas (inglés): {conjugations_en}")
