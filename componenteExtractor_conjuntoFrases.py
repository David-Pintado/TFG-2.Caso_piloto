
import sys
sys.path.append("./auxFunctionLibrary")
from pythonLib import auxFunctions


def get_result(element, llm_answer_list):
    
    """Método para extraer y tratar un conjunto de frases en un único string.
    
       Parámetros:
        - element (dict): Elemento de la estructura de datos knowledge_table, compuesto por key + attributes.
        - llm_answer_list (List[str]): Lista que se compone de un único string devuelto por el LLM que necesita ser extraído.
       Retorna:
        - result (List[str]): Lista de frases extraídas de llm_answer_list
    """
    
    result = auxFunctions.extract_llm_answers_set_of_phrases(llm_answer_list[0])

    return result