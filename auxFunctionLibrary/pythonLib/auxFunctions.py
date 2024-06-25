

import spacy
from itertools import product
import re
import random
import nltk

# Descargar el recurso necesario
nltk.download('averaged_perceptron_tagger')

# Cargar el modelo de lenguaje en español
nlp_es = spacy.load("es_core_news_sm")

# Cargar el modelo de lenguaje en inglés
nlp_en = spacy.load("en_core_web_sm")

def validation_find_element_with_difference(lst, plural_list, difference):
    if not lst:
        return []

    # Filtrar los elementos que tienen el segundo valor mayor o igual a la diferencia
    filtered_list = [element for element in lst if element[1] >= difference]

    if not filtered_list:
        return []
      
    new_list = [(element,pos) for (element,pos) in filtered_list if element in plural_list]
    if new_list:
        return new_list[0]

    # Encontrar el máximo valor del segundo elemento en la lista filtrada
    max_value = max(filtered_list, key=lambda x: x[1])[1]

    # Obtener todos los elementos con el valor máximo
    max_elements = [element for element in filtered_list if element[1] == max_value]

    # Elegir uno al azar en caso de empate
    return random.choice(max_elements)

def find_element_with_difference(lst, difference):
    if not lst:
        return []

    # Filtrar los elementos que tienen el segundo valor mayor o igual a la diferencia
    filtered_list = [element for element in lst if element[1] >= difference]

    if not filtered_list:
        return []

    # Encontrar el máximo valor del segundo elemento en la lista filtrada
    max_value = max(filtered_list, key=lambda x: x[1])[1]

    # Obtener todos los elementos con el valor máximo
    max_elements = [element for element in filtered_list if element[1] == max_value]

    # Elegir uno al azar en caso de empate
    return random.choice(max_elements)

def normalize_list_english(lista):
    # Convertir la lista a un conjunto para buscar palabras de manera eficiente
    palabras_set = set(palabra for palabra, _ in lista)
    # Lista para almacenar los plurales que se eliminarán
    plurales_a_eliminar = []

    for palabra, conteo in lista:
        pluralize_word_list = pluralize_word_english(palabra)[1:]
        for plural in pluralize_word_list:
            if plural in palabras_set:
                # Si el plural está en la lista, encontrar su índice y sumar el conteo
                try:
                    index_plural = next(index for index, (word, _) in enumerate(lista) if word == plural)
                    index_palabra = next(index for index, (word, _) in enumerate(lista) if word == palabra)
                    lista[index_palabra] = (palabra, lista[index_plural][1] + conteo)
                    plurales_a_eliminar.append(plural)
                except StopIteration:
                    True

    # Eliminar los plurales de la lista
    lista_normalizada = [(palabra, conteo) for palabra, conteo in lista if palabra not in plurales_a_eliminar]
    
    return lista_normalizada

def normalize_list_spanish(lista):
    # Convertir la lista a un conjunto para buscar palabras de manera eficiente
    palabras_set = set(palabra for palabra, _ in lista)
    # Lista para almacenar los plurales que se eliminarán
    plurales_a_eliminar = []

    for palabra, conteo in lista:
        pluralize_word_list = pluralize_word_spanish(palabra)[1:]
        for plural in pluralize_word_list:
            if plural in palabras_set:
                # Si el plural está en la lista, encontrar su índice y sumar el conteo
                try:
                    index_plural = next(index for index, (word, _) in enumerate(lista) if word == plural)
                    index_palabra = next(index for index, (word, _) in enumerate(lista) if word == palabra)
                    lista[index_palabra] = (palabra, lista[index_plural][1] + conteo)
                    plurales_a_eliminar.append(plural)
                except StopIteration:
                    True

    # Eliminar los plurales de la lista
    lista_normalizada = [(palabra, conteo) for palabra, conteo in lista if palabra not in plurales_a_eliminar]
    
    return lista_normalizada

def pluralize_word_spanish(word):
    """Función para obtener la forma plural de una palabra (En el caso de que esta sea plural, devolverá su plural)
       En el caso de que la palabra sea compuesta, devolverá las permutaciones plurales de esa palabra en español
       
       Parámetros:
        - word (string)= Palabra a pluralizar (Puede ser simple o compuesta)
        
       Retorna:
        - pluralize_words_list (Array<string>)
                - Si la palabra es simple la lista contendrá solo un elemento
                - Si la palabra es compuesta la lista contendrá las permutaciones plurales de la palabra
                    () 
    """
    # Lista de sufijos comunes para la formación del plural en español
    suffixes = {
        'z': 'ces',
        'l': 'les',
        'r': 'res',
        'n': 'nes',
        'y': 'yes',
        'j': 'jes',
        'd': 'des',
        's': 'ses',
        'x': 'xes'
    }

    prepositions = ["a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "durante", "en", "entre", "hacia", "hasta", "mediante", "para", "por", "según", "sin", "so", "sobre", "tras"]

    words = word.split()

    # Función para pluralizar una palabra individual
    def pluralize(word):
        for suffix, plural in suffixes.items():
            if word.endswith(suffix):
                return word[:-1] + plural
        return word + 's'

    plural_permutations = []
    for word in words:
        if word in prepositions:
            plural_permutations.append([word])
        else:
            plural = pluralize(word)
            if plural != word:
                plural_permutations.append([word, plural])
            else:
                plural_permutations.append([word])

    composite_permutations = product(*plural_permutations)
    pluralize_words_list = []
    for permutation in composite_permutations:
        pluralize_words_list.append(" ".join(permutation))

    return pluralize_words_list

from itertools import product

def pluralize_word_english(word):
    """
    Función para obtener la forma plural de una palabra en inglés (En el caso de que esta sea plural, devolverá su plural).
    En el caso de que la palabra sea compuesta, devolverá las permutaciones plurales de esa palabra en inglés.
    
    Parámetros:
        - word (string): Palabra a pluralizar (Puede ser simple o compuesta)
        
    Retorna:
        - pluralize_words_list (Array<string>):
            - Si la palabra es simple la lista contendrá solo un elemento
            - Si la palabra es compuesta la lista contendrá las permutaciones plurales de la palabra
    """
    # Lista de preposiciones en inglés que no se pluralizan
    prepositions = ["of", "in", "to", "for", "with", "on", "at", "by", "about", "as", "into", "like", "through", "after", "over", "between", "out", "against", "during", "without", "before", "under", "around", "among"]

    # Diccionario de irregularidades en el plural
    irregulars = {
        "child": "children",
        "foot": "feet",
        "tooth": "teeth",
        "mouse": "mice",
        "person": "people",
        "man": "men",
        "woman": "women",
        "cactus": "cacti",
        "phenomenon": "phenomena",
        "analysis": "analyses",
        "thesis": "theses",
        "datum": "data",
        "leaf": "leaves",
        "life": "lives",
        "wife": "wives",
        "loaf": "loaves",
        "half": "halves",
        "knife": "knives",
        "city": "cities",
        "baby": "babies",
        "fish": "fish",
        "sheep": "sheep",
        "deer": "deer",
        "goose": "geese",
        "ox": "oxen",
        "bacterium": "bacteria",
        "criterion": "criteria",
        "series": "series",
        "species": "species",
    }

    words = word.split()

    # Función para pluralizar una palabra individual en inglés
    def pluralize(word):
        if word in irregulars:
            return irregulars[word]
        elif word.endswith('y') and word[-2] not in 'aeiou':
            return word[:-1] + 'ies'
        elif word.endswith(('s', 'sh', 'ch', 'x', 'z')):
            return word + 'es'
        elif word.endswith('f'):
            return word[:-1] + 'ves'
        elif word.endswith('fe'):
            return word[:-2] + 'ves'
        else:
            return word + 's'

    plural_permutations = []
    for word in words:
        if word in prepositions:
            plural_permutations.append([word])
        else:
            plural = pluralize(word)
            if plural != word:
                plural_permutations.append([word, plural])
            else:
                plural_permutations.append([word])

    composite_permutations = product(*plural_permutations)
    pluralize_words_list = []
    for permutation in composite_permutations:
        pluralize_words_list.append(" ".join(permutation))

    return pluralize_words_list

def extract_nouns_with_positions_english(sentence):
    """
    Extrae los sustantivos de una frase junto con sus posiciones, excluyendo los que son parte de compuestos.

    Args:
    sentence (str): La frase de la que se extraerán los sustantivos.

    Returns:
    List[Tuple[str, int, str, str]]: Una lista de tuplas que contiene el sustantivo, su posición,
                                     su dependencia y la palabra cabeza.
    """
    
    # Procesar la frase
    doc = nlp_en(sentence)
    
    # Extraer sustantivos que no sean parte de compuestos y agregar sus posiciones
    nouns_with_positions = [(token.text, token.i) for token in doc if token.pos_ == "NOUN" and token.dep_ != "compound"]
    
    return nouns_with_positions

def extract_nouns_with_positions_spanish(sentence):
    """
    Extrae los sustantivos de una frase junto con sus posiciones, excluyendo los que son parte de compuestos.

    Args:
    sentence (str): La frase de la que se extraerán los sustantivos.

    Returns:
    List[Tuple[str, int, str, str]]: Una lista de tuplas que contiene el sustantivo, su posición,
                                     su dependencia y la palabra cabeza.
    """
    
    # Procesar la frase
    doc = nlp_es(sentence)
    
    # Extraer sustantivos que no sean parte de compuestos y agregar sus posiciones
    nouns_with_positions = [(token.text, token.i) for token in doc if token.pos_ == "NOUN" and token.dep_ != "compound"]
    
    return nouns_with_positions

def destokenize(original_tokens, new_tokens):
    """Reconstruye una oración a partir de una lista de tokens, manejando contracciones y posesivos."""
    sentence = ''
    for i, token in enumerate(new_tokens):
        # Check if the current token is a possessive
        is_current_possessive = is_possessive(original_tokens, i)
        
        # Check for word-word junction (excluding punctuation and special cases)
        if re.match(r'\w', token) and re.match(r'\w', new_tokens[i - 1]) and token not in ['.', ',', '!', '?', ':', ';'] and new_tokens[i - 1] not in ['¿', '¡']:
            # Handle contractions (ends with "'s")
            if re.match(r'\w', token) and i <= len(new_tokens) - 3 and new_tokens[i + 1] == "'" and not new_tokens[i + 2] == "s":
                # If the current token is a possessive, don't add extra space
                if is_current_possessive:
                    sentence += ' ' + token
                else:
                    sentence += ' ' + token + ' '
            elif token == "'" and not (i <= len(new_tokens) - 2 and new_tokens[i + 1] == 's'): 
                sentence += token
            else:
                sentence += ' ' + token
        else:
            # Handle spaces after sentence-ending punctuations
            if token in [')',';',':',',','.', '!','¡','¿','?'] and i < len(new_tokens) - 1:
                sentence += token + ' '
            elif token == "(":
                sentence += ' ' + token
            else:
                if is_possessive(original_tokens, i-2):
                    sentence += ' ' + token
                else:
                    sentence += token
    return sentence.strip()  # Remove leading/trailing spaces

def is_possessive(tokens, index):
    """Determina si la palabra en el índice dado es un posesivo."""
    # Etiquetar las partes de la oración
    pos_tags = nltk.pos_tag(tokens)
    
    # Verificar si la palabra en el índice dado es un posesivo
    if index >= 0 and index < len(tokens) - 1:
        # Comprobar si la palabra siguiente es un apóstrofe
        if tokens[index + 1] == "'":
            # Comprobar si la palabra actual es un sustantivo propio (NNP) o plural (NNS)
            if pos_tags[index][1] in ["NNP", "NNS"]:
                return True
    
    return False