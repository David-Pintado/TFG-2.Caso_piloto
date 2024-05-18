


def generate_provisional_prompts(element):
    
    offset_word = element[0]
    word = offset_word.split('_')[1]
    gloss = element[1][1]
    question = "As a linguistics expert, please provide five sentences containing the word '" + word + "', with the meaning of '" + gloss + "'."
    prompt_list = [question]
    
    return prompt_list

def generate_validation_prompts(element, provisional_answer):
    
    offset_word = element[0]
    word = offset_word.split('_')[1]
    gloss = element[1][1]
    question = "Como experto en lingüística, por favor, proporciona cinco frases donde la palabra '" + word + "' se utilice en género " + provisional_answer + " en todo momento, con el sentido de '" + gloss + "'. Cada frase debe contener la palabra '" + word + "' en género " + provisional_answer + ", asegurándote de mantener este género en todas las instancias dentro de la frase."
    prompt_list = [question]
    
    return prompt_list