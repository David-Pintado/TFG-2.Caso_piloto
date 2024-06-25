import componenteExtractor
import componenteValidator
import random
import spacy
import sys
sys.path.append("./auxFunctionLibrary") #Agrega la carpeta superior al sys.path
from pythonLib import auxFunctions
# Cargar el modelo de lenguaje en español
nlp_es = spacy.load("es_core_news_sm")

# Cargar el modelo de lenguaje en inglés
nlp_en = spacy.load("en_core_web_sm")

a = (
  "eng-30-14974264-n_paper", [
    "1",
    "A material made of cellulose pulp derived mainly from wood or rags or certain grasses.",
    "Un material hecho de pulpa de celulosa derivada principalmente del madera o los paños o ciertas hierbas..",
    "n",
    "eng",
    [
      [
        "The paper is a versatile material that has been used for centuries to write on, print on, and package goods.",
        "El papel es un material muy versátil que ha estado en uso durante siglos para escribir, imprimir y empaquetar productos."
      ],
      [
        "It is made by breaking down wood or other fibrous materials into small pieces, which are then mixed with water and formed into sheets.",
        "Se hace rompiendo la madera o otros materiales fibrosos en pequeños trozos, que se mezclan con agua y se forman en hojas."
      ],
      [
        "The resulting product can be used in a variety of ways, from printing newspapers and books to creating decorative items like origami and scrapbook pages.",
        "El producto resultante puede ser utilizado de muchas maneras, desde la impresión de periódicos y libros hasta la creación de elementos decorativos como el origami y las páginas de álbumes."
      ],
      [
        "In the modern world, paper has become an essential part of daily life, from receipts and invoices to packaging materials for products we buy.",
        "En el mundo moderno, el papel ha convertido en una parte esencial de la vida diaria, desde los recibos y las facturas hasta los materiales para empaquetar productos que compramos."
      ],
      [
        "It is also an important tool for education, as textbooks, notebooks, and other learning materials are often made from paper.",
        "También es una herramienta importante para la educación, ya que los libros de texto, cuadernos y otros materiales de aprendizaje se hacen a menudo con papel."
      ],
      [
        "However, with growing concerns about environmental sustainability, there is a push towards more eco-friendly alternatives to traditional paper production methods.",
        "Sin embargo, con la creciente preocupación por la sostenibilidad ambiental, hay una tendencia hacia alternativas más ecológicas a los métodos de producción tradicionales de papel."
      ]
    ],
    "papel",
    [
      [
        "El papel es un material muy común en nuestras vidas diarias, desde la impresión hasta la escritura y el empaquetado.",
        "The paper is a very common material in our daily lives, from printing to writing and packaging."
      ],
      [
        "La industria del papel ha estado creciendo rápidamente en los últimos años debido a la demanda mundial de este producto.",
        "The paper industry has been growing rapidly in recent years due to the global demand for this product."
      ],
      [
        "El papel reciclado es una opción ecológica para reducir la contaminación y preservar los recursos naturales.",
        "Recycled paper is an ecological option for reducing pollution and preserving natural resources."
      ],
      [
        "La calidad del papel es crucial en la producción de libros, revistas y otros materiales impresos.",
        "The quality of paper is critical in the production of books, magazines, and other printed materials."
      ],
      [
        "Los carteles publicitarios son un ejemplo claro de cómo el papel puede ser utilizado para comunicar mensajes importantes a una audiencia amplia.",
        "The billboards are a clear example of how paper can be used to communicate important messages to a wide audience."
      ]
    ],
    "papel"
  ]
)

b =       [
      [
        "The paper is a versatile material that has been used for centuries to write on, print on, and package goods.",
        "El papel es un material muy versátil que ha estado en uso durante siglos para escribir, imprimir y empaquetar productos."
      ],
      [
        "It is made by breaking down wood or other fibrous materials into small pieces, which are then mixed with water and formed into sheets.",
        "Se hace rompiendo la madera o otros materiales fibrosos en pequeños trozos, que se mezclan con agua y se forman en hojas."
      ],
      [
        "The resulting product can be used in a variety of ways, from printing newspapers and books to creating decorative items like origami and scrapbook pages.",
        "El producto resultante puede ser utilizado de muchas maneras, desde la impresión de periódicos y libros hasta la creación de elementos decorativos como el origami y las páginas de álbumes."
      ],
      [
        "In the modern world, paper has become an essential part of daily life, from receipts and invoices to packaging materials for products we buy.",
        "En el mundo moderno, el papel ha convertido en una parte esencial de la vida diaria, desde los recibos y las facturas hasta los materiales para empaquetar productos que compramos."
      ],
      [
        "It is also an important tool for education, as textbooks, notebooks, and other learning materials are often made from paper.",
        "También es una herramienta importante para la educación, ya que los libros de texto, cuadernos y otros materiales de aprendizaje se hacen a menudo con papel."
      ],
      [
        "However, with growing concerns about environmental sustainability, there is a push towards more eco-friendly alternatives to traditional paper production methods.",
        "Sin embargo, con la creciente preocupación por la sostenibilidad ambiental, hay una tendencia hacia alternativas más ecológicas a los métodos de producción tradicionales de papel."
      ]
    ]
 
