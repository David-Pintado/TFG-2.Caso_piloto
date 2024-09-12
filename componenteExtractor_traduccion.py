
import sys
sys.path.append("./auxFunctionLibrary")
from pythonLib import auxFunctions


def get_result(element, llm_answer_list):
    
    """Método para extraer y tratar la traducción de una frase.
    
       Parámetros:
        - element (dict): Elemento de la estructura de datos knowledge_table, compuesto por key + attributes.
        - llm_answer_list (list): Lista que se de una traducción que necesita ser extraída.
       Retorna:
        - element (dict): Elemento de la estructura de datos 'knowledge_table', compuesto por key + attributes
            con los atributos modificados.  
    """
    print('--------------                ----------------')
    print(element)
    print('\n\n')
    print(llm_answer_list)
    element[1]["Spanish gloss"] = auxFunctions.extract_llm_answers_translation(llm_answer_list[0])

    return element