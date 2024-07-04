

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
    
    """
    Método para encontrar un 'Value' en una lista de tuplas de tipo [Value, num], donde 'num' ha de superar o igualar la 
    diferencia, y donde 'num' deberá tener el valor más alto en la lista. En caso de haber un empate tiene prioridad
    el elemento cuyo 'Value' se encuentre en 'plural_list'. Si no se encuentra ninguno, se elige uno al azar.

        Parámetros:
            - lst (List[Tuple[Any, int]]): Lista de tuplas donde cada tupla contiene un elemento y un valor entero.
            - difference (int): Diferencia mínima requerida para el segundo valor de las tuplas.

        Retorna:
            - element (Tuple[Any, int]): Un elemento de 'lst' que cumple con los requisitos.
    """
    
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
    
    """
    Método para encontrar un 'Value' en una lista de tuplas de tipo [Value, num], donde 'num' ha de superar o igualar la 
    diferencia, y donde 'num' deberá tener el valor más alto en la lista. En caso de haber un empate se elige uno al azar.

        Parámetros:
            - lst (List[Tuple[Any, int]]): Lista de tuplas donde cada tupla contiene un elemento y un valor entero.
            - difference (int): Diferencia mínima requerida para el segundo valor de las tuplas.

        Retorna:
            - element (Tuple[Any, int]): Un elemento de 'lst' que cumple con los requisitos.
    """
    
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
    
    """
    Método para normalizar una lista de palabras en inglés, combinando el número de apariciones de las palabras
    y sus formas plurales.

        Parámetros:
            - lista (List[Tuple[str, int]]): Lista de tuplas donde cada tupla contiene una palabra en inglés
                                            y su número de apariciones correspondiente.
        Retorna:
            - lista_normalizada (List[Tuple[str, int]]): Lista de tuplas donde los número de apariciones de las palabras y
                                                        sus formas plurales se han combinado.
    """
    
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
    
    """
    Método para normalizar una lista de palabras en castellano, combinando el número de apariciones de las palabras
    y sus formas plurales.

        Parámetros:
            - lista (List[Tuple[str, int]]): Lista de tuplas donde cada tupla contiene una palabra en castellano
                                            y su número de apariciones correspondiente.
        Retorna:
            - lista_normalizada (List[Tuple[str, int]]): Lista de tuplas donde los número de apariciones de las palabras y
                                                        sus formas plurales se han combinado.
    """
    
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

    """
    Método para obtener la forma plural de una palabra en castellano. Si word es una palabra compuesta,
    devuelve las permutaciones plurales de esa palabra.
    
        Parámetros:
            - word (str): Palabra en castellano a pluralizar
        Retorna:
            - pluralize_words_list (List[str]): Lista de plurales de la palabra. Incluye la forma singular
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
    Método para obtener la forma plural de una palabra en inglés. Si word es una palabra compuesta,
    devuelve las permutaciones plurales de esa palabra.
    
        Parámetros:
            - word (str): Palabra en inglés a pluralizar
        Retorna:
            - pluralize_words_list (List[str]): Lista de plurales de la palabra. Incluye la forma singular
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
    Método que extrae los sustantivos de una frase en inglés junto con sus posiciones.
    
        Parámetros:
            - sentence (str): Oración en inglés sobre la que extraer los sustantivos
        Retorna:
            - nouns_with_positions (List[Tuple[str, int]]): Lista de tuplas que contienen el sustantivo junto a su posición 
                                                            en la frase 'sentence' tokenizada
    """
    
    # Procesar la frase
    doc = nlp_en(sentence)
    
    # Extraer sustantivos que no sean parte de compuestos y agregar sus posiciones
    nouns_with_positions = [(token.text, token.i) for token in doc if token.pos_ == "NOUN" and token.dep_ != "compound"]
    
    return nouns_with_positions

def extract_nouns_with_positions_spanish(sentence):

    """
    Método que extrae los sustantivos de una frase en castellano junto con sus posiciones.
    
        Parámetros:
            - sentence (str): Oración en castellano sobre la que extraer los sustantivos
        Retorna:
            - nouns_with_positions (List[Tuple[str, int]]): Lista de tuplas que contienen el sustantivo junto a su posición 
                                                            en la frase 'sentence' tokenizada
    """
    
    # Procesar la frase
    doc = nlp_es(sentence)
    
    # Extraer sustantivos que no sean parte de compuestos y agregar sus posiciones
    nouns_with_positions = [(token.text, token.i) for token in doc if token.pos_ == "NOUN" and token.dep_ != "compound"]
    
    return nouns_with_positions

def destokenize(original_tokens, new_tokens):

    """
    Método que reconstruye una oración a partir de una lista de tokens, manejando contracciones y posesivos.
    
        Parámetros:
            - original_tokens (List[str]): Lista de tokens de la oración completa. Necesaria para saber información sobre cada token
            - new_tokens (List[str]): Sublista de tokens de original_tokens.
        Retorna:
            - sentence (str): Oración resultante de la correcta unión de los tokens    
    """
    
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

    """
    Método para determinar si una palabra correspondiente al índice de una lista de tokens es un posesivo.
    
        Parámetros:
            - tokens (List[str]): Lista de tokens
            - index (number): Índice
        Retorna:
            - Valor booleano (True/False)
            
    """
    
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