d =     [
      [
        "El papel es un material muy común en nuestras vidas diarias, desde la impresión hasta la escritura y el empaquetado.",
        "The paper is a very common material in our daily lives, from printing to writing and packaging."
      ],
      [
        "La industria del papel ha estado creciendo rápidamente en los últimos años debido a la demanda mundial de este producto.",
        "The paper industry has been growing rapidly in recent years due to the global demand for this product."
      ],
      [
        "El papel reciclado es una opción ecológica para reducir la contaminación y preservar los recursos naturales.",
        "Recycled paper is an ecological option for reducing pollution and preserving natural resources."
      ],
      [
        "La calidad del papel es crucial en la producción de libros, revistas y otros materiales impresos.",
        "The quality of paper is critical in the production of books, magazines, and other printed materials."
      ],
      [
        "Los carteles publicitarios son un ejemplo claro de cómo el papel puede ser utilizado para comunicar mensajes importantes a una audiencia amplia.",
        "The billboards are a clear example of how paper can be used to communicate important messages to a wide audience."
      ]
    ]

# Obtener la respuesta final
print(componenteValidator.get_final_result(a, d, "papel"))

# print(componenteExtractor.get_provisional_result(a,b))

# print(auxFunctions.pluralize_word_english('home'))
# print(auxFunctions.pluralize_word_english('house'))
# print(auxFunctions.pluralize_word_english('agriculture')) 

# ['home', 'homes']
# ['house', 'houses']
# ['agriculture', 'agricultures']

 
# print(auxFunctions.validation_find_element_with_difference([('agriculture', 5)],['agriculture', 'agricultures'],1))
# print(auxFunctions.validation_find_element_with_difference([('agriculture', 5)],['agriculture', 'agricultures'],5))
# print(auxFunctions.validation_find_element_with_difference([('agriculture', 5)],['agriculture', 'agricultures'],6))
# print(auxFunctions.validation_find_element_with_difference([('home', 2), ('house', 2)],['home', 'homes'],2))
# print(auxFunctions.validation_find_element_with_difference([('home', 2), ('house', 2)],['house', 'houses'],2))
# print(auxFunctions.validation_find_element_with_difference([('home', 2), ('house', 2)],['house', 'houses'],3))





def extract_nouns_with_positions_spanish(sentence):
    """
    Extrae los sustantivos de una frase junto con sus posiciones, excluyendo los que son parte de compuestos.

    Args:
    sentence (str): La frase de la que se extraerán los sustantivos.

    Returns:
    List[Tuple[str, int, str, str]]: Una lista de tuplas que contiene el sustantivo, su posición,
                                     su dependencia y la palabra cabeza.
    """
    
    # Procesar la frase
    doc = nlp_es(sentence)
    
    # Extraer sustantivos, sus posiciones, etiquetas POS, dependencias sintácticas y cabezas
    nouns_with_positions = [(token.text, token.i, token.pos_, token.dep_, token.head.text) for token in doc]
        
    return nouns_with_positions

# print(extract_nouns_with_positions_spanish("El jugador utilizó trucos para ganar la partida."))


