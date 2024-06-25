


def generate_prompts(element):

    offset_word = element[0]
    word = offset_word.split('_')[1]
    gloss = element[1][1]
    question = f"As an English to Spanish translation expert, I need an accurate translation into Spanish of the English sentence '{phrase}', where the noun '{word}' appears in the sense '{gloss}'.'"
    prompt_list = [question]
    
    return prompt_list