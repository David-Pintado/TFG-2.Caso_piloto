
import re
from unidecode import unidecode
from itertools import product
import nltk
nltk.download('punkt')
from nltk.tokenize import RegexpTokenizer
from simalign import SentenceAligner
from collections import Counter


def extract_llm_answers(llm_answer):

    # Extraer el texto devuelto
    return_answer_value = llm_answer['choices'][0]['text']
    # Dividirlo en dos partes (la parte de la pregunta, la parte de la respuesta)
    llm_extracted_answer = return_answer_value.split('Answer:')[1]
    # Eliminar los saltos de linea
    llm_extracted_answer = llm_extracted_answer.replace('\n',' ').replace('\n\n',' ').strip()
    # Comprabar si tiene separadores de frases. Si no tiene es que es una traduccion
    if(re.split(r'\d+\)|\d+\.', llm_extracted_answer)[1:] != []):    
        # Dividir el texto en frases utilizando cualquier secuencia de un número seguido de un punto como criterio de separación
        llm_extracted_answer = re.split(r'\d+\)|\d+\.', llm_extracted_answer)[1:]
        # Quitar los espacios blancos del principio y final de las frases 
        llm_extracted_answer = [answer.strip() for answer in llm_extracted_answer]
        # Quitar las comillas y barras de las frases
        llm_extracted_answer = [answer.replace('"', '').replace("\"", "").replace('\\', '').replace("\\\"", "") for answer in llm_extracted_answer]

    return llm_extracted_answer


# def get_provisional_answer4(element, llm_extracted_answer_list):
    
#     """Función para la respuesta provisional al conocimiento a obtener en base a una palabra y una lista de frases
#        con la palabra en varios géneros
    
#        Parámetros:
#         - element = Elemento de la estructura de datos source_information, compuesto por key + attributes
#         - llm_extracted_answer_list (list) = Lista que se compone de dos listas de misma longud
#                         - La primera contiene frases con la palabra en género maculino
#                         - La segunda contiene frases con la palabra en género femenino
#        Retorna:
#         - provisional_answer (string)
#                 - "Masculino": La palabra es de género masculino
#                 - "Femenino": La palabra es de género femenino
#                 - "NULL": No se ha conseguido encontrar el género de la palabra
#     """
    
#     # Inicializamos las variables necesarias
#     count_male = 0
#     count_female = 0
#     word = element[0].split('_')[1]
#     plural_word = auxFunctions.pluralize_word(word)
#     male_word_appearence = ""
#     female_word_appearence = ""
#     provisional_answer = ""
#     max_difference = len(llm_extracted_answer_list[0])-round((len(llm_extracted_answer_list[0])*2)/3) + 1
#     list_minimum_appearences = len(llm_extracted_answer_list[0]) * 0.8
#     array_female = ['la', 'las', 'una', 'unas','esa', 'esta', 'esas', 'estas', 'otra', 'otras']
#     array_male = ['el', 'del', 'los', 'un', 'unos', 'al', 'ese', 'este', 'esos', 'estos', 'otro', 'otros']
    
#     # Si una lista tiene más frases en un género que en otro, se acorta la lista a la cantidad mínima de frases
#     minimun_number_of_sentences = min(len(llm_extracted_answer_list[0]), len(llm_extracted_answer_list[1]))
#     maximun_number_of_sentences = max(len(llm_extracted_answer_list[0]), len(llm_extracted_answer_list[1]))
#     llm_extracted_answer_list[0] = llm_extracted_answer_list[0][:minimun_number_of_sentences]
#     llm_extracted_answer_list[1] = llm_extracted_answer_list[1][:minimun_number_of_sentences]
    