c = {
  "id": "cmpl-5f9f618d-6410-41f1-8b4a-763ed16291bf",
  "object": "text_completion",
  "created": 1717236003,
  "model": "../models/zephyr-7b-alpha.Q4_K_M.gguf",
  "choices": [
    {
      "text": "Question: As a linguistics expert, provide five sentences where the noun 'rejection' appears in the sense of 'The act of rejecting something.'. Answer: The hiring committee rejected the candidate's application due to lack of experience.\n\nThe editor rejected the author's manuscript because it did not meet the publisher's standards.\n\nThe customer rejected the product, claiming that it was defective and did not work properly.\n\nThe jury rejected the defendant's plea of insanity and found him guilty of murder.\n\nThe school board rejected the teacher's request for a salary increase, citing budget constraints.",
      "index": 0,
      "logprobs": "null",
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 36,
    "completion_tokens": 100,
    "total_tokens": 136
  }
}

# print(componenteExtractor.extract_llm_answers(c))

# TODO: Da error al haber una lista. En el .lower() de la traducción
# [
#   ['El uso de lenguaje es un patrón automático de comportamiento en respuesta a la necesidad de comunicarse.', 'The use of language is an automatic pattern of behavior in response to the need to communicate.'],
#   ['El uso de drogas recreativas puede ser hereditario o adquirido a través de la repetición frecuente.', 'The use of recreational drugs can be hereditary or acquired through frequent repetition.'],
#   ['El uso de tecnología ha cambiado drásticamente en los últimos años.', 'The use of technology has undergone a dramatic change over the past few years.'],
#   ['El uso de armas de fuego es una preocupación importante para muchos ciudadanos.', ['The use of firearms is a significant concern for many citizens, particularly in light of recent incidents involving mass shootings and other violent crimes', 'This issue has become a major focus of public debate and policy discussions at the local, state, and national levels', 'While some argue that gun ownership is a fundamental right protected by the Second Amendment to the U.S', 'Constitution, others contend that stricter regulation and control measures are necessary to prevent further tragedies and promote public safety', 'Ultimately, this ongoing controversy highlights the complex and often contentious relationship between individual liberties and collective responsibilities in a democratic society.']],
#   ['El uso de recursos naturales está siendo cuestionado debido a la falta de sostenibilidad.', 'The use of natural resources is being questioned due to the lack of sustainability.']
#   ]


d = {
  "id": "cmpl-d1c34734-27c6-46d6-9cf5-3796fc1f09a8",
  "object": "text_completion",
  "created": 1717606096,
  "model": "../models/zephyr-7b-alpha.Q4_K_M.gguf",
  "choices": [
    {
      "text": "Question: As a linguistics expert, provide five sentences where the noun 'year' appears in the sense of 'A period of time containing 365 (or 366) days.'. Answer: The year 2021 has been marked by the COVID-19 pandemic, which has affected every aspect of our lives. In this year alone, over four million people have lost their lives to the virus.\n\nThe year 2020 was a challenging one for many, with lockdowns and restrictions imposed in response to the pandemic. However, it was also a year of innovation and adaptation, as people found new ways to work, learn, and connect from home.\n\nThe year 1963 saw the signing of the Civil Rights Act, which marked a significant turning point in the struggle for equality in the United States. This legislation helped to pave the way for future civil rights legislation and has had a lasting impact on American society.\n\nThe year 1850 was a pivotal one in the history of the United States, as it saw the passage of the Compromise of 1850. This legislation helped to",
      "index": 0,
      "logprobs": "null",
      "finish_reason": "length"
    }
  ],
  "usage": {
    "prompt_tokens": 46,
    "completion_tokens": 200,
    "total_tokens": 246
  }
}

# print(componenteExtractor.extract_llm_answers(d))

def find_element_with_difference(lst, difference):
    if not lst:
        return []

    # Filtrar los elementos que tienen el segundo valor mayor o igual a la diferencia
    filtered_list = [element for element in lst if element[1] >= difference]

    if not filtered_list:
        return []

    # Encontrar el máximo valor del segundo elemento en la lista filtrada
    max_value = max(filtered_list, key=lambda x: x[1])[1]

    # Obtener todos los elementos con el valor máximo
    max_elements = [element for element in filtered_list if element[1] == max_value]

    # Elegir uno al azar en caso de empate
    return random.choice(max_elements)

# Listas de prueba
a = [('contacto', 2), ('comunicaciones', 2), ('relaciones', 1)]
b = [('captura', 2), ('jaque', 1), ('torre', 1), (',', 1)]
c = [('contacto', 2)]
d = []
e = [('captura', 1), ('jaque', 1), ('torre', 1), (',', 1)]

# Pruebas
# print(find_element_with_difference(a, 2))  # Output esperado: ('contacto', 2) o ('comunicaciones', 2) de forma aleatoria
# print(find_element_with_difference(b, 2))  # Output esperado: ('captura', 2)
# print(find_element_with_difference(c, 2))  # Output esperado: ('contacto', 2)
# print(find_element_with_difference(d, 2))  # Output esperado: []
# print(find_element_with_difference(e, 2))  # Output esperado: uno de los elementos con valor 1 aleatoriamente

import re

def destokenize(tokens):
    """Reconstruye una oración a partir de una lista de tokens, manejando contracciones y posesivos."""
    sentence = ''
    for i, token in enumerate(tokens):
        # Check for word-word junction (excluding punctuation and special cases)
        if re.match(r'\w', token) and re.match(r'\w', tokens[i - 1]) and token not in ['.', ',', '!', '?', ':', ';'] and tokens[i - 1] not in ['¿', '¡']:
            # Handle contractions (ends with "'s")
            if re.match(r'\w', token) and i <= len(tokens) - 2 and tokens[i + 1] == "'" and not tokens[i + 2] == "s":
                sentence += ' ' + token + ' '
            elif token == "'" and not (i <= len(tokens) - 1 and tokens[i + 1] == 's'): 
                sentence += token
            else:      
                sentence += ' ' + token
        else:
            # Handle spaces after sentence-ending punctuations
            if token in ['.', '!', '?'] and i < len(tokens) - 1:
                sentence += token + ' '
            else:
                sentence += token
    return sentence.strip()  # Remove leading/trailing spaces
  

# Test the function with the given tokens
tokens = ['the', 'sports', 'team', "'", 's', 'were', 'great', '.', 'He', 'used', 'to', 'call', 'her', "'", 'supeeer', "'", '.']
# sentence = destokenize(tokens)
# print(sentence)

element = ("eng-30-00039297-n_protest", [
            "1",
            "Close interaction.",
            "Interacción cercana.",
            "n",
            "eng",
            [
            [
                "The sales team had frequent contacts with potential clients to close deals.",
                "La plantilla debe ser una traducción exacta del original en inglés"
            ],
            [
                "The doctor scheduled regular contacts with her patients for follow-up care.",
                "El médico programó contactos regulares con sus pacientes para seguimiento de la atención."
            ],
            [
                "The project manager maintained constant contact with the team members to ensure progress.",
                "El gerente del proyecto mantuvo una comunicación constante con los miembros de la equipo para asegurar el avance."
            ],
            [
                "The social media influencer had numerous contacts with her followers through various platforms.",
                "La influencera de redes sociales tuvo numerosas interacciones cercanas con sus seguidores a través de diferentes plataformas."
            ],
            [
                "The diplomat established close contacts with foreign officials to negotiate treaties and agreements.",
                "El diplomático estableció relaciones cercanas con funcionarios extranjeros para negociar tratados y acuerdos."
            ]
            ],
            "NULL",
            {
            "Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.": 0
            },
            {
            "Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.": 0
            },
            {
            "Mensaje de información": "La entrada ha terminado su ejecución en la extracción del resultado provisional."
            }
        ])
provisional_result = "manifestación"
prueba = [['la manifestación de los ciudadanos contra la corrupción ha sido una constante en nuestro país durante años.', "the citizens' constant demonstrations against corruption have been a feature of our country for years."],
['el desfile de la marcha por los derechos humanos fue una poderosa manifestación de solidaridad y un llamado a la justicia social.', 'the human rights march was a powerful demonstration of solidarity and a call for social justice.'],
['la manifestación de los estudiantes exigía cambios en el sistema educativo y una mayor inversión en la infraestructura escolar.', 'the student protest demanded changes in the educational system and increased investment in school infrastructure.'],
['la manifestación de los trabajadores contra las condiciones laborales deshumanizantes fue un acto de coraje y solidaridad.', "the workers' protest against inhumane working conditions was an act of courage and solidarity."]]


# print(componenteValidator.get_final_result(element, prueba, provisional_result))


def find_element_with_difference(lst, difference):
    if not lst:
        return []

    # Filtrar los elementos que tienen el segundo valor mayor o igual a la diferencia
    filtered_list = [element for element in lst if element[1] >= difference]

    if not filtered_list:
        return []

    # Encontrar el máximo valor del segundo elemento en la lista filtrada
    max_value = max(filtered_list, key=lambda x: x[1])[1]

    # Obtener todos los elementos con el valor máximo
    max_elements = [element for element in filtered_list if element[1] == max_value]

    # Elegir uno al azar en caso de empate
    return random.choice(max_elements)

# print(find_element_with_difference([('demonstration', 2), ('protest', 2)], 2))