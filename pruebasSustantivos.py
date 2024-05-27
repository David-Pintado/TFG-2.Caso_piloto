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

    plural_words = set()
    for word in words:
        if word in prepositions:
            plural_words.add(word)
        else:
            plural = pluralize(word)
            if plural != word:
                plural_words.add(plural)
            else:
                plural_words.add(word)

    return list(plural_words)

def normalizar(lista):
    # Convertir la lista a un conjunto para buscar palabras de manera eficiente
    palabras_set = set(palabra for palabra, _ in lista)
    # Lista para almacenar los plurales que se eliminarán
    plurales_a_eliminar = []

    for palabra, conteo in lista:
        pluralize_word_list = pluralize_word_spanish(palabra)
        for plural in pluralize_word_list:
            if plural in palabras_set:
                # Si el plural está en la lista, encontrar su índice y sumar el conteo
                index_palabra = next(index for index, (word, _) in enumerate(lista) if word == palabra)
                lista[index_palabra] = (palabra, lista[index_palabra][1] + conteo)
                plurales_a_eliminar.append(plural)

    # Eliminar los plurales de la lista
    lista_normalizada = [(palabra, conteo) for palabra, conteo in lista if palabra not in plurales_a_eliminar]
    
    return lista_normalizada

# Lista original
lista_original = [('objeto', 5)]

# Normalizar la lista
lista_normalizada = normalizar(lista_original)

print(lista_normalizada)
