
import sys
sys.path.append("./auxFunctionLibrary")
from pythonLib import auxFunctions


def get_result(element, llm_answer_list):
    
    """Método para extraer y tratar la traducción de una frase.
    
       Parámetros:
        - element (dict): Elemento de la estructura de datos knowledge_table, compuesto por key + attributes.
        - llm_answer_list (list): Lista que se de una traducción que necesita ser extraída.
       Retorna:
        - result (str): Traducción extraída y tratada.
    """
    
    result = auxFunctions.extract_llm_answers_translation(llm_answer_list[0])

    return result