def extract_llm_answers_set_of_phrases(llm_answer):
    
    """
    Método para extraer la respuesta del LLM.
    
        Parámetros:
            - llm_answer (str): Respuesta del LLM sin tratar. Contiene separadores de oraciones 
        Retorna:
            - llm_extracted_answer (List[str]): Respuesta del LLM extraída. Se forma una lista con las frases.
            
    """

    # Eliminar los saltos de línea
    llm_extracted_answer = llm_answer.replace('\n', ' ').replace('\n\n', ' ').strip()
    # Comprobar si tiene separadores de frases.
    if re.split(r'\d+\)|\d+\.', llm_extracted_answer)[1:] != [] and len(re.split(r'\d+\)|\d+\.', llm_extracted_answer)) >= 5: 
        # Dividir el texto en frases utilizando cualquier secuencia de un número seguido de un punto o paréntesis como criterio de separación
        llm_extracted_answer = re.split(r'\d+\)|\d+\.', llm_extracted_answer)[1:]
        # Quitar los espacios blancos del principio y final de las frases y asegurarse de que cada frase termine con un punto
        llm_extracted_answer = [answer.strip() + '.' if not answer.strip().endswith('.') else answer.strip() for answer in llm_extracted_answer]
        # Quitar las comillas y barras de las frases
        llm_extracted_answer = [answer.replace('"', '').replace("'", "").replace('\\', '') for answer in llm_extracted_answer]
        # Si empieza por '-' eliminarlo
        llm_extracted_answer = [answer[1:].strip() if answer.startswith('-') else answer for answer in llm_extracted_answer]
        return llm_extracted_answer
    # Comprobar si tiene más de una frase separada por un punto seguido de un espacio
    elif len(llm_extracted_answer.split('. ')) >= 5:
        # Dividir el texto en frases utilizando el punto seguido de un espacio como criterio de separación
        llm_extracted_answer = [phrase for phrase in llm_extracted_answer.split('. ')]
        # Quitar los espacios blancos del principio y final de las frases y asegurarse de que cada frase termine con un punto
        llm_extracted_answer = [answer.strip() + '.' if not answer.strip().endswith('.') else answer.strip() for answer in llm_extracted_answer]
        # Quitar las comillas y barras de las frases
        llm_extracted_answer = [answer.replace('"', '').replace("'", "").replace('\\', '') for answer in llm_extracted_answer]
        # Si empieza por '-' eliminarlo
        llm_extracted_answer = [answer[1:].strip() if answer.startswith('-') else answer for answer in llm_extracted_answer]
        return llm_extracted_answer
    # Comprobar si tiene más de una frase separada por un punto y coma seguido de un espacio
    elif len(llm_extracted_answer.split('; ')) >= 5:
        # Dividir el texto en frases utilizando el punto y coma seguido de un espacio como criterio de separación
        llm_extracted_answer = [phrase for phrase in llm_extracted_answer.split('; ')]
        # Quitar los espacios blancos del principio y final de las frases y asegurarse de que cada frase termine con un punto
        llm_extracted_answer = [answer.strip() + '.' if not answer.strip().endswith('.') else answer.strip() for answer in llm_extracted_answer]
        # Quitar las comillas y barras de las frases
        llm_extracted_answer = [answer.replace('"', '').replace("'", "").replace('\\', '') for answer in llm_extracted_answer]
        # Si empieza por '-' eliminarlo
        llm_extracted_answer = [answer[1:].strip() if answer.startswith('-') else answer for answer in llm_extracted_answer]
        return llm_extracted_answer
    # Comprobar si tiene más de una frase separada por un punto y coma seguido de un espacio
    elif len(llm_extracted_answer.split(', ')) >= 5:
        # Dividir el texto en frases utilizando el punto y coma seguido de un espacio como criterio de separación
        llm_extracted_answer = [phrase for phrase in llm_extracted_answer.split(', ')]
        # Quitar los espacios blancos del principio y final de las frases y asegurarse de que cada frase termine con un punto
        llm_extracted_answer = [answer.strip() + '.' if not answer.strip().endswith('.') else answer.strip() for answer in llm_extracted_answer]
        # Quitar las comillas y barras de las frases
        llm_extracted_answer = [answer.replace('"', '').replace("'", "").replace('\\', '') for answer in llm_extracted_answer]
        # Si empieza por '-' eliminarlo
        llm_extracted_answer = [answer[1:].strip() if answer.startswith('-') else answer for answer in llm_extracted_answer]
        return llm_extracted_answer
    # Si no cumple ninguna de las condiciones anteriores, devolver la respuesta sin tratar
    return llm_extracted_answer

def save_json(file_path, json):
    
    """
    Método para guardar datos JSON en un archivo en la ruta proporcionada.

        Parámetros:
            - file_path (str): Ruta completa donde se guarda el archivo JSON.
            - json_data (str): Datos JSON que se escriben en el archivo.

        Retorna:
            - None
    """
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json)