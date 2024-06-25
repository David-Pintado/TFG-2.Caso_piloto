

def generate_prompts(element):
    
    offset_word = element[0]
    word = offset_word.split('_')[1]
    gloss = element[1][1]
    # question = "As a linguistics expert, please provide five sentences containing the word '" + word + "', with the meaning of '" + gloss + "'."
    # question = f"As a linguistics expert, provide five sentences where the word '{word}' appears only as a noun, in the sense of '{gloss}'. Do not use verb forms or other variations of the word."
    question = f"As a linguistics expert, provide five sentences where the noun '{word}' appears in the sense of '{gloss}'."
    prompt_list = [question]
    
    return prompt_list