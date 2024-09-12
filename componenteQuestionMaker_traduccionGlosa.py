

def generate_prompts(element):
    
    """
    Método para generar una lista de prompts para la traducción de la glosa inglés a castellano,
    basada en un elemento de 'knowledge_table'.
    
        Parámetros:
            - element (dict): Un elemento de 'knowledge_table'.
                    
        Retorna:
            - prompt_list (List[str]): Lista que contiene los prompts para la traducción de la glosa inglés a castellano.
    """
    
    gloss = element[1]["English gloss"]
    question = f"As a translation expert, I need an accurate translation into Spanish of the following phrase: '{gloss}'."
    prompt_list = [question]
    
    return prompt_list