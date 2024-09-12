
import sys
sys.path.append("./auxFunctionLibrary")
from pythonLib import auxFunctions


def get_result(element, llm_answer_list):
    
    """Método para extraer y tratar un conjunto de frases en un único string.
    
       Parámetros:
        - element (dict): Elemento de la estructura de datos knowledge_table, compuesto por key + attributes.
        - llm_answer_list (List[str]): Lista que se compone de un único string devuelto por el LLM que necesita ser extraído.
       Retorna:
        - element (dict): Elemento de la estructura de datos 'knowledge_table', compuesto por key + attributes
            con los atributos modificados.    
    """
    print('------------------------------')
    print(element)
    print('\n\n')
    print(llm_answer_list)
    if (element[1]["Extraction translation"] == "NULL"):
        element[1]["Extraction LLM answers"].append(auxFunctions.extract_llm_answers_set_of_phrases(llm_answer_list[0]))
    elif (element[1]["Extraction translation"] != "NULL"):
        element[1]["Validation LLM answers"].append(auxFunctions.extract_llm_answers_set_of_phrases(llm_answer_list[0]))
    return element