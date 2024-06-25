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




def get_final_result(element, llm_extracted_answer, provisional_result):
    
    """Función para la respuesta final al conocimiento a obtener en base a una palabra y una lista de frases en español
        con la palabra en el gloss, y sus respectivas traducciones al inglés

        Parámetros:
        - element = Elemento de la estructura de datos knowledge_table, compuesto por key + attributes
        - llm_extracted_answer (list) = Lista que se compone de listas de misma longud
                        - El primer de cada elemento de list es una frase en español
                        - El segundo de cada elemento de list es una frase en inglés, la traducción de la anterior

        Retorna:
        - provisional_result (string)
                - word: La palabra en inglés que corresponde al provisional_result 
                - "NULL": No se ha conseguido encontrar la palabra en español correspondiente a word
    """
    # Crear la lista del contenido completo del final_result
    final_result = []
    # Crear el mensaje de información del estado de la entrada: 
    #   - Si es NULL, no se ha podido obtner un resultado a partir de la entrada, y la ejecución queda en provisional
    #       message: "La entrada ha terminado su ejecución en la extracción del resultado provisional"
    #   - Si no es NULL, no se añade ningún mensaje
    message = "La entrada ha terminado su ejecución en la validación del resultado provisional."
    # Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.
    count_incorrect_1 = 0
    # Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.
    count_incorrect_2 = 0
    # Respuesta final
    answer = ''
    # Obtener el word
    word = element[0].split('_')[1]
    # Lista de apariciones de provisional_result
    list_of_provisional_result_appearence = []
    # Obtener las formas plurales de final_result
    plural_provisional_result = auxFunctions.pluralize_word_spanish(provisional_result)
    # Crear la lista donde vamos a ir guardando las palabras que simAlign relaciona con provisional_result
    relationships_list = []
    # Crear un tokenizador personalizado con una expresión regular
    tokenizer = RegexpTokenizer(r'\w+|[^\w\s]')
    # making an instance of our model.
    # You can specify the embedding model and all alignment settings in the constructor.
    myaligner = SentenceAligner(model="bert", token_type="bpe", matching_methods="mai")
    # Recorremos 'llm_extracted_answer' para comparar cada frase/traduccion y sacar las relaciones
    for phrase in llm_extracted_answer:
        # Si tenemos una lista en vez de frases las tratamos quedandonos con el primero elemento / frase de las listas
        if type(phrase[0]) is list:
            phrase[0] = phrase[0][0]
        if type(phrase[1]) is list:
            phrase[1] = phrase[1][0]
        # Encontrar la forma de provisional_result que aparece en las frases
        provisional_result_appearence = ""
        phrase_copy = str(phrase[0].lower())  # Crear una copia de element
        for item in plural_provisional_result:
            pattern = r'\b' + re.escape(unidecode(item)) + r'(?=[^\w]|$)'
            match = re.search(pattern, unidecode(phrase_copy))
            if match:
                provisional_result_appearence = phrase_copy[match.start():match.end()]
                list_of_provisional_result_appearence.append(provisional_result_appearence)
        if len(list_of_provisional_result_appearence) != 0:
            # Obtenemos la frase origina el inglés
            original_phrase = phrase[0].lower()
            # Obtenemos la traducción de la frase original proporcionada por el LLM
            translated_original_phrase = phrase[1].lower()
            # Tokenizar la frase original
            tokens_original_phrase =  tokenizer.tokenize(original_phrase)
            # Tokenizar la frase original traducida
            tokens_translated_original_phrase =  tokenizer.tokenize(translated_original_phrase)
            # Obtener la posicion de la forma de provisional_result (noun) que aparece en las frases originales
            provisional_result_position = -1
            nouns_with_positions = auxFunctions.extract_nouns_with_positions_spanish(original_phrase)
            provisional_result_position_list = list(position for (noun, position) in nouns_with_positions if noun in list_of_provisional_result_appearence)
            if len(provisional_result_position_list) >= 1:
                provisional_result_position = provisional_result_position_list[0]
                # The output is a dictionary with different matching methods.
                # Each method has a list of pairs indicating the indexes of aligned words (The alignments are zero-indexed).
                alignments = myaligner.get_word_aligns(tokens_original_phrase, tokens_translated_original_phrase)
                # Obtener los resultados
                results = alignments['mwmf']
                # Crear la palabra que corresponde a la posicion de la forma de provisional_result que aparece en las frases traducidas
                translated_provisional_result_position = []
                # Obtener los resultados que nos interesan:
                for tuple in results:
                    if tuple[0] == provisional_result_position:
                        translated_provisional_result_position.append(tuple)
                if translated_provisional_result_position != []:
                    # Recorrer la lista
                    for pos in translated_provisional_result_position:
                        # Busca apóstrofes en contracciones y posesivos
                        position = pos[1]
                        other_position = pos[1]
                        new_phrase_tokens = tokens_translated_original_phrase[:position+1]
                        new_phrase = auxFunctions.destokenize(tokens_translated_original_phrase, new_phrase_tokens)
                        apostrophes = re.findall(r"\b\w+s'|\b\w+'s\b|'\w+'", new_phrase)
                        if apostrophes:
                            other_position += len(apostrophes)
                        # Obtener la palabra que corresponde a la posicion de la forma de provisional_result que aparece en las frases traducidas
                        tranlated_relationed_provisional_result = tokens_translated_original_phrase[position]
                        nouns_with_positions_english = auxFunctions.extract_nouns_with_positions_english(translated_original_phrase)
                        print(nouns_with_positions_english)
                        # Añadirla a 'relationships_list'
                        if (tranlated_relationed_provisional_result, position) in nouns_with_positions_english:
                            relationships_list.append(tranlated_relationed_provisional_result)
                        # Añadir el otro:
                        if position != other_position:
                            # Obtener la palabra que corresponde a la posicion de la forma de provisional_result que aparece en las frases traducidas
                            new_tranlated_relationed_provisional_result = tokens_translated_original_phrase[other_position]
                            # Añadirla a 'relationships_list'
                            if (new_tranlated_relationed_provisional_result, other_position) in nouns_with_positions_english:
                                relationships_list.append(new_tranlated_relationed_provisional_result)
            else:
                # Sumar Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase. en caso de que no haya nouns
                count_incorrect_1 += 1
        else:
            # Sumamos a Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.
            count_incorrect_2 += 1
        # Vaciar la lista
        list_of_provisional_result_appearence = []
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
        provisional_result_count = Counter(relationships_list)
        # Convertir el resultado a una lista de tuplas de tipo ('palabra',Apariciones en provisional_result_count)
        provisional_result_count_tuples = list(provisional_result_count.items())
        # Normalizar la lista: Si existe un plural de una palabra, eliminar el plural sumandole una aparición a esa palabra
        normalized_provisional_results = auxFunctions.normalize_list_english(provisional_result_count_tuples)
        # Encontrar el elemento que tenga una diferencia importante en comparación con los demás
        found_element = auxFunctions.validation_find_element_with_difference(normalized_provisional_results, auxFunctions.pluralize_word_english(word), minimum_number_of_difference)
        # Realizar comprobaciones del resultado provisional
        if found_element == []:
            answer = "NULL"
        else:
            answer = found_element[0]
            if answer == word:
                answer = provisional_result
            elif answer in auxFunctions.pluralize_word_english(word)[1:]:
                answer = provisional_result
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
        final_result = [answer, correct_message, incorrect_message_1, incorrect_message_2, information_message]
    else:
        final_result = [answer]
    return final_result
