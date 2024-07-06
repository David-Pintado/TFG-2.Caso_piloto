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
        en inglés de una palabra en castellano

        Parámetros:
        - element = Elemento de la estructura de datos knowledge_table, compuesto por key + attributes
        - llm_extracted_answer (list) = 
                - El primer elemento corresponde con las frases originales
                - El segundo elemento es una lista de respuestas del LLM a las traducciones de las frases anteriores

        Retorna:
        - extraction_result (string)
                - word: La palabra en inglés que corresponde al extraction_result 
                - "NULL": No se ha conseguido encontrar la palabra en español correspondiente a word
    """
    
    # Lista  de respuesta extraídas del LLM
    llm_extracted_answer_list_original = auxFunctions.extract_llm_answers_set_of_phrases(llm_answer_list[0])
    llm_extracted_answer_list_trads = []
    for llm_answer in llm_answer_list[1]:
        llm_extracted_answer_list_trads.append(auxFunctions.extract_llm_answers_translation(llm_answer))
        
    # Combinar las listas
    llm_extracted_answer = [list(par) for par in zip(llm_extracted_answer_list_original, llm_extracted_answer_list_trads)]
    
    # Crear la lista del contenido completo del result
    result = []
    # Crear el mensaje de información del estado de la entrada: 
    #   - Si es NULL, no se ha podido validar el resultado de la fase de extracción
    #       message: "La entrada ha terminado su ejecución en la fase de validación"
    #   - Si no es NULL, no se añade ningún mensaje
    message = "La entrada ha terminado su ejecución en la fase de validación."
    # Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.
    count_incorrect_1 = 0
    # Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.
    count_incorrect_2 = 0
    # Respuesta final
    answer = ''
    # Obtener el word
    word = element[0].split('_')[1]
    # Obtener el resultado de la fase de extracción
    extraction_result = element[1][6]
    # Lista de apariciones de extraction_result
    list_of_extraction_result_appearence = []
    # Obtener las formas plurales de result
    plural_extraction_result = auxFunctions.pluralize_word_spanish(extraction_result)
    # Crear la lista donde vamos a ir guardando las palabras que simAlign relaciona con extraction_result
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
        # Encontrar la forma de extraction_result que aparece en las frases
        extraction_result_appearence = ""
        phrase_copy = str(phrase[0].lower())  # Crear una copia de element
        for item in plural_extraction_result:
            pattern = r'\b' + re.escape(unidecode(item)) + r'(?=[^\w]|$)'
            match = re.search(pattern, unidecode(phrase_copy))
            if match:
                extraction_result_appearence = phrase_copy[match.start():match.end()]
                list_of_extraction_result_appearence.append(extraction_result_appearence)
        if len(list_of_extraction_result_appearence) != 0:
            # Obtenemos la frase origina el inglés
            original_phrase = phrase[0].lower()
            # Obtenemos la traducción de la frase original proporcionada por el LLM
            translated_original_phrase = phrase[1].lower()
            # Tokenizar la frase original
            tokens_original_phrase =  tokenizer.tokenize(original_phrase)
            # Tokenizar la frase original traducida
            tokens_translated_original_phrase =  tokenizer.tokenize(translated_original_phrase)
            # Obtener la posicion de la forma de extraction_result (noun) que aparece en las frases originales
            extraction_result_position = -1
            nouns_with_positions = auxFunctions.extract_nouns_with_positions_spanish(original_phrase)
            extraction_result_position_list = list(position for (noun, position) in nouns_with_positions if noun in list_of_extraction_result_appearence)
            if len(extraction_result_position_list) >= 1:
                extraction_result_position = extraction_result_position_list[0]
                # El resultado es un diccionario con diferentes métodos de comparación.
                # Cada método tiene una lista de pares que indican los índices de palabras alineadas (las alineaciones tienen un índice cero).
                alignments = myaligner.get_word_aligns(tokens_original_phrase, tokens_translated_original_phrase)
                # Obtener los resultados
                results = alignments['mwmf']
                # Crear la palabra que corresponde a la posicion de la forma de extraction_result que aparece en las frases traducidas
                translated_extraction_result_position = []
                # Obtener los resultados que nos interesan:
                for tuple in results:
                    if tuple[0] == extraction_result_position:
                        translated_extraction_result_position.append(tuple)
                if translated_extraction_result_position != []:
                    # Recorrer la lista
                    for pos in translated_extraction_result_position:
                        # Busca apóstrofes en contracciones y posesivos
                        position = pos[1]
                        other_position = pos[1]
                        new_phrase_tokens = tokens_translated_original_phrase[:position+1]
                        new_phrase = auxFunctions.destokenize(tokens_translated_original_phrase, new_phrase_tokens)
                        apostrophes = re.findall(r"\b\w+s'|\b\w+'s\b|'\w+'", new_phrase)
                        if apostrophes:
                            other_position += len(apostrophes)
                        # Obtener la palabra que corresponde a la posicion de la forma de extraction_result que aparece en las frases traducidas
                        tranlated_relationed_extraction_result = tokens_translated_original_phrase[position]
                        nouns_with_positions_english = auxFunctions.extract_nouns_with_positions_english(translated_original_phrase)
                        print(nouns_with_positions_english)
                        # Añadirla a 'relationships_list'
                        if (tranlated_relationed_extraction_result, position) in nouns_with_positions_english:
                            relationships_list.append(tranlated_relationed_extraction_result)
                        # Añadir el otro:
                        if position != other_position:
                            # Obtener la palabra que corresponde a la posicion de la forma de extraction_result que aparece en las frases traducidas
                            new_tranlated_relationed_extraction_result = tokens_translated_original_phrase[other_position]
                            # Añadirla a 'relationships_list'
                            if (new_tranlated_relationed_extraction_result, other_position) in nouns_with_positions_english:
                                relationships_list.append(new_tranlated_relationed_extraction_result)
            else:
                # Sumar Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase. en caso de que no haya nouns
                count_incorrect_1 += 1
        else:
            # Sumar Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.
            count_incorrect_2 += 1
        # Vaciar la lista
        list_of_extraction_result_appearence = []
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
        extraction_result_count = Counter(relationships_list)
        # Convertir el resultado a una lista de tuplas de tipo ('palabra',Apariciones en extraction_result_count)
        extraction_result_count_tuples = list(extraction_result_count.items())
        # Normalizar la lista: Si existe un plural de una palabra, eliminar el plural sumandole una aparición a esa palabra
        normalized_extraction_results = auxFunctions.normalize_list_english(extraction_result_count_tuples)
        # Encontrar el elemento que tenga una diferencia importante en comparación con los demás
        found_element = auxFunctions.validation_find_element_with_difference(normalized_extraction_results, auxFunctions.pluralize_word_english(word), minimum_number_of_difference)
        # Realizar comprobaciones del resultado provisional
        if found_element == []:
            answer = "NULL"
        else:
            answer = found_element[0]
            if answer == word:
                answer = extraction_result
            elif answer in auxFunctions.pluralize_word_english(word)[1:]:
                answer = extraction_result
            else:
                answer = "NULL"
    else:
        answer = "NULL"
    # Devolver las respuesta provisional
    if answer == "NULL":
        # Crea el primer elemento como un diccionario
        correct_message = {
            "Correctas.": len(relationships_list)
        }
        # Crea el segundo elemento como un diccionario
        incorrect_message_1 = {
            "Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.": count_incorrect_1
        }
        # Crea el tercer elemento como un diccionario
        incorrect_message_2 = {
            "Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.": count_incorrect_2
        }
        # Crea el cuarto elemento como un diccionario
        information_message = {
            "Mensaje de información" : message
        }
        result = [answer, correct_message, incorrect_message_1, incorrect_message_2, information_message]
    else:
        result = [answer]
    return result
