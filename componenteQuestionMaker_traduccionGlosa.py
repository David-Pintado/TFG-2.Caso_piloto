

def generate_prompts(element):
    
    gloss = element[1][1]
    question = f"As a translation expert, I need an accurate translation into Spanish of the following phrase: '{gloss}'."
    prompt_list = [question]
    
    return prompt_list