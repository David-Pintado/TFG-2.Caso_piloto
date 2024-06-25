import nltk
nltk.download('punkt')

from nltk.tokenize import RegexpTokenizer

# Crear un tokenizador personalizado con una expresión regular
tokenizer = RegexpTokenizer(r'\w+|[^\w\s]')

# Frase de ejemplo
frase = 'La casa es pequeña, pero a mi me gusta mucho. ¿A ti?'

# Tokenizar la frase
tokens = tokenizer.tokenize(frase)

print(tokens)


# Crear un tokenizador personalizado con una expresión regular
tokenizer = RegexpTokenizer(r'\w+|[^\w\s]')

# Frase de ejemplo en inglés
frase_ingles = "The house is small, but I like it a lot. Do you?"

# Tokenizar la frase en inglés
tokens_ingles = tokenizer.tokenize(frase_ingles)

print(tokens_ingles)