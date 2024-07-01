


def generate_prompts(element):
    
    """
    Método para generar una lista de prompts para la traducción de frases en inglés a castellano,
    basada en un elemento de 'knowledge_table'.
    
        Parámetros:
            - element (dict): Un elemento de 'knowledge_table'.
                    
        Retorna:
            - prompt_list (List[str]): Lista que contiene los prompts para la traducción de frases en inglés a castellano.
    """
    
    prompt_list = []
    offset_word = element[0]
    word = offset_word.split('_')[1]
    gloss = element[1][1]
    phrases = element[1][4][1]
    for phrase in phrases: 
        question = f"As an English to Spanish translation expert, I need an accurate translation into Spanish of the English sentence '{phrase}', where the noun '{word}' appears in the sense of '{gloss}'."
        prompt_list.append(question)
    return prompt_list


