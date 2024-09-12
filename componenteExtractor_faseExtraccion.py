
import re
from unidecode import unidecode
import nltk
nltk.download('punkt')
from nltk.tokenize import RegexpTokenizer
from simalign import SentenceAligner
from collections import Counter
import sys
sys.path.append("./auxFunctionLibrary")
from pythonLib import auxFunctions


def get_result(element, llm_answer_list):
    
    """Función para pbtener el resultado de la fase de extracción. El conocimiento a obtener es la palabra correspondiente
        en castellano de una palabra en inglés

        Parámetros:
        - element = Elemento de la estructura de datos knowledge_table, compuesto por key + attributes
        - llm_extracted_answer (list) = 
                - El primer elemento corresponde con las frases originales
                - El segundo elemento es una lista de respuestas del LLM a las traducciones de las frases anteriores

        Retorna:
        - element (dict): Elemento de la estructura de datos 'knowledge_table', compuesto por key + attributes
            con los atributos modificados.  
    """
    
    # Lista de respuesta extraídas del LLM
    llm_extracted_answer_list_original = auxFunctions.extract_llm_answers_set_of_phrases(llm_answer_list[0])
    llm_extracted_answer_list_trads = []
    for llm_answer in llm_answer_list[1]:
        llm_extracted_answer_list_trads.append(auxFunctions.extract_llm_answers_translation(llm_answer))
        
    # Combinar las listas
    llm_extracted_answer = [list(par) for par in zip(llm_extracted_answer_list_original, llm_extracted_answer_list_trads)]
    
    # Crear el mensaje de información del estado de la entrada: 
    #   - Si es NULL, no se ha podido obtener un resultado a partir de la entrada
    #       message: "La entrada ha terminado su ejecución en la fase de extracción."
    #   - Si no es NULL, no se añade ningún mensaje
    message = "La entrada ha terminado su ejecución en la fase de extracción."
    # Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase
    count_incorrect_1 = 0
    # Incorrectas de tipo 2: la palabra a analizar no aparece en la frase
    count_incorrect_2 = 0
    # Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo
    count_incorrect_3 = 0
    # Lista de apariciones de word
    list_of_word_appearences = []
    # Respuesta provisional
    answer = ''
    # Obtener la palabra
    word = element[0].split('_')[1]
    # Obtener las formas plurales de la palabra
    plural_word = auxFunctions.pluralize_word_english(word)
    # Crear la lista donde vamos a ir guardando las palabras que simAlign relaciona con word
    relationships_list = []
    # Crear un tokenizador personalizado con una expresión regular
    tokenizer = RegexpTokenizer(r'\w+|[^\w\s]')
    # Crear una instancia del modelo
    myaligner = SentenceAligner(model="bert", token_type="bpe", matching_methods="mai")
    # Recorremos 'llm_extracted_answer' para comparar cada frase/traduccion y sacar las relaciones
    for phrase in llm_extracted_answer:
        # Si tenemos una lista en vez de frases las tratamos quedandonos con el primero elemento / frase de las listas
        if type(phrase[0]) is list:
            phrase[0] = phrase[0][0]
        if type(phrase[1]) is list:
            phrase[1] = phrase[1][0]
        # Obtenemos la frase original el inglés
        original_phrase = phrase[0].lower()
        # Obtenemos la traducción de la frase original proporcionada por el LLM
        translated_original_phrase = phrase[1].lower()
        # Encontrar la forma de word que aparece en las frases
        word_appearence = ""
        phrase_copy = str(phrase[0].lower())  # Crear una copia de element
        for item in plural_word:
            pattern = r'\b' + re.escape(unidecode(item)) + r'(?=[^\w]|$)'
            match = re.search(pattern, unidecode(phrase_copy))
            if match:
                word_appearence = phrase_copy[match.start():match.end()]
                list_of_word_appearences.append(word_appearence)
        if len(list_of_word_appearences) != 0:
            # Tokenizar la frase original
            tokens_original_phrase =  tokenizer.tokenize(original_phrase)
            # Tokenizar la frase original traducida
            tokens_translated_original_phrase =  tokenizer.tokenize(translated_original_phrase)
            # Obtener la posicion de la forma de word (noun) que aparece en las frases originales
            word_position = -1
            nouns_with_positions = auxFunctions.extract_nouns_with_positions_english(original_phrase)
            word_position_list = list(position for (noun, position) in nouns_with_positions if noun in list_of_word_appearences)
            if len(word_position_list) >= 1:
                word_position = word_position_list[0]
                # Busca apóstrofes en contracciones y posesivos
                new_phrase_tokens = tokens_original_phrase[:word_position+1]
                new_phrase = auxFunctions.destokenize(tokens_original_phrase, new_phrase_tokens)
                apostrophes = re.findall(r"\b\w+s'|\b\w+'s\b|'\w+'", new_phrase)
                if apostrophes:
                    word_position += len(apostrophes)
                # El resultado es un diccionario con diferentes métodos de comparación.
                # Cada método tiene una lista de pares que indican los índices de palabras alineadas (las alineaciones tienen un índice cero).
                alignments = myaligner.get_word_aligns(tokens_original_phrase, tokens_translated_original_phrase)
                # Obtener los resultados
                results = alignments['mwmf']
                # Crear la palabra que corresponde a la posicion de la forma de result que aparece en las frases traducidas
                translated_result_position = []
                # Obtener los resultados que nos interesan:
                for tuple in results:
                    if tuple[0] == word_position:
                        translated_result_position.append(tuple)
                if translated_result_position != []:
                    # Recorrer la lista
                    for pos in translated_result_position:
                        # Obtener la palabra que corresponde a la posicion de la forma de result que aparece en las frases traducidas
                        tranlated_relationed_result = tokens_translated_original_phrase[pos[1]]
                        nouns_with_positions_spanish = auxFunctions.extract_nouns_with_positions_spanish(translated_original_phrase)
                        # Añadirla a 'relationships_list'
                        if (tranlated_relationed_result, pos[1]) in nouns_with_positions_spanish:
                            relationships_list.append(tranlated_relationed_result)
                        else:
                            # Sumar Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo
                            count_incorrect_3 += 1
            else:
                # Sumar Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase en caso de que no haya nouns
                count_incorrect_1 += 1
        else:
            # Sumar Incorrectas de tipo 2: la palabra a analizar no aparece en la frase
            count_incorrect_2 += 1
        # Vaciar la lista
        list_of_word_appearences = []
    # Obtener el número de frases
    number_of_phrases = 5
    # Obtener el número de relaciones encontradas
    number_of_relationships = len(relationships_list)
    # Obtener la diferencia mínima entre las distintas palabras que aparecen en las relaciones
    minimum_number_of_difference = number_of_phrases*0.4
    # Obtener el resultado provisional
    if number_of_relationships >= 1:
        # Contar las apariciones usando Counter
        relationships_list = [element.lower() for element in relationships_list]
        word_count = Counter(relationships_list)
        # Convertir el resultado a una lista de tuplas de tipo ('palabra',Apariciones en word_count)
        word_count_tuples = list(word_count.items())
        # Normalizar la lista: Si existe un plural de una palabra, eliminar el plural sumandole una aparición a esa palabra
        normalized_words = auxFunctions.normalize_list_spanish(word_count_tuples)
        # Encontrar el elemento que tenga una diferencia importante en comparación con los demás
        found_element = auxFunctions.find_element_with_difference(normalized_words, minimum_number_of_difference)
        # Realizar comprobaciones del resultado provisional
        if found_element == []:
            answer = "NULL"
        else:
            answer = found_element[0]
    else:
        answer = "NULL"
    # Comprobar el tipo de resultado obtenido en la fase de extraccion
    if answer == "NULL":
        # Modificar el número de frases correctas
        element[1]["Correctas"] = len(relationships_list)
        # Modificar el número de frases incorrectas de tipo 1
        element[1]["Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase"] = count_incorrect_1
        # Modificar el número de frases incorrectas de tipo 2
        element[1]["Incorrectas de tipo 2: la palabra a analizar no aparece en la frase"] = count_incorrect_2
        # Modificar el número de frases incorrectas de tipo 3
        element[1]["Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo"] = count_incorrect_3
        # Modificar el mensaje de información de la fase en la que el proceso acaba
        element[1]["Mensaje de información"] = message
    # Modificar el resultado de la fase de extracción
    element[1]["Extraction translation"] = answer
    return (element[0], element[1])
            