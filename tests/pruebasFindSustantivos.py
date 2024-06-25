import spacy

# Cargar el modelo de lenguaje en inglés
nlp = spacy.load("en_core_web_sm")

def extract_nouns_with_positions(sentence):
    """
    Extrae los sustantivos de una frase junto con sus posiciones, excluyendo los que son parte de compuestos.

    Args:
    sentence (str): La frase de la que se extraerán los sustantivos.

    Returns:
    List[Tuple[str, int, str, str]]: Una lista de tuplas que contiene el sustantivo, su posición,
                                     su dependencia y la palabra cabeza.
    """
    # Procesar la frase
    doc = nlp(sentence)
    
    # Extraer sustantivos que no sean parte de compuestos y agregar sus posiciones
    nouns_with_positions = [(token.text, token.i, token.dep_, token.head.text) for token in doc if token.pos_ == "NOUN" and token.dep_ != "compound"]
    
    return nouns_with_positions

# Ejemplo de uso
# sentence = "The cell membrane acts as a barrier between the internal environment of the cell and the external environment."
sentence = "The court issued a legal release, absolving the defendant of all criminal charges."
nouns_with_positions = extract_nouns_with_positions(sentence)
print(nouns_with_positions)
# Mostrar los resultados
for noun, position, dep, head in nouns_with_positions:
    print(f"Word: {noun}, Position: {position}, Dependency: {dep}, Head: {head}")

