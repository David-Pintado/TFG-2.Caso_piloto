

def generate_prompts(element):
    
    """
    Método para generar una lista de prompts para la fase de validación basada en un elemento de 'knowledge_table'.
    
        Parámetros:
            - element (dict): Un elemento de 'knowledge_table'.
                    
        Retorna:
            - prompt_list (List[str]): Lista que contiene los prompts para la fase de validación.
    """
    
    gloss = element[1][2]
    result = element[1][6]
    question = f"Como experto en lingüística, proporciona cinco frases en las que el sustantivo '{result}' aparezca en el sentido de '{gloss}'."
    prompt_list = [question]
    
    return prompt_list

# ------------------- Otras versiones antiguas --------------------- #

# question = "Como experto en lingüística, por favor, proporciona cinco frases que contengan la palabra '" + result + "', con el significado de '" + gloss + "'."
# question = f"Como experto en lingüística, proporciona cinco frases donde la palabra '{result}' aparezca solo como sustantivo, con el sentido de '{gloss}'. No utilices formas verbales ni otras variaciones de la palabra."

