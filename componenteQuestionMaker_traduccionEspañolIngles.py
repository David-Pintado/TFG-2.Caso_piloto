

def generate_prompts(element):
    
    """
    Método para generar una lista de prompts para la traducción de frases en castellano a inglés,
    basada en un elemento de 'knowledge_table'.
    
        Parámetros:
            - element (dict): Un elemento de 'knowledge_table'.
                    
        Retorna:
            - prompt_list (List[str]): Lista que contiene los prompts para la traducción de frases en castellano a inglés.
    """

    prompt_list = []
    word = element[1]["Extraction translation"]
    gloss = element[1]["Spanish gloss"]
    phrases = element[1]["Validation LLM answers"][1]
    for phrase in phrases: 
        question = f"As an Spanish to English translation expert, I need an accurate translation into English of the Spanish sentence '{phrase}', where the noun '{word}' appears in the sense of '{gloss}'."
        prompt_list.append(question)
    return prompt_list