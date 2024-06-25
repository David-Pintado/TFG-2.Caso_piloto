
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


def extract_llm_answers(llm_answer):

    # Extraer el texto devuelto
    return_answer_value = llm_answer['choices'][0]['text']
    # Dividirlo en dos partes (la parte de la pregunta, la parte de la respuesta)
    llm_extracted_answer = return_answer_value.split('Answer:')[1]
    # Eliminar los saltos de linea
    llm_extracted_answer = llm_extracted_answer.replace('\n',' ').replace('\n\n',' ').strip()
    # Comprabar si tiene separadores de frases. Si no tiene es que es una traduccion
    if(re.split(r'\d+\)|\d+\.', llm_extracted_answer)[1:] != [] and (len(re.split(r'\d+\)|\d+\.', llm_extracted_answer)) >= 4)):    
        # Dividir el texto en frases utilizando cualquier secuencia de un número seguido de un punto como criterio de separación
        llm_extracted_answer = re.split(r'\d+\)|\d+\.', llm_extracted_answer)[1:]
        # Quitar los espacios blancos del principio y final de las frases 
        llm_extracted_answer = [answer.strip() + '.' if not answer.strip().endswith('.') else answer.strip() for answer in llm_extracted_answer]
        # Quitar las comillas y barras de las frases
        llm_extracted_answer = [answer.replace('"', '').replace("\"", "").replace('\\', '').replace("\\\"", "") for answer in llm_extracted_answer]
        return llm_extracted_answer
    # Comprobar si tiene más de una frase. En ese caso puede que no tenga separadores pero que sean un conjunto de frases
    elif(len(llm_extracted_answer.split('. ')) >= 4):
        # Compilar la expresión regular directamente sin escapar
        llm_extracted_answer = [phrase for phrase in llm_extracted_answer.split('. ')]
        # Quitar los espacios blancos del principio y final de las frases 
        llm_extracted_answer = [answer.strip() + '.' if not answer.strip().endswith('.') else answer.strip() for answer in llm_extracted_answer]
        # Quitar las comillas y barras de las frases
        llm_extracted_answer = [answer.replace('"', '').replace("\"", "").replace('\\', '').replace("\\\"", "") for answer in llm_extracted_answer]
        return llm_extracted_answer
    # Comprobar si tiene más de una frase (; ). En ese caso puede que no tenga separadores pero que sean un conjunto de frases
    elif(len(llm_extracted_answer.split('; ')) >= 4):
        # Compilar la expresión regular directamente sin escapar
        llm_extracted_answer = [phrase for phrase in llm_extracted_answer.split('; ')]
        # Quitar los espacios blancos del principio y final de las frases 
        llm_extracted_answer = [answer.strip() + '.' if not answer.strip().endswith('.') else answer.strip() for answer in llm_extracted_answer]
        # Quitar las comillas y barras de las frases
        llm_extracted_answer = [answer.replace('"', '').replace("\"", "").replace('\\', '').replace("\\\"", "") for answer in llm_extracted_answer]
        return llm_extracted_answer
    # Si es una traducción tratarla
    if type(llm_extracted_answer) is list:
        if len(llm_extracted_answer) > 0:
            llm_extracted_answer = llm_extracted_answer[0]
        elif len(llm_extracted_answer) == 0:
            llm_extracted_answer = ""
    llm_extracted_answer = llm_extracted_answer.split(". ")[0].strip()
    llm_extracted_answer = llm_extracted_answer.strip().replace('"', '').replace("\"", "").replace('\\', '').replace("\\\"", "").capitalize()
    if not llm_extracted_answer.endswith('.'):
        llm_extracted_answer += '.'
    return llm_extracted_answer

def get_provisional_result(element, llm_extracted_answer):
    
    """Función para el resultado provisional al conocimiento a obtener en base a una palabra y una lista de frases en inglés
        con la palabra en el gloss, y sus respectivas traducciones

        Parámetros:
        - element = Elemento de la estructura de datos knowledge_table, compuesto por key + attributes
        - llm_extracted_answer (list) = Lista que se compone de listas de misma longud
                        - El primer de cada elemento de list es una frase en inglés
                        - El segundo de cada elemento de list es una frase en español, la traducción de la anterior

        Retorna:
        - provisional_result (Lista)
                - word: La palabra en español que corresponde al word de element 
                - "NULL" (Y más información para analizar): No se ha conseguido encontrar la palabra en español correspondiente a word
    """
    # Crear la lista del contenido completo del provisional_result
    provisional_result = []
    # Crear el mensaje de información del estado de la entrada: 
    #   - Si es NULL, no se ha podido obtner un resultado a partir de la entrada, y la ejecución queda en provisional
    #       message: "La entrada ha terminado su ejecución en la extracción del resultado provisional"
    #   - Si no es NULL, no se añade ningún mensaje
    message = "La entrada ha terminado su ejecución en la extracción del resultado provisional."
    # Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.
    count_incorrect_1 = 0
    # Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.
    count_incorrect_2 = 0
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
                # The output is a dictionary with different matching methods.
                # Each method has a list of pairs indicating the indexes of aligned words (The alignments are zero-indexed).
                alignments = myaligner.get_word_aligns(tokens_original_phrase, tokens_translated_original_phrase)
                # Obtener los resultados
                results = alignments['mwmf']
                # Crear la palabra que corresponde a la posicion de la forma de provisional_result que aparece en las frases traducidas
                translated_provisional_result_position = []
                # Obtener los resultados que nos interesan:
                for tuple in results:
                    if tuple[0] == word_position:
                        translated_provisional_result_position.append(tuple)
                if translated_provisional_result_position != []:
                    # Recorrer la lista
                    for pos in translated_provisional_result_position:
                        # Obtener la palabra que corresponde a la posicion de la forma de provisional_result que aparece en las frases traducidas
                        tranlated_relationed_provisional_result = tokens_translated_original_phrase[pos[1]]
                        nouns_with_positions_spanish = auxFunctions.extract_nouns_with_positions_spanish(translated_original_phrase)
                        # Añadirla a 'relationships_list'
                        if (tranlated_relationed_provisional_result, pos[1]) in nouns_with_positions_spanish:
                            relationships_list.append(tranlated_relationed_provisional_result)
            else:
                # Sumar Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase. en caso de que no haya nouns
                count_incorrect_1 += 1
        else:
            # Sumamos a Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.
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
    # Devolver el contenido completo del resultado provisional
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
        provisional_result = [answer, correct_message, incorrect_message_1, incorrect_message_2, information_message]
    else:
        provisional_result = [answer]
    return provisional_result
            