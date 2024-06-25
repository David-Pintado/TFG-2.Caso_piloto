
from itertools import product

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

    words = word.split()

    # Función para pluralizar una palabra individual en inglés
    def pluralize(word):
        if word.endswith('y') and word[-2] not in 'aeiou':
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


examples = [
    "cat",
    "city",
    "brush",
    "leaf",
    "dog and cat",
    "book on table",
    "knife",
    "baby and toy"
]

ejemplos = [
    "gato",
    "ciudad",
    "cepillo",
    "hoja",
    "perro y gato",
    "libro sobre la mesa",
    "cuchillo",
    "bebé y juguete"
]

print('ESPAÑOL')
for example in ejemplos:
    print(f"{example}: {pluralize_word_spanish(example)}")
    
print('----------------')
    
print('INGLÉS')
for example in examples:
    print(f"{example}: {pluralize_word_english(example)}")