#     # Contamos las apariciones de las palabras y articulos para saber su genero
#     for element in llm_extracted_answer_list[0]:
#         male_word_appearence = ""
#         element_copy = str(element)  # Crear una copia de element
#         for item in plural_word:
#             pattern = r'\b' + re.escape(unidecode(item)) + r'(?=[^\w]|$)'
#             match = re.search(pattern, unidecode(element_copy))
#             if match:
#                 male_word_appearence = element_copy[match.start():match.end()]
#                 break
#         if male_word_appearence != "":
#             male_word_appearence = " " + male_word_appearence + " "
#             search_article_phrase = element.split(male_word_appearence)[0].strip().split(' ')
#             if len(search_article_phrase) == 1:
#                 if search_article_phrase[-1].lower() in array_male:  # Comparar en minúsculas para hacerlo insensible a mayúsculas/minúsculas
#                     count_male += 1
#                 elif search_article_phrase[-1].lower() in array_female:
#                     count_male += -1
#             elif len(search_article_phrase) > 1:
#                 reversed_search_article_phrase = search_article_phrase[::-1][:2]
#                 if reversed_search_article_phrase[0].lower() in array_male:
#                     count_male += 1
#                 elif reversed_search_article_phrase[1].lower() in array_male:
#                     count_male += 0.5
#                 elif reversed_search_article_phrase[0].lower() in array_female:
#                     count_male += -1
#                 elif reversed_search_article_phrase[1].lower() in array_female:
#                     count_male += -0.5
#     for element in llm_extracted_answer_list[1]:
#         female_word_appearence = ""
#         element_copy = str(element)  # Crear una copia de element
#         for item in plural_word:
#             pattern = r'\b' + re.escape(unidecode(item)) + r'(?=[^\w]|$)'
#             match = re.search(pattern, unidecode(element_copy))
#             if match:
#                 female_word_appearence = element_copy[match.start():match.end()]
#                 break
#         if female_word_appearence != "":
#             female_word_appearence = " " + female_word_appearence + " "
#             search_article_phrase = element.split(female_word_appearence)[0].strip().split(' ')
#             if len(search_article_phrase) == 1:
#                 if search_article_phrase[-1].lower() in array_male:  # Comparar en minúsculas para hacerlo insensible a mayúsculas/minúsculas
#                     count_female += -1
#                 elif search_article_phrase[-1].lower() in array_female:
#                     count_female += 1
#             elif len(search_article_phrase) > 1:
#                 reversed_search_article_phrase = search_article_phrase[::-1][:2]
#                 if reversed_search_article_phrase[0].lower() in array_male:
#                     count_female += -1
#                 elif reversed_search_article_phrase[1].lower() in array_male:
#                     count_female += -0.5
#                 elif reversed_search_article_phrase[0].lower() in array_female:
#                     count_female += 1
#                 elif reversed_search_article_phrase[1].lower() in array_female:
#                     count_female += 0.5

#     # print(' ')
#     # print('Puntos masculinos: ')
#     # print(count_male) 
#     # print(' ')
#     # print('Puntos femeninos')
#     # print(count_female)
#     # print(' ')
#     # print('Umbral para categoría (Femenino o masculino han de superar el umbral para obtener la respuesta): ')
#     # print(list_minimum_appearences)
#     # print('Umbra general (La diferencia entre las categorías tiene que superar este umbral para obtener un género): ')
#     # print(max_difference)
    
#     if len(llm_extracted_answer_list[0]) > 0 and len(llm_extracted_answer_list[0]) >= maximun_number_of_sentences/2:
#         # Calculamos la diferencia maxima que pueden tener los distintos generos en base a la longitud de la lamina de pruebas 
#         if count_male >=  list_minimum_appearences and 0 <= max_difference < abs(count_male-count_female) and count_male > count_female:
#             provisional_answer = "Masculino"
#         elif count_female >=  list_minimum_appearences and 0 <= max_difference < abs(count_male-count_female) and count_female > count_male:
#             provisional_answer = "Femenino"
#         else: 
#             provisional_answer = "NULL"
#     else:
#         provisional_answer = "NULL"
#     return provisional_answer

def get_provisional_answer(element, llm_extracted_answer_list):
    # Respuesta provisional
    provisional_answer = ''
    # Obtener la palabra
    word = element[0].split('_')[1]
    # Obtener las formas plurales de la palabra
    plural_word = pluralize_word_english(word)
    # Crear la lista donde vamos a ir guardando las palabras que simAlign relaciona con word
    relationships_list = []
    # Crear un tokenizador personalizado con una expresión regular
    tokenizer = RegexpTokenizer(r'\w+|[^\w\s]')
    # making an instance of our model.
    # You can specify the embedding model and all alignment settings in the constructor.
    myaligner = SentenceAligner(model="bert", token_type="bpe", matching_methods="mai")
    # Recorremos 'llm_extracted_answer_list' para comparar cada frase/traduccion y sacar las relaciones
    for phrase in llm_extracted_answer_list:
        # Encontrar la forma de word que aparece en las frases
        word_appearence = ""
        phrase_copy = str(phrase)  # Crear una copia de element
        for item in plural_word:
            pattern = r'\b' + re.escape(unidecode(item)) + r'(?=[^\w]|$)'
            match = re.search(pattern, unidecode(phrase_copy))
            if match:
                word_appearence = phrase_copy[match.start():match.end()]
                break
        if word_appearence != "":
            # Obtenemos la frase origina el inglés
            original_phrase = phrase[0]
            # Obtenemos la traducción de la frase original proporcionada por el LLM
            translated_original_phrase = phrase[1]
            # Tokenizar la frase original
            tokens_original_phrase =  tokenizer.tokenize(original_phrase)
            # Tokenizar la frase original traducida 
            tokens_translated_original_phrase =  tokenizer.tokenize(translated_original_phrase)
            # Obtener la posicion de la forma de word que aparece en las frases originales
            word_position = find_first_index(tokens_original_phrase, lambda x: x ==  word_appearence)
            # The output is a dictionary with different matching methods.
            # Each method has a list of pairs indicating the indexes of aligned words (The alignments are zero-indexed).
            alignments = myaligner.get_word_aligns(tokens_original_phrase, tokens_translated_original_phrase)
            # Obtener los resultados
            results = alignments['mwmf']
            # Crear la palabra que corresponde a la posicion de la forma de word que aparece en las frases traducidas
            translated_word_position = ""
            # Obtener los resultados que nos interesan:
            for tuple in results:
                if tuple[0] == word_position:
                    translated_word_position = tuple
                    break
                else:
                    # Manejar el caso donde no se encontró el valor x en ninguna tupla
                    translated_word_position = None
            if translated_word_position != None:
                # Obtener la palabra que corresponde a la posicion de la forma de word que aparece en las frases traducidas
                tranlated_relationed_word = tokens_translated_original_phrase[tuple[1]]
                # Añadirla a 'relationships_list'
                relationships_list.append(tranlated_relationed_word)
    # Obtener el número de frases
    number_of_phrases = len(llm_extracted_answer_list)
    # Obtener el número de relaciones encontradas
    number_of_relationships = len(relationships_list)
    # Obtener el mínimo número de relaciones para devolver la respuesta provisional
    minimum_number_of_relations = number_of_phrases*0.8
    # Obtener la diferencia mínima entre las distintas palabras que aparecen en las relaciones
    minimum_number_of_difference = number_of_phrases*0.4
    # Obtener la respuesta provisional
    if number_of_relationships >= minimum_number_of_relations:
        # Contar las apariciones usando Counter
        word_count = Counter(relationships_list)
        # Convertir el resultado a una lista de tuplas de tipo ('palabra',Apariciones en word_count)
        word_count_tuples = list(word_count.items())
        # Normalizar la lista: Si existe un plural de una palabra, eliminar el plural sumandole una aparición a esa palabra
        normalized_words = normalizar(word_count_tuples)
        # Encontrar el elemento que tenga una diferencia importante en comparación con los demás
        found_element = find_element_with_difference(normalized_words, minimum_number_of_difference)
        # Realizar comprobaciones de la respuesta provisional
        if found_element == []:
            provisional_answer = "NULL"
        else:
            provisional_answer = found_element[0]
    else:
        provisional_answer = "NULL"
    # Devolver las respuesta provisional
    return provisional_answer


# TODO
# Encontrar la manera de conjugar las palabras --> No hace falta
# Cambiar los prompt a los del caso piloto 1
            
    
def find_first_index(lst, condition):
    for index, element in enumerate(lst):
        if condition(element):
            return index
    return -1 

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


def find_element_with_difference(list, difference):
    # Ordenar la lista de forma descendente según el segundo elemento de las tuplas
    sorted_list = sorted(list, key=lambda x: x[1], reverse=True)

    # Tomar el primer elemento como referencia para la comparación
    reference = sorted_list[0]

    # Verificar si la diferencia es mayor o igual a la diferencia especificada con respecto a los demás elementos
    for element in sorted_list[1:]:
        if reference[1] - element[1] < difference:
            return []
    return reference