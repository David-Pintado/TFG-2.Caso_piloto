from nltk import pos_tag
import re

def is_possessive(tokens, index):
    """Determina si la palabra en el índice dado es un posesivo."""
    # Etiquetar las partes de la oración
    pos_tags = pos_tag(tokens)
    
    # Verificar si la palabra en el índice dado es un posesivo
    if index >= 0 and index < len(tokens) - 1:
        # Comprobar si la palabra siguiente es un apóstrofe
        if tokens[index + 1] == "'":
            # Comprobar si la palabra actual es un sustantivo propio (NNP) o plural (NNS)
            if pos_tags[index][1] in ["NNP", "NNS"]:
                return True
    
    return False

def destokenize(original_tokens, new_tokens):
    """Reconstruye una oración a partir de una lista de tokens, manejando contracciones y posesivos."""
    sentence = ''
    for i, token in enumerate(new_tokens):
        # Check if the current token is a possessive
        is_current_possessive = is_possessive(original_tokens, i)
        
        # Check for word-word junction (excluding punctuation and special cases)
        if re.match(r'\w', token) and re.match(r'\w', new_tokens[i - 1]) and token not in ['.', ',', '!', '?', ':', ';'] and new_tokens[i - 1] not in ['¿', '¡']:
            # Handle contractions (ends with "'s")
            if re.match(r'\w', token) and i <= len(new_tokens) - 3 and new_tokens[i + 1] == "'" and not new_tokens[i + 2] == "s":
                # If the current token is a possessive, don't add extra space
                if is_current_possessive:
                    sentence += ' ' + token
                else:
                    sentence += ' ' + token + ' '
            elif token == "'" and not (i <= len(new_tokens) - 2 and new_tokens[i + 1] == 's'): 
                sentence += token
            else:
                sentence += ' ' + token
        else:
            # Handle spaces after sentence-ending punctuations
            if token in ['.', '!', '?'] and i < len(new_tokens) - 1:
                sentence += token + ' '
            else:
                if is_possessive(original_tokens, i-2):
                    sentence += ' ' + token
                else:
                    sentence += token
    return sentence.strip()  # Remove leading/trailing spaces

# Ejemplo de uso:
frase_original = "the workers' protest against inhumane. They call him 'Act'. They're strong."
tokens1 = ['the', 'workers', "'", 'protest', 'against', 'inhumane',".", "They", "call", "him", "'", "Act", "'", ".", "They", "'", "re", "strong","."]
new_tokens = ['the', 'workers', "'"]
# print(destokenize(tokens1, new_tokens))  # Salida: the workers' protest against inhumane. They call him 'Act'. They're strong.

import re

texto = "the workers' protest against inhumane. They call him 'Act'. They're strong."
ap = re.findall(r"\b\w+s'|\b\w+'s\b|'\w+'", texto)
print(ap)
