


def generate_provisional_prompts(element):
    
    offset_word = element[0]
    word = offset_word.split('_')[1]
    gloss = element[1][1]
    # question = "As a linguistics expert, please provide five sentences containing the word '" + word + "', with the meaning of '" + gloss + "'."
    # question = f"As a linguistics expert, provide five sentences where the word '{word}' appears only as a noun, in the sense of '{gloss}'. Do not use verb forms or other variations of the word."
    question = f"As a linguistics expert, provide five sentences where the noun '{word}' appears in the sense of '{gloss}'."
    prompt_list = [question]
    
    return prompt_list

def generate_validation_prompts(element, provisional_result):
    
    gloss = element[1][2]
    # question = "Como experto en lingüística, por favor, proporciona cinco frases que contengan la palabra '" + provisional_result + "', con el significado de '" + gloss + "'."
    # question = f"Como experto en lingüística, proporciona cinco frases donde la palabra '{provisional_result}' aparezca solo como sustantivo, con el sentido de '{gloss}'. No utilices formas verbales ni otras variaciones de la palabra."
    question = f"Como experto en lingüística, proporciona cinco frases en las que el sustantivo '{provisional_result}' aparezca en el sentido de '{gloss}'."
    prompt_list = [question]
    
    return prompt_list


# Segundo caso piloto
    # f"As a linguistics expert, provide five sentences where the noun '{word}' appears in the sense of '{gloss}'."
# Para traducir frases: 
    # As an English to Spanish translation expert, I need an accurate translation into English of the Spanish sentence "' + phrase +'" where the noun 'word' appears in the sense 'gloss'.'
    # Modificar la siguiente: 'As a translation expert, I need an accurate translation into English of the following phrase: "' + phrase +'".'
# Primer caso piloto
# Como experto en lingüística, proporciona cinco frases utilizando el sustantivo 'humano' en género masculino con el sentido de 'Un ser humano'.
 