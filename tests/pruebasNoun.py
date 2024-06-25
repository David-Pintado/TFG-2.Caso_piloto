import spacy

# Cargar el modelo de spaCy
nlp = spacy.load("en_core_web_sm")

# Cargar el modelo de lenguaje en español
nlp_es = spacy.load("es_core_news_sm")

def is_noun(word):
    # Procesar la palabra
    doc = nlp_es(word)
    
    # Asumimos que la palabra es la primera (y única) del documento
    token = doc[0]
    
    # Verificar si la palabra es un sustantivo
    return token.pos_

# Ejemplo de uso
word = "apple"
print(f"Is '{word}' a noun? {is_noun(word)}")

word = "partida"
print(f"Is '{word}' a noun? {is_noun(word)}")
