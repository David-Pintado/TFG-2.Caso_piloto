

from io import StringIO
import json
from configparser import ConfigParser
import re
import sys
sys.path.append('..')  # Agrega la carpeta superior al sys.path
sys.path.append("../auxFunctionLibrary") #Agrega la carpeta superior al sys.path
from pythonLib import auxFunctions
from componenteImporter import ComponenteImporter
import componenteQuestionMaker_extraccion
import componenteQuestionMaker_validacion
import componenteQuestionMaker_traduccionGlosa
import componenteQuestionMaker_traduccionInglesEspañol
import componenteQuestionMaker_traduccionEspañolIngles
from componenteLLMCommunicator import ComponenteLLMCommunicator
import componenteExtractor_traduccion
import componenteExtractor_conjuntoFrases
import componenteExtractor_faseExtraccion
import componenteExtractor_faseValidacion
from componenteExporter import ComponenteExporter


def component_importer_test():
    
    config = ConfigParser()
    config.read('./config.ini')
    
    # Inicializamos el componenteImporter para importar los datos de las fuentes 
    component1 = ComponenteImporter(config['file_path']['eng_variant_file'], config['file_path']['eng_synset_file'], config['file_path']['words_spa_file'])
    
    # Guarda el flujo original de salida estándar
    stdout_orig = sys.stdout

    # Define un archivo para redirigir la salida estándar
    archivo_salida = open("./test.txt", "w")

    # Redirige la salida estándar al archivo
    sys.stdout = archivo_salida

    # Si el path no es correcto debe entrar en la excepcion
    component1_test = ComponenteImporter(config['file_path']['eng_variant_file'], config['file_path']['eng_synset_file'],  config['file_path']['words_spa_file_test'])
    test_data_structure = component1_test.generate_data_structure()

    # Cierra el archivo
    archivo_salida.close()
    
    # Restaura la salida estándar
    sys.stdout = stdout_orig
    
    # Abre el archivo de salida en modo lectura
    with open("./test.txt", "r") as archivo:
        # Lee todas las líneas del archivo
        lines = archivo.readlines()

        # Itera sobre cada línea
        for line in lines:
            # Verifica si la línea contiene el mensaje que estás buscando
            if "Archivo \"./files/test_words_1.txt\" no encontrado. Vuelve a introducir una nueva ruta" in line:
                assert True, "Should be there"
                break
        else:
            # Si no se encuentra el mensaje
            assert False, "Should be there"
    
    # Generar la estructura de datos con la que realizar el proceso de explotación de conocimiento
    knowledge_table = component1.generate_data_structure()
    
    # # Después de comprobar en spa_variant_file las palabras a analizar, en total debe haber 33 elementos
    assert len(knowledge_table) == 15, "Should be 15"
    
    # # Contador para contar cuántos elementos tienen una clave
    appearences_person = 0
    appearences_room = 0
    appearences_face = 0
    appearences_paper = 0
    appearences_david = 0

    # # Iterar sobre los elementos del diccionario
    for key, _ in knowledge_table.items():
        if "person" in key:  # Verificar si la clave contiene "person"
            appearences_person += 1
        elif "room" in key: # Verificar si la clave contiene "room"
            appearences_room += 1
        elif "face" in key: # Verificar si la clave contiene "face"
            appearences_face += 1
        elif "paper" in key: # Verificar si la clave contiene "paper"
            appearences_paper += 1
        elif "david" in key: # Verificar si la clave contiene "david"
            appearences_david += 1
            
    # knowledge_table debe contener 1 elementos con "person"
    assert appearences_person == 1, "Should be 1"
    
    # knowledge_table debe contener 1 elementos con "room"
    assert appearences_room == 1, "Should be 1"
    
    # knowledge_table debe contener 1 elementos con "face"
    assert appearences_face == 1, "Should be 1"
    
    # knowledge_table debe contener 1 elementos con "paper"
    assert appearences_paper == 2, "Should be 2"
    
    # knowledge_table debe contener 1 elementos con "david"
    assert appearences_david == 0, "Should be 0"
    
    # Elemento que debe contener el knowledge_table
    element_paper = ("eng-30-14974264-n_paper", {
        "Sense index": "1",
        "English gloss": "A material made of cellulose pulp derived mainly from wood or rags or certain grasses.",
        "Spanish gloss": "NULL",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [],
        "Validation LLM answers": [],
        "Extraction translation": "NULL",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "NULL"
    })
    assert (element_paper[0], element_paper[1]) in knowledge_table.items(), "Should appear"
    
    # Elemento que debe contener el knowledge_table
    element_year = ("eng-30-15203791-n_year", {
        "Sense index": "1",
        "English gloss": "A period of time containing 365 (or 366) days.",
        "Spanish gloss": "NULL",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [],
        "Validation LLM answers": [],
        "Extraction translation": "NULL",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "NULL"
    })
    assert (element_year[0], element_year[1]) in knowledge_table.items(), "Should appear"
    
    # print the output
    # print(json.dumps(knowledge_table, indent=2, ensure_ascii=False))
    
    
def component_question_maker_traduccion_glosa_test():
     
    # Elementos de prueba
    element_paper = ("eng-30-14974264-n_paper", {
        "Sense index": "1",
        "English gloss": "A material made of cellulose pulp derived mainly from wood or rags or certain grasses.",
        "Spanish gloss": "NULL",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [],
        "Validation LLM answers": [],
        "Extraction translation": "NULL",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "NULL"
    })
    element_year = ("eng-30-15203791-n_year", {
        "Sense index": "1",
        "English gloss": "A period of time containing 365 (or 366) days.",
        "Spanish gloss": "NULL",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [],
        "Validation LLM answers": [],
        "Extraction translation": "NULL",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "NULL"
    })
    
    prompts_paper = componenteQuestionMaker_traduccionGlosa.generate_prompts(element_paper)
    prompts_year = componenteQuestionMaker_traduccionGlosa.generate_prompts(element_year)
    
    assert prompts_paper == ["As a translation expert, I need an accurate translation into Spanish of the following phrase: 'A material made of cellulose pulp derived mainly from wood or rags or certain grasses.'."], "Shold be true"
    assert prompts_year == ["As a translation expert, I need an accurate translation into Spanish of the following phrase: 'A period of time containing 365 (or 366) days.'."], "Shold be true"
 
def component_question_maker_traduccion_ingles_español_test():
     
    # Elementos de prueba
    element_plant = ("eng-30-00017222-n_plant", {
        "Sense index": "2",
        "English gloss": "(botany) a living organism lacking the power of locomotion.",
        "Spanish gloss": "NULL",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " 1. The plant, with its green leaves and sturdy stem, stood tall amidst the barren landscape.\n2. The botanist carefully examined the plant's intricate structure, noting the arrangement of its roots and branches.\n3. The plant's delicate petals opened to reveal a vibrant array of colors, attracting bees and butterflies alike.\n4. The plant's leaves, once lush and green, now wilted under the scorching sun, a victim of drought and neglect.\n5. The plant's seeds, carefully nurtured in the soil, sprouted into a new life, a testament to the power of nature and the cycle of life.",
            [
                "The plant, with its green leaves and sturdy stem, stood tall amidst the barren landscape.",
                "The botanist carefully examined the plant's intricate structure, noting the arrangement of its roots and branches.",
                "The plant's delicate petals opened to reveal a vibrant array of colors, attracting bees and butterflies alike.",
                "The plant's leaves, once lush and green, now wilted under the scorching sun, a victim of drought and neglect.",
                "The plant's seeds, carefully nurtured in the soil, sprouted into a new life, a testament to the power of nature and the cycle of life."
            ]
        ],
        "Validation LLM answers": [],
        "Extraction translation": "NULL",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "NULL"
    })
    
    elemet_substance = ("eng-30-00019613-n_substance", {
        "Sense index": "1",
        "English gloss": "The real physical matter of which a person or thing consists.",
        "Spanish gloss": "NULL",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " 1. The substance of the rock is primarily composed of granite.\n2. The chemical substance of water is H2O.\n3. The substance of the human body is made up of various organs and tissues.\n4. The substance of the diamond is carbon, arranged in a crystalline structure.\n5. The substance of the air we breathe is primarily composed of nitrogen, oxygen, and trace amounts of other gases.",
            [
                "The substance of the rock is primarily composed of granite.",
                "The chemical substance of water is H2O.",
                "The substance of the human body is made up of various organs and tissues.",
                "The substance of the diamond is carbon, arranged in a crystalline structure.",
                "The substance of the air we breathe is primarily composed of nitrogen, oxygen, and trace amounts of other gases."
            ]
        ],
        "Validation LLM answers": [],
        "Extraction translation": "NULL",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "NULL"
    })
    
    prompts_plant = componenteQuestionMaker_traduccionInglesEspañol.generate_prompts(element_plant)
    prompts_substance = componenteQuestionMaker_traduccionInglesEspañol.generate_prompts(elemet_substance)
    
    assert prompts_plant == ["As an English to Spanish translation expert, I need an accurate translation into Spanish of the English sentence 'The plant, with its green leaves and sturdy stem, stood tall amidst the barren landscape.', where the noun 'plant' appears in the sense of '(botany) a living organism lacking the power of locomotion.'.",
                             "As an English to Spanish translation expert, I need an accurate translation into Spanish of the English sentence 'The botanist carefully examined the plant's intricate structure, noting the arrangement of its roots and branches.', where the noun 'plant' appears in the sense of '(botany) a living organism lacking the power of locomotion.'.",
                             "As an English to Spanish translation expert, I need an accurate translation into Spanish of the English sentence 'The plant's delicate petals opened to reveal a vibrant array of colors, attracting bees and butterflies alike.', where the noun 'plant' appears in the sense of '(botany) a living organism lacking the power of locomotion.'.",
                             "As an English to Spanish translation expert, I need an accurate translation into Spanish of the English sentence 'The plant's leaves, once lush and green, now wilted under the scorching sun, a victim of drought and neglect.', where the noun 'plant' appears in the sense of '(botany) a living organism lacking the power of locomotion.'.",
                             "As an English to Spanish translation expert, I need an accurate translation into Spanish of the English sentence 'The plant's seeds, carefully nurtured in the soil, sprouted into a new life, a testament to the power of nature and the cycle of life.', where the noun 'plant' appears in the sense of '(botany) a living organism lacking the power of locomotion.'."                      
                            ], "Shold be true"
    
    assert prompts_substance == ["As an English to Spanish translation expert, I need an accurate translation into Spanish of the English sentence 'The substance of the rock is primarily composed of granite.', where the noun 'substance' appears in the sense of 'The real physical matter of which a person or thing consists.'.",
                                 "As an English to Spanish translation expert, I need an accurate translation into Spanish of the English sentence 'The chemical substance of water is H2O.', where the noun 'substance' appears in the sense of 'The real physical matter of which a person or thing consists.'.",
                                 "As an English to Spanish translation expert, I need an accurate translation into Spanish of the English sentence 'The substance of the human body is made up of various organs and tissues.', where the noun 'substance' appears in the sense of 'The real physical matter of which a person or thing consists.'.",
                                 "As an English to Spanish translation expert, I need an accurate translation into Spanish of the English sentence 'The substance of the diamond is carbon, arranged in a crystalline structure.', where the noun 'substance' appears in the sense of 'The real physical matter of which a person or thing consists.'.",
                                 "As an English to Spanish translation expert, I need an accurate translation into Spanish of the English sentence 'The substance of the air we breathe is primarily composed of nitrogen, oxygen, and trace amounts of other gases.', where the noun 'substance' appears in the sense of 'The real physical matter of which a person or thing consists.'."                      
                                ], "Shold be true"
    
def component_question_maker_traduccion_español_ingles_test():
    
    # Elementos de prueba
    elemet_animal = ("eng-30-00015388-n_animal", {
        "Sense index": "1",
        "English gloss": "A living organism characterized by voluntary movement.",
        "Spanish gloss": "Un ser vivo con capacidad de movimiento voluntario.",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " 1. The lion is a majestic animal that roams the African savannah.\n2. The elephant is the largest land animal and can weigh up to six tons.\n3. The cheetah is the fastest animal on land, capable of reaching speeds of over 70 miles per hour.\n4. The monkey is a primate animal that lives in trees and has opposable thumbs.\n5. The shark is a predatory animal that inhabits oceans around the world and can grow up to 30 feet long.",
            [
                " El león es un animal majestuoso que pasea por las praderas africanas.",
                " El elefante es el mayor animal terrestre y puede pesar hasta seis toneladas.",
                " La gueparda es el animal más rápido en tierra, capaz de alcanzar velocidades superiores a los 110 km/h.",
                " El mono es un animal primate que vive en árboles y tiene dedos opuestos.",
                " El tiburón es un animal depredador que habita los océanos en todo el mundo y puede alcanzar una longitud de hasta 30 pies."
            ]
        ],
        "Validation LLM answers": [
            " 1. El leopardo es un animal grande y poderoso.\n2. La jirafa es un animal herbívoro que puede alcanzar alturas de hasta 5,5 metros.\n3. El elefante es un animal inteligente y social que vive en grupos.\n4. El tigre es un animal carnívoro que habita en las selvas tropicales.\n5. La ballena es un animal marino gigante que puede pesar hasta 180 toneladas.",
            [
               "El leopardo es un animal grande y poderoso.",
               "La jirafa es un animal herbívoro que puede alcanzar alturas de hasta 5,5 metros.",
               "El elefante es un animal inteligente y social que vive en grupos.",
               "El tigre es un animal carnívoro que habita en las selvas tropicales.",
               "La ballena es un animal marino gigante que puede pesar hasta 180 toneladas."
            ]
        ],
        "Extraction translation": "animal",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "NULL"
    })
    
    element_cell = ("eng-30-00006484-n_cell", {
        "Sense index": "2",
        "English gloss": "(biology) the basic structural and functional unit of all organisms; they may exist as independent units of life (as in monads) or may form colonies or tissues as in higher plants and animals.",
        "Spanish gloss": "(biología) la unidad estructural y funcional básica de todas las organizaciones vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " 1. The cell is a fundamental building block of all living organisms, providing structure and facilitating essential biological processes.\n2. In multicellular organisms, cells work together to form complex tissues and organs that enable the organism to carry out its functions.\n3. Cells are capable of reproducing through binary fission or other means, allowing for growth and development in both unicellular and multicellular organisms.\n4. The cell membrane is a crucial component of the cell, regulating the exchange of materials between the cell and its environment.\n5. Cells contain various organelles that perform specific functions, such as the mitochondria which generate energy through cellular respiration or the chloroplasts in plant cells that carry out photosynthesis.",
            [
                " La célula es el bloque básico de construcción fundamental en todas las entidades vivientes, proporcionando estructura y facilitando procesos biológicos esenciales.",
                " En los seres multicelulares, las células trabajan juntas para formar tejidos y órganos complejos que permiten al organismo llevar a cabo sus funciones.",
                " Las células son capaces de reproducirse a través de la fisión binaria o otros medios, lo que permite el crecimiento y el desarrollo tanto en organismos unicelulares como en multicelulares.",
                " La membrana celular es un componente crucial de la célula, regulando el intercambio de materiales entre la célula y su entorno.",
                " Las células contienen varias organelas que realizan funciones específicas, como las mitocondrias que generan energía a través de la respiración celular o los cloroplastos en las células vegetales que llevan a cabo la fotosíntesis."
            ]
        ],
        "Validation LLM answers": [
            " 1. Las células son el bloque básico de la vida.\n2. La división celular es un proceso fundamental para la reproducción y el crecimiento.\n3. Cada célula contiene una copia completa del ADN, pero solo una pequeña parte se expresa en cualquier momento.\n4. Las células especializadas tienen funciones específicas en los organismos multicelulares.\n5. La investigación de las células ha revelado muchas verdades sobre la biología y la medicina.",
            [
                "Las células son el bloque básico de la vida.",
                "La división celular es un proceso fundamental para la reproducción y el crecimiento.",
                "Cada célula contiene una copia completa del ADN, pero solo una pequeña parte se expresa en cualquier momento.",
                "Las células especializadas tienen funciones específicas en los organismos multicelulares.",
                "La investigación de las células ha revelado muchas verdades sobre la biología y la medicina."
            ]
        ],
        "Extraction translation": "célula",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "NULL"
    })
  
    prompts_animal = componenteQuestionMaker_traduccionEspañolIngles.generate_prompts(elemet_animal)
    
    assert prompts_animal == ["As an Spanish to English translation expert, I need an accurate translation into English of the Spanish sentence 'El leopardo es un animal grande y poderoso.', where the noun 'animal' appears in the sense of 'Un ser vivo con capacidad de movimiento voluntario.'.",
                              "As an Spanish to English translation expert, I need an accurate translation into English of the Spanish sentence 'La jirafa es un animal herbívoro que puede alcanzar alturas de hasta 5,5 metros.', where the noun 'animal' appears in the sense of 'Un ser vivo con capacidad de movimiento voluntario.'.",
                              "As an Spanish to English translation expert, I need an accurate translation into English of the Spanish sentence 'El elefante es un animal inteligente y social que vive en grupos.', where the noun 'animal' appears in the sense of 'Un ser vivo con capacidad de movimiento voluntario.'.",
                              "As an Spanish to English translation expert, I need an accurate translation into English of the Spanish sentence 'El tigre es un animal carnívoro que habita en las selvas tropicales.', where the noun 'animal' appears in the sense of 'Un ser vivo con capacidad de movimiento voluntario.'.",
                              "As an Spanish to English translation expert, I need an accurate translation into English of the Spanish sentence 'La ballena es un animal marino gigante que puede pesar hasta 180 toneladas.', where the noun 'animal' appears in the sense of 'Un ser vivo con capacidad de movimiento voluntario.'."                      
                             ], "Shold be true"
    
    prompts_cell = componenteQuestionMaker_traduccionEspañolIngles.generate_prompts(element_cell)
    
    assert prompts_cell == ["As an Spanish to English translation expert, I need an accurate translation into English of the Spanish sentence 'Las células son el bloque básico de la vida.', where the noun 'célula' appears in the sense of '(biología) la unidad estructural y funcional básica de todas las organizaciones vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.'.",
                              "As an Spanish to English translation expert, I need an accurate translation into English of the Spanish sentence 'La división celular es un proceso fundamental para la reproducción y el crecimiento.', where the noun 'célula' appears in the sense of '(biología) la unidad estructural y funcional básica de todas las organizaciones vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.'.",
                              "As an Spanish to English translation expert, I need an accurate translation into English of the Spanish sentence 'Cada célula contiene una copia completa del ADN, pero solo una pequeña parte se expresa en cualquier momento.', where the noun 'célula' appears in the sense of '(biología) la unidad estructural y funcional básica de todas las organizaciones vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.'.",
                              "As an Spanish to English translation expert, I need an accurate translation into English of the Spanish sentence 'Las células especializadas tienen funciones específicas en los organismos multicelulares.', where the noun 'célula' appears in the sense of '(biología) la unidad estructural y funcional básica de todas las organizaciones vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.'.",
                              "As an Spanish to English translation expert, I need an accurate translation into English of the Spanish sentence 'La investigación de las células ha revelado muchas verdades sobre la biología y la medicina.', where the noun 'célula' appears in the sense of '(biología) la unidad estructural y funcional básica de todas las organizaciones vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.'."                      
                             ], "Shold be true"
    
def component_question_maker_extraccion_test():
     
    # Elementos de prueba
    element_paper = ("eng-30-14974264-n_paper", {
        "Sense index": "1",
        "English gloss": "A material made of cellulose pulp derived mainly from wood or rags or certain grasses.",
        "Spanish gloss": "NULL",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [],
        "Validation LLM answers": [],
        "Extraction translation": "NULL",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "NULL"
    })
    element_year = ("eng-30-15203791-n_year", {
        "Sense index": "1",
        "English gloss": "A period of time containing 365 (or 366) days.",
        "Spanish gloss": "NULL",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [],
        "Validation LLM answers": [],
        "Extraction translation": "NULL",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "NULL"
    })
    
    prompts_paper = componenteQuestionMaker_extraccion.generate_prompts(element_paper)
    prompts_year = componenteQuestionMaker_extraccion.generate_prompts(element_year)
    
    assert prompts_paper == ["As a linguistics expert, provide five sentences where the noun 'paper' appears in the sense of 'A material made of cellulose pulp derived mainly from wood or rags or certain grasses.'."], "Shold be true"
    assert prompts_year == ["As a linguistics expert, provide five sentences where the noun 'year' appears in the sense of 'A period of time containing 365 (or 366) days.'."], "Shold be true"
   
def component_question_maker_validacion_test():
    
    # Elementos de prueba
    element_plant = ("eng-30-00017222-n_plant", {
        "Sense index": "2",
        "English gloss": "(botany) a living organism lacking the power of locomotion.",
        "Spanish gloss": "(botánica) una entidad viviente que no posee la capacidad de movimiento.",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " 1. The plant, with its green leaves and sturdy stem, stood tall amidst the barren landscape.\n2. The botanist carefully examined the plant's intricate structure, noting the arrangement of its roots and branches.\n3. The plant's delicate petals opened to reveal a vibrant array of colors, attracting bees and butterflies alike.\n4. The plant's leaves, once lush and green, now wilted under the scorching sun, a victim of drought and neglect.\n5. The plant's seeds, carefully nurtured in the soil, sprouted into a new life, a testament to the power of nature and the cycle of life.",
            [
                " La planta, con sus hojas verdes y su tronco firme, se erguía en medio del paisaje árido.",
                " El botánico examinó cuidadosamente la estructura intrincada de la planta, notando la disposición de sus raíces y ramas.",
                " Las delicadas pétalos de la planta se abrieron para revelar un espectacular arreglo de colores, atraendo a las abejas y mariposas igualmente.",
                " Las hojas de la planta, que una vez eran vives y verdes, ahora están marchitando bajo el sol ardiente, víctima de la sequía y la negligencia.",
                " Las semillas de la planta, cuidadosamente nutridas en el suelo, brotaron en una nueva vida, un testimonio del poder de la naturaleza y el ciclo de la vida.",      
            ]
        ],
        "Validation LLM answers": [],
        "Extraction translation": "planta",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "NULL"
    })
    
    elemet_substance = ("eng-30-00019613-n_substance",  {
        "Sense index": "1",
        "English gloss": "The real physical matter of which a person or thing consists.",
        "Spanish gloss": "La materia física real de la que consta una persona o cosa.",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " 1. The substance of the rock is primarily composed of granite.\n2. The chemical substance of water is H2O.\n3. The substance of the human body is made up of various organs and tissues.\n4. The substance of the diamond is carbon, arranged in a crystalline structure.\n5. The substance of the air we breathe is primarily composed of nitrogen, oxygen, and trace amounts of other gases.",
            [
                " La sustancia de la roca está principalmente compuesta de granito.",
                " La sustancia química del agua es H2O.",
                " La sustancia del cuerpo humano está compuesta por varios órganos y tejidos.",
                " La sustancia del diamante es carbono, dispuesto en una estructura cristalina.",
                " La sustancia principal del aire que respiramos está compuesta por nitrógeno, oxígeno y pequeñas cantidades de otros gases.",
            ]
        ],
        "Validation LLM answers": [],
        "Extraction translation": "sustancia",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "NULL"
    })
    
    prompts_plant = componenteQuestionMaker_validacion.generate_prompts(element_plant)
    prompts_substance = componenteQuestionMaker_validacion.generate_prompts(elemet_substance)
    
    assert prompts_plant == ["Como experto en lingüística, proporciona cinco frases en las que el sustantivo 'planta' aparezca en el sentido de '(botánica) una entidad viviente que no posee la capacidad de movimiento.'."], "Shold be true"
    assert prompts_substance == ["Como experto en lingüística, proporciona cinco frases en las que el sustantivo 'sustancia' aparezca en el sentido de 'La materia física real de la que consta una persona o cosa.'."], "Shold be true"
        
    
def component_llm_communicator_test():
    
    config = ConfigParser()
    config.read('./config.ini')
    
    # Guarda el flujo original de salida estándar
    stdout_orig = sys.stdout

    # Define un archivo para redirigir la salida estándar
    archivo_salida = open("./test.txt", "w")

    # Redirige la salida estándar al archivo
    sys.stdout = archivo_salida

    # Si el path del modelo no es correcto no debe dar error, si no indicar el motivo por consola
    componenteLLMCommunicator_test = ComponenteLLMCommunicator(config['file_path']['language_model_path_test']) 
    componenteLLMCommunicator_test.load_model()

    # Cierra el archivo
    archivo_salida.close()
    
    # Restaura la salida estándar
    sys.stdout = stdout_orig
    
    # Abre el archivo de salida en modo lectura
    with open("./test.txt", "r") as archivo:
        # Lee todas las líneas del archivo
        lines = archivo.readlines()

        # Itera sobre cada línea
        for line in lines:
            # Verifica si la línea contiene el mensaje que estás buscando
            if "LLM \"../../models/zephyr-7b-alpha.Q5_K_M.gguf\" no encontrado. Vuelve a introducir una nueva ruta" in line:
                assert True, "Should be there"
                break
        else:
            # Si no se encuentra el mensaje
            assert False, "Should be there"
            
    # Guarda el flujo original de salida estándar
    stdout_orig = sys.stdout

    # Define un archivo para redirigir la salida estándar
    archivo_salida = open("./test.txt", "w")

    # Guarda los flujos originales de salida estándar y de error
    stdout_orig = sys.stdout
    stderr_orig = sys.stderr
    
    # Abre el archivo de salida en modo lectura
    with open("./test.txt", "r") as archivo:
        
        # Redirige la salida estándar al archivo
        sys.stdout = archivo_salida
        # Redirige la salida de error al archivo
        sys.stderr = archivo_salida
        
        # Inicializamos el componenteLLMCommunicator con el llm que vamos a utilizar para conseguir las respuestas provisionales
        componenteLLMCommunicator = ComponenteLLMCommunicator(config['file_path']['language_model_path'])
        
        # Cargamos el modelo de lenguaje que vamos a utilizar para conseguir las respuestas provisionales
        componenteLLMCommunicator.load_model()
        
        # Elementos de prueba
        element_paper = ("eng-30-14974264-n_paper", {
            "Sense index": "1",
            "English gloss": "A material made of cellulose pulp derived mainly from wood or rags or certain grasses.",
            "Spanish gloss": "NULL",
            "Part of speech": "n",
            "Language": "eng",
            "Extraction LLM answers": [],
            "Validation LLM answers": [],
            "Extraction translation": "NULL",
            "Validation translation": "NULL",
            "Correctas": 0,
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
            "Mensaje de información": "NULL"
        })
        element_year = ("eng-30-15203791-n_year", {
            "Sense index": "1",
            "English gloss": "A period of time containing 365 (or 366) days.",
            "Spanish gloss": "NULL",
            "Part of speech": "n",
            "Language": "eng",
            "Extraction LLM answers": [],
            "Validation LLM answers": [],
            "Extraction translation": "NULL",
            "Validation translation": "NULL",
            "Correctas": 0,
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
            "Mensaje de información": "NULL"
        })
    
        # Pruebas de preguntas
        prompts_paper = componenteQuestionMaker_extraccion.generate_prompts(element_paper)
        prompts_year = componenteQuestionMaker_extraccion.generate_prompts(element_year)
        for element in prompts_paper:
            componenteLLMCommunicator.run_the_model(element) 
        for element in prompts_year:
            componenteLLMCommunicator.run_the_model(element) 
        
        # Lee todas las líneas del archivo
        lines = archivo.readlines()

        # Inicializa banderas para cada mensaje buscado
        mensajes_encontrados = {
            "llama_model_loader: loaded meta data with": False,
            "llama_new_context_with_model:": False,
            "Model loaded": False
        }

        # Itera sobre cada línea
        for line in lines:
            # Verifica si la línea contiene alguno de los mensajes buscados
            for mensaje in mensajes_encontrados:
                if mensaje in line:
                    mensajes_encontrados[mensaje] = True

        # Verifica si todos los mensajes buscados se encontraron
        for mensaje, encontrado in mensajes_encontrados.items():
            assert encontrado, f"El mensaje '{mensaje}' no se encontró en el archivo."

        # Verifica la cantidad de veces que aparecen ciertos mensajes específicos
        # Contar cuántas veces aparece la parte en cada elemento de la lista
        assert sum(1 for elemento in lines if "llama_print_timings:        load time =" in elemento) == 2, "Should be 2"
        assert sum(1 for elemento in lines if "llama_print_timings:      sample time =" in elemento) == 2, "Should be 2"
        assert sum(1 for elemento in lines if "llama_print_timings: prompt eval time =" in elemento) == 2, "Should be 2"
        assert sum(1 for elemento in lines if "llama_print_timings:        eval time =" in elemento) == 2, "Should be 2"
        assert sum(1 for elemento in lines if "llama_print_timings:       total time =" in elemento) == 2, "Should be 2"
        assert sum(1 for elemento in lines if "Llama.generate: prefix-match hit" in elemento) == 1, "Should be 1"
        
        
        # Restaura la salida estándar y de error
        sys.stdout = stdout_orig
        sys.stderr = stderr_orig     
        
    # Cierra el archivo
    archivo_salida.close()
    
def component_extractor_translation_test():
    
    element_credit = ('eng-30-00065855-n_credit', {
        'Sense index': '6',
        'English gloss': 'Recognition by a college or university that a course of studies has been successfully completed; typically measured in semester hours.',
        'Spanish gloss': 'NULL',
        'Part of speech': 'n',
        'Language': 'eng',
        'Extraction LLM answers': [
            ' 1. The student received credit for completing the introductory course on computer programming with a grade of B+.\n2. After passing the final exam, Sarah earned three credits towards her degree in psychology.\n3. The summer school program offered by the university awarded students up to six credits for each course completed.\n4. In order to graduate, students must have accumulated at least 120 credits from approved courses.\n5. The transfer student was granted credit for the equivalent of two semesters of college-level French language classes.', 
            [
                'The student received credit for completing the introductory course on computer programming with a grade of B+.',
                'After passing the final exam, Sarah earned three credits towards her degree in psychology.',
                'The summer school program offered by the university awarded students up to six credits for each course completed.',
                'In order to graduate, students must have accumulated at least 120 credits from approved courses.',
                'The transfer student was granted credit for the equivalent of two semesters of college-level French language classes.'
            ]
        ],
        'Validation LLM answers': [],
        'Extraction translation': 'NULL',
        'Validation translation': 'NULL',
        'Correctas': 0,
        'Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase': 0,
        'Incorrectas de tipo 2: la palabra a analizar no aparece en la frase': 0,
        'Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo': 0,
        'Mensaje de información': 'NULL'
    })
    
    llm_answer = [" 'Reconocimiento de una universidad o colegio por la completa realización de un curso de estudios, medido en horas semestrales.'."]
    
    result_credit = componenteExtractor_traduccion.get_result(element_credit, llm_answer)
    
    expected_result_credit = ('eng-30-00065855-n_credit', {
        'Sense index': '6',
        'English gloss': 'Recognition by a college or university that a course of studies has been successfully completed; typically measured in semester hours.',
        'Spanish gloss': 'Reconocimiento de una universidad o colegio por la completa realización de un curso de estudios, medido en horas semestrales.',
        'Part of speech': 'n',
        'Language': 'eng',
        'Extraction LLM answers': [
            ' 1. The student received credit for completing the introductory course on computer programming with a grade of B+.\n2. After passing the final exam, Sarah earned three credits towards her degree in psychology.\n3. The summer school program offered by the university awarded students up to six credits for each course completed.\n4. In order to graduate, students must have accumulated at least 120 credits from approved courses.\n5. The transfer student was granted credit for the equivalent of two semesters of college-level French language classes.', 
            [
                'The student received credit for completing the introductory course on computer programming with a grade of B+.',
                'After passing the final exam, Sarah earned three credits towards her degree in psychology.',
                'The summer school program offered by the university awarded students up to six credits for each course completed.',
                'In order to graduate, students must have accumulated at least 120 credits from approved courses.',
                'The transfer student was granted credit for the equivalent of two semesters of college-level French language classes.'
            ]
        ],
        'Validation LLM answers': [],
        'Extraction translation': 'NULL',
        'Validation translation': 'NULL',
        'Correctas': 0,
        'Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase': 0,
        'Incorrectas de tipo 2: la palabra a analizar no aparece en la frase': 0,
        'Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo': 0,
        'Mensaje de información': 'NULL'
    })
    
    assert expected_result_credit == result_credit, "Should be true"
    
    element_food = ('eng-30-00021265-n_food', {
        'Sense index': '1',
        'English gloss': 'Any substance that can be metabolized by an animal to give energy and build tissue.',
        'Spanish gloss': 'NULL',
        'Part of speech': 'n',
        'Language': 'eng',
        'Extraction LLM answers': [
            ' 1. The farmer grew crops such as wheat, corn, and soybeans for food.\n2. The chef prepared a delicious meal consisting of grilled chicken, roasted vegetables, and steamed rice for dinner.\n3. The nutritionist recommended a balanced diet that included fruits, vegetables, whole grains, lean protein, and healthy fats for optimal health.\n4. The traveler packed snacks such as granola bars, trail mix, and dried fruit for the long hike in the mountains.\n5. The food bank distributed canned goods, fresh produce, and dairy products to families in need.',
            [
                'The farmer grew crops such as wheat, corn, and soybeans for food.',
                'The chef prepared a delicious meal consisting of grilled chicken, roasted vegetables, and steamed rice for dinner.',
                'The nutritionist recommended a balanced diet that included fruits, vegetables, whole grains, lean protein, and healthy fats for optimal health.',
                'The traveler packed snacks such as granola bars, trail mix, and dried fruit for the long hike in the mountains.',
                'The food bank distributed canned goods, fresh produce, and dairy products to families in need.'
            ]
        ],
        'Validation LLM answers': [],
        'Extraction translation': 'NULL',
        'Validation translation': 'NULL',
        'Correctas': 0,
        'Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase': 0,
        'Incorrectas de tipo 2: la palabra a analizar no aparece en la frase': 0,
        'Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo': 0,
        'Mensaje de información': 'NULL'
    })

    llm_answer_2 = [" 'Cualquier sustancia que pueda ser metabolizada por un animal para dar energía y construir tejido'."]
    
    result_food = componenteExtractor_traduccion.get_result(element_food, llm_answer_2)
    
    expected_result_food = ('eng-30-00021265-n_food', {
        'Sense index': '1',
        'English gloss': 'Any substance that can be metabolized by an animal to give energy and build tissue.',
        'Spanish gloss': 'Cualquier sustancia que pueda ser metabolizada por un animal para dar energía y construir tejido.',
        'Part of speech': 'n',
        'Language': 'eng',
        'Extraction LLM answers': [
            ' 1. The farmer grew crops such as wheat, corn, and soybeans for food.\n2. The chef prepared a delicious meal consisting of grilled chicken, roasted vegetables, and steamed rice for dinner.\n3. The nutritionist recommended a balanced diet that included fruits, vegetables, whole grains, lean protein, and healthy fats for optimal health.\n4. The traveler packed snacks such as granola bars, trail mix, and dried fruit for the long hike in the mountains.\n5. The food bank distributed canned goods, fresh produce, and dairy products to families in need.',
            [
                'The farmer grew crops such as wheat, corn, and soybeans for food.',
                'The chef prepared a delicious meal consisting of grilled chicken, roasted vegetables, and steamed rice for dinner.',
                'The nutritionist recommended a balanced diet that included fruits, vegetables, whole grains, lean protein, and healthy fats for optimal health.',
                'The traveler packed snacks such as granola bars, trail mix, and dried fruit for the long hike in the mountains.',
                'The food bank distributed canned goods, fresh produce, and dairy products to families in need.'
            ]
        ],
        'Validation LLM answers': [],
        'Extraction translation': 'NULL',
        'Validation translation': 'NULL',
        'Correctas': 0,
        'Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase': 0,
        'Incorrectas de tipo 2: la palabra a analizar no aparece en la frase': 0,
        'Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo': 0,
        'Mensaje de información': 'NULL'
    })
    
    assert expected_result_food == result_food, "Should be true"

def component_extractor_set_of_phrases_test():
    
    element_credit = ('eng-30-00065855-n_credit', {
        'Sense index': '6',
        'English gloss': 'Recognition by a college or university that a course of studies has been successfully completed; typically measured in semester hours.',
        'Spanish gloss': 'NULL',
        'Part of speech': 'n',
        'Language': 'eng',
        'Extraction LLM answers': [
            ' 1. The student received credit for completing the introductory course on computer programming with a grade of B+.\n2. After passing the final exam, Sarah earned three credits towards her degree in psychology.\n3. The summer school program offered by the university awarded students up to six credits for each course completed.\n4. In order to graduate, students must have accumulated at least 120 credits from approved courses.\n5. The transfer student was granted credit for the equivalent of two semesters of college-level French language classes.'
        ],
        'Validation LLM answers': [],
        'Extraction translation': 'NULL',
        'Validation translation': 'NULL',
        'Correctas': 0,
        'Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase': 0,
        'Incorrectas de tipo 2: la palabra a analizar no aparece en la frase': 0,
        'Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo': 0,
        'Mensaje de información': 'NULL'
    })

    llm_answer = [' 1. The student received credit for completing the introductory course on computer programming with a grade of B+.\n2. After passing the final exam, Sarah earned three credits towards her degree in psychology.\n3. The summer school program offered by the university awarded students up to six credits for each course completed.\n4. In order to graduate, students must have accumulated at least 120 credits from approved courses.\n5. The transfer student was granted credit for the equivalent of two semesters of college-level French language classes.']
    
    result_credit = componenteExtractor_conjuntoFrases.get_result(element_credit, llm_answer)
    
    expected_element_credit = ('eng-30-00065855-n_credit', {
        'Sense index': '6',
        'English gloss': 'Recognition by a college or university that a course of studies has been successfully completed; typically measured in semester hours.',
        'Spanish gloss': 'NULL',
        'Part of speech': 'n',
        'Language': 'eng', 
        'Extraction LLM answers': [
            ' 1. The student received credit for completing the introductory course on computer programming with a grade of B+.\n2. After passing the final exam, Sarah earned three credits towards her degree in psychology.\n3. The summer school program offered by the university awarded students up to six credits for each course completed.\n4. In order to graduate, students must have accumulated at least 120 credits from approved courses.\n5. The transfer student was granted credit for the equivalent of two semesters of college-level French language classes.',
            [
                'The student received credit for completing the introductory course on computer programming with a grade of B+.',
                'After passing the final exam, Sarah earned three credits towards her degree in psychology.',
                'The summer school program offered by the university awarded students up to six credits for each course completed.',
                'In order to graduate, students must have accumulated at least 120 credits from approved courses.',
                'The transfer student was granted credit for the equivalent of two semesters of college-level French language classes.'
            ]
        ],
        'Validation LLM answers': [],
        'Extraction translation': 'NULL',
        'Validation translation': 'NULL',
        'Correctas': 0,
        'Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase': 0,
        'Incorrectas de tipo 2: la palabra a analizar no aparece en la frase': 0,
        'Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo': 0,
        'Mensaje de información': 'NULL'
    })
    
    assert result_credit == expected_element_credit, "Should be true"
    
    element_food = ('eng-30-00021265-n_food', {
        'Sense index': '1',
        'English gloss': 'Any substance that can be metabolized by an animal to give energy and build tissue.',
        'Spanish gloss': 'NULL',
        'Part of speech': 'n',
        'Language': 'eng',
        'Extraction LLM answers': [
            ' 1. The farmer grew crops such as wheat, corn, and soybeans for food.\n2. The chef prepared a delicious meal consisting of grilled chicken, roasted vegetables, and steamed rice for dinner.\n3. The nutritionist recommended a balanced diet that included fruits, vegetables, whole grains, lean protein, and healthy fats for optimal health.\n4. The traveler packed snacks such as granola bars, trail mix, and dried fruit for the long hike in the mountains.\n5. The food bank distributed canned goods, fresh produce, and dairy products to families in need.'
        ],
        'Validation LLM answers': [],
        'Extraction translation': 'NULL',
        'Validation translation': 'NULL',
        'Correctas': 0,
        'Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase': 0,
        'Incorrectas de tipo 2: la palabra a analizar no aparece en la frase': 0,
        'Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo': 0,
        'Mensaje de información': 'NULL'
    })

    llm_answer_2 = [' 1. The farmer grew crops such as wheat, corn, and soybeans for food.\n2. The chef prepared a delicious meal consisting of grilled chicken, roasted vegetables, and steamed rice for dinner.\n3. The nutritionist recommended a balanced diet that included fruits, vegetables, whole grains, lean protein, and healthy fats for optimal health.\n4. The traveler packed snacks such as granola bars, trail mix, and dried fruit for the long hike in the mountains.\n5. The food bank distributed canned goods, fresh produce, and dairy products to families in need.']
    
    result_food = componenteExtractor_conjuntoFrases.get_result(element_food, llm_answer_2)
    
    expected_element_food = ('eng-30-00021265-n_food', {
        'Sense index': '1',
        'English gloss': 'Any substance that can be metabolized by an animal to give energy and build tissue.',
        'Spanish gloss': 'NULL',
        'Part of speech': 'n',
        'Language': 'eng',
        'Extraction LLM answers': [
            ' 1. The farmer grew crops such as wheat, corn, and soybeans for food.\n2. The chef prepared a delicious meal consisting of grilled chicken, roasted vegetables, and steamed rice for dinner.\n3. The nutritionist recommended a balanced diet that included fruits, vegetables, whole grains, lean protein, and healthy fats for optimal health.\n4. The traveler packed snacks such as granola bars, trail mix, and dried fruit for the long hike in the mountains.\n5. The food bank distributed canned goods, fresh produce, and dairy products to families in need.',
            [
                'The farmer grew crops such as wheat, corn, and soybeans for food.',
                'The chef prepared a delicious meal consisting of grilled chicken, roasted vegetables, and steamed rice for dinner.',
                'The nutritionist recommended a balanced diet that included fruits, vegetables, whole grains, lean protein, and healthy fats for optimal health.',
                'The traveler packed snacks such as granola bars, trail mix, and dried fruit for the long hike in the mountains.',
                'The food bank distributed canned goods, fresh produce, and dairy products to families in need.'
            ]
        ],
        'Validation LLM answers': [],
        'Extraction translation': 'NULL',
        'Validation translation': 'NULL',
        'Correctas': 0,
        'Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase': 0,
        'Incorrectas de tipo 2: la palabra a analizar no aparece en la frase': 0,
        'Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo': 0,
        'Mensaje de información': 'NULL'
    })
    
    assert expected_element_food == result_food, "Should be true"

def component_extractor_extraccion_test():
    
    # --------------------------------------   Prueba 1   -------------------------------------------
        
    # Elementos de prueba
    element_cell = ("eng-30-00006484-n_cell", {
            "Sense index": "2",
            "English gloss": "(biology) the basic structural and functional unit of all organisms; they may exist as independent units of life (as in monads) or may form colonies or tissues as in higher plants and animals.",
            "Spanish gloss": "(biología) la unidad estructural y funcional básica de todas las organizaciones vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.",
            "Part of speech": "n",
            "Language": "eng",
            "Extraction LLM answers": [
                " 1. The cell is a fundamental building block of all living organisms, providing structure and facilitating essential biological processes.\n2. In multicellular organisms, cells work together to form complex tissues and organs that enable the organism to carry out its functions.\n3. Cells are capable of reproducing through binary fission or other means, allowing for growth and development in both unicellular and multicellular organisms.\n4. The cell membrane is a crucial component of the cell, regulating the exchange of materials between the cell and its environment.\n5. Cells contain various organelles that perform specific functions, such as the mitochondria which generate energy through cellular respiration or the chloroplasts in plant cells that carry out photosynthesis.",
                [
                    " La célula es el bloque básico de construcción fundamental en todas las entidades vivientes, proporcionando estructura y facilitando procesos biológicos esenciales.",
                    " En los seres multicelulares, las células trabajan juntas para formar tejidos y órganos complejos que permiten al organismo llevar a cabo sus funciones.",
                    " Las células son capaces de reproducirse a través de la fisión binaria o otros medios, lo que permite el crecimiento y el desarrollo tanto en organismos unicelulares como en multicelulares.",
                    " La membrana celular es un componente crucial de la célula, regulando el intercambio de materiales entre la célula y su entorno.",
                    " Las células contienen varias organelas que realizan funciones específicas, como las mitocondrias que generan energía a través de la respiración celular o los cloroplastos en las células vegetales que llevan a cabo la fotosíntesis."
                ]
            ],
            "Validation LLM answers": [],
            "Extraction translation": "NULL",
            "Validation translation": "NULL",
            "Correctas": 0,
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
            "Mensaje de información": "NULL"
    })
    
    llm_answer_list_1 = [
            " 1. The cell is a fundamental building block of all living organisms, providing structure and facilitating essential biological processes.\n2. In multicellular organisms, cells work together to form complex tissues and organs that enable the organism to carry out its functions.\n3. Cells are capable of reproducing through binary fission or other means, allowing for growth and development in both unicellular and multicellular organisms.\n4. The cell membrane is a crucial component of the cell, regulating the exchange of materials between the cell and its environment.\n5. Cells contain various organelles that perform specific functions, such as the mitochondria which generate energy through cellular respiration or the chloroplasts in plant cells that carry out photosynthesis.",
            [
                " La célula es el bloque básico de construcción fundamental en todas las entidades vivientes, proporcionando estructura y facilitando procesos biológicos esenciales.",
                " En los seres multicelulares, las células trabajan juntas para formar tejidos y órganos complejos que permiten al organismo llevar a cabo sus funciones.",
                " Las células son capaces de reproducirse a través de la fisión binaria o otros medios, lo que permite el crecimiento y el desarrollo tanto en organismos unicelulares como en multicelulares.",
                " La membrana celular es un componente crucial de la célula, regulando el intercambio de materiales entre la célula y su entorno.",
                " Las células contienen varias organelas que realizan funciones específicas, como las mitocondrias que generan energía a través de la respiración celular o los cloroplastos en las células vegetales que llevan a cabo la fotosíntesis."
            ]
        ]
    
    result_cell = componenteExtractor_faseExtraccion.get_result(element_cell, llm_answer_list_1)
    
    expected_element_cell = ("eng-30-00006484-n_cell", {
        "Sense index": "2",
        "English gloss": "(biology) the basic structural and functional unit of all organisms; they may exist as independent units of life (as in monads) or may form colonies or tissues as in higher plants and animals.",
        "Spanish gloss": "(biología) la unidad estructural y funcional básica de todas las organizaciones vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " 1. The cell is a fundamental building block of all living organisms, providing structure and facilitating essential biological processes.\n2. In multicellular organisms, cells work together to form complex tissues and organs that enable the organism to carry out its functions.\n3. Cells are capable of reproducing through binary fission or other means, allowing for growth and development in both unicellular and multicellular organisms.\n4. The cell membrane is a crucial component of the cell, regulating the exchange of materials between the cell and its environment.\n5. Cells contain various organelles that perform specific functions, such as the mitochondria which generate energy through cellular respiration or the chloroplasts in plant cells that carry out photosynthesis.",
            [
                " La célula es el bloque básico de construcción fundamental en todas las entidades vivientes, proporcionando estructura y facilitando procesos biológicos esenciales.",
                " En los seres multicelulares, las células trabajan juntas para formar tejidos y órganos complejos que permiten al organismo llevar a cabo sus funciones.",
                " Las células son capaces de reproducirse a través de la fisión binaria o otros medios, lo que permite el crecimiento y el desarrollo tanto en organismos unicelulares como en multicelulares.",
                " La membrana celular es un componente crucial de la célula, regulando el intercambio de materiales entre la célula y su entorno.",
                " Las células contienen varias organelas que realizan funciones específicas, como las mitocondrias que generan energía a través de la respiración celular o los cloroplastos en las células vegetales que llevan a cabo la fotosíntesis."
            ]
        ],
        "Validation LLM answers": [],
        "Extraction translation": "célula",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "NULL"
    })
    
    assert result_cell == expected_element_cell, "Should be true"
    
    # --------------------------------------   Prueba 2   -------------------------------------------
   
    # Elementos de prueba
    element_cause = ("eng-30-00007347-n_cause", {
            "Sense index": "4",
            "English gloss": "Any entity that produces an effect or is responsible for events or results.",
            "Spanish gloss": "Cualquier entidad que produce un efecto o es responsable de los eventos o resultados'.",
            "Part of speech": "n",
            "Language": "eng",
            "Extraction LLM answers": [
                " 1. The cause of the accident was a malfunctioning brake system.\n2. The lack of rainfall is the primary cause of the drought.\n3. The cause of the disease outbreak can be traced back to contaminated food.\n4. The cause of the financial crisis was a combination of factors, including risky investments and lax regulation.\n5. The cause of the explosion was a gas leak in the pipeline.",
                [
                    " La causa del accidente fue un sistema de frenos defectuoso.",
                    " La falta de lluvias es la causa principal de la sequía.",
                    " La causa de la salida de la enfermedad se puede rastrear hasta la comida contaminada.",
                    " La causa de la crisis financiera fue una combinación de factores, incluyendo inversiones riesgosas y regulación relajada.",
                    " La causa de la explosión fue una fuga de gas en el conducto."
                ]
            ],
            "Validation LLM answers": [],
            "Extraction translation": "NULL",
            "Validation translation": "NULL",
            "Correctas": 0,
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
            "Mensaje de información": "NULL"
    })
    
    llm_answer_list_2 = [
            " 1. The cause of the accident was a malfunctioning brake system.\n2. The lack of rainfall is the primary cause of the drought.\n3. The cause of the disease outbreak can be traced back to contaminated food.\n4. The cause of the financial crisis was a combination of factors, including risky investments and lax regulation.\n5. The cause of the explosion was a gas leak in the pipeline.",
            [
                " La causa del accidente fue un sistema de frenos defectuoso.",
                " La falta de lluvias es la causa principal de la sequía.",
                " La causa de la salida de la enfermedad se puede rastrear hasta la comida contaminada.",
                " La causa de la crisis financiera fue una combinación de factores, incluyendo inversiones riesgosas y regulación relajada.",
                " La causa de la explosión fue una fuga de gas en el conducto."
            ]
        ]

    result_cause = componenteExtractor_faseExtraccion.get_result(element_cause, llm_answer_list_2)
    
    expected_element_cause = ("eng-30-00007347-n_cause", {
        "Sense index": "4",
        "English gloss": "Any entity that produces an effect or is responsible for events or results.",
        "Spanish gloss": "Cualquier entidad que produce un efecto o es responsable de los eventos o resultados'.",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " 1. The cause of the accident was a malfunctioning brake system.\n2. The lack of rainfall is the primary cause of the drought.\n3. The cause of the disease outbreak can be traced back to contaminated food.\n4. The cause of the financial crisis was a combination of factors, including risky investments and lax regulation.\n5. The cause of the explosion was a gas leak in the pipeline.",
            [
                " La causa del accidente fue un sistema de frenos defectuoso.",
                " La falta de lluvias es la causa principal de la sequía.",
                " La causa de la salida de la enfermedad se puede rastrear hasta la comida contaminada.",
                " La causa de la crisis financiera fue una combinación de factores, incluyendo inversiones riesgosas y regulación relajada.",
                " La causa de la explosión fue una fuga de gas en el conducto."
            ]
        ],
        "Validation LLM answers": [],
        "Extraction translation": "causa",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "NULL"
    })
    
    assert result_cause == expected_element_cause, "Should be True"
    
    # --------------------------------------   Prueba 3   -------------------------------------------
    
    llm_answer_list_3 = [
            " 1. The cell is a fundamental building block of all living organisms, providing structure and facilitating essential biological processes.\n2. In multicellular organisms, cells work together to form complex tissues and organs that enable the organism to carry out its functions.\n3. Cells are capable of reproducing through binary fission or other means, allowing for growth and development in both unicellular and multicellular organisms.\n4. The cell membrane is a crucial component of the cell, regulating the exchange of materials between the cell and its environment.\n5. Cells contain various organelles that perform specific functions, such as the mitochondria which generate energy through cellular respiration or the chloroplasts in plant cells that carry out photosynthesis.",
            [
                " La célula procariota es el bloque básico de construcción fundamental en todas las entidades vivientes, proporcionando estructura y facilitando procesos biológicos esenciales.",
                " En los seres multicelulares, las células trabajan juntas para formar tejidos y órganos complejos que permiten al organismo llevar a cabo sus funciones.",
                " Las células procariotas son capaces de reproducirse a través de la fisión binaria o otros medios, lo que permite el crecimiento y el desarrollo tanto en organismos unicelulares como en multicelulares.",
                " La membrana celular es un componente crucial de la célula, regulando el intercambio de materiales entre la célula y su entorno.",
                " Las células procariotas contienen varias organelas que realizan funciones específicas, como las mitocondrias que generan energía a través de la respiración celular o los cloroplastos en las células vegetales que llevan a cabo la fotosíntesis."
            ]
        ]
    
    result_cell_2 = componenteExtractor_faseExtraccion.get_result(element_cause, llm_answer_list_3)
    
    expected_element_cause_2 = ("eng-30-00007347-n_cause", {
        "Sense index": "4",
        "English gloss": "Any entity that produces an effect or is responsible for events or results.",
        "Spanish gloss": "Cualquier entidad que produce un efecto o es responsable de los eventos o resultados'.",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " 1. The cause of the accident was a malfunctioning brake system.\n2. The lack of rainfall is the primary cause of the drought.\n3. The cause of the disease outbreak can be traced back to contaminated food.\n4. The cause of the financial crisis was a combination of factors, including risky investments and lax regulation.\n5. The cause of the explosion was a gas leak in the pipeline.",
            [
                " La causa del accidente fue un sistema de frenos defectuoso.",
                " La falta de lluvias es la causa principal de la sequía.",
                " La causa de la salida de la enfermedad se puede rastrear hasta la comida contaminada.",
                " La causa de la crisis financiera fue una combinación de factores, incluyendo inversiones riesgosas y regulación relajada.",
                " La causa de la explosión fue una fuga de gas en el conducto."
            ]
        ],
        "Validation LLM answers": [],
        "Extraction translation": "NULL",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 5,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "La entrada ha terminado su ejecución en la fase de extracción."
    })
    
    assert result_cell_2 == expected_element_cause_2, "Should be true"
     

    
def component_extractor_validacion_test():
        
    # --------------------------------------   Prueba 1   -------------------------------------------
    
    element_cause = ("eng-30-00007347-n_cause", {
        "Sense index": "4",
        "English gloss": "Any entity that produces an effect or is responsible for events or results.",
        "Spanish gloss": "Cualquier entidad que produce un efecto o es responsable de los eventos o resultados'.",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " 1. The cause of the accident was a malfunctioning brake system.\n2. The lack of rainfall is the primary cause of the drought.\n3. The cause of the disease outbreak can be traced back to contaminated food.\n4. The cause of the financial crisis was a combination of factors, including risky investments and lax regulation.\n5. The cause of the explosion was a gas leak in the pipeline.",
            [
                " La causa del accidente fue un sistema de frenos defectuoso.",
                " La falta de lluvias es la causa principal de la sequía.",
                " La causa de la salida de la enfermedad se puede rastrear hasta la comida contaminada.",
                " La causa de la crisis financiera fue una combinación de factores, incluyendo inversiones riesgosas y regulación relajada.",
                " La causa de la explosión fue una fuga de gas en el conducto."
            ]
        ],
        "Validation LLM answers": [
            " 1) La causa del accidente fue la falta de atención del conductor.\n2) El cambio climático es una causa preocupante para la supervivencia de las especies en peligro.\n3) La pobreza es una causa importante de la mortalidad infantil en muchos países.\n4) La falta de educación es una causa de la desigualdad social.\n5) El estrés es una causa común de problemas de salud mental.",
            [
                " The cause of the accident was the lack of attention by the driver.",
                " The climate change is a concerning cause for the survival of endangered species.",
                " Poverty is a significant cause of childhood mortality in many countries.",
                " The lack of education is a cause of social inequality.",
                " Stress is a common cause of mental health problems."
            ]
        ],
        "Extraction translation": "causa",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 5,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "La entrada ha terminado su ejecución en la fase de extracción."
    })
    
    llm_answer_list_1 = [
        " 1) La causa del accidente fue la falta de atención del conductor.\n2) El cambio climático es una causa preocupante para la supervivencia de las especies en peligro.\n3) La pobreza es una causa importante de la mortalidad infantil en muchos países.\n4) La falta de educación es una causa de la desigualdad social.\n5) El estrés es una causa común de problemas de salud mental.",
        [
            " The cause of the accident was the lack of attention by the driver.",
            " The climate change is a concerning cause for the survival of endangered species.",
            " Poverty is a significant cause of childhood mortality in many countries.",
            " The lack of education is a cause of social inequality.",
            " Stress is a common cause of mental health problems."
        ]
    ]
    
    expected_element_cause = ("eng-30-00007347-n_cause", {
        "Sense index": "4",
        "English gloss": "Any entity that produces an effect or is responsible for events or results.",
        "Spanish gloss": "Cualquier entidad que produce un efecto o es responsable de los eventos o resultados'.",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " 1. The cause of the accident was a malfunctioning brake system.\n2. The lack of rainfall is the primary cause of the drought.\n3. The cause of the disease outbreak can be traced back to contaminated food.\n4. The cause of the financial crisis was a combination of factors, including risky investments and lax regulation.\n5. The cause of the explosion was a gas leak in the pipeline.",
            [
                " La causa del accidente fue un sistema de frenos defectuoso.",
                " La falta de lluvias es la causa principal de la sequía.",
                " La causa de la salida de la enfermedad se puede rastrear hasta la comida contaminada.",
                " La causa de la crisis financiera fue una combinación de factores, incluyendo inversiones riesgosas y regulación relajada.",
                " La causa de la explosión fue una fuga de gas en el conducto."
            ]
        ],
        "Validation LLM answers": [
            " 1) La causa del accidente fue la falta de atención del conductor.\n2) El cambio climático es una causa preocupante para la supervivencia de las especies en peligro.\n3) La pobreza es una causa importante de la mortalidad infantil en muchos países.\n4) La falta de educación es una causa de la desigualdad social.\n5) El estrés es una causa común de problemas de salud mental.",
            [
                " The cause of the accident was the lack of attention by the driver.",
                " The climate change is a concerning cause for the survival of endangered species.",
                " Poverty is a significant cause of childhood mortality in many countries.",
                " The lack of education is a cause of social inequality.",
                " Stress is a common cause of mental health problems."
            ]
        ],
        "Extraction translation": "causa",
        "Validation translation": "causa",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 5,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "La entrada ha terminado su ejecución en la fase de extracción."
    })
    
    result_cause = componenteExtractor_faseValidacion.get_result(element_cause, llm_answer_list_1)
    
    assert result_cause == expected_element_cause, "Should be True"
    
    # --------------------------------------   Prueba 2   -------------------------------------------
    
    element_cell = ("eng-30-00006484-n_cell", {
        "Sense index": "2",
        "English gloss": "(biology) the basic structural and functional unit of all organisms; they may exist as independent units of life (as in monads) or may form colonies or tissues as in higher plants and animals.",
        "Spanish gloss": "(biología) la unidad estructural y funcional básica de todas las organizaciones vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " 1. The cell is a fundamental building block of all living organisms, providing structure and facilitating essential biological processes.\n2. In multicellular organisms, cells work together to form complex tissues and organs that enable the organism to carry out its functions.\n3. Cells are capable of reproducing through binary fission or other means, allowing for growth and development in both unicellular and multicellular organisms.\n4. The cell membrane is a crucial component of the cell, regulating the exchange of materials between the cell and its environment.\n5. Cells contain various organelles that perform specific functions, such as the mitochondria which generate energy through cellular respiration or the chloroplasts in plant cells that carry out photosynthesis.",
            [
                " La célula es el bloque básico de construcción fundamental en todas las entidades vivientes, proporcionando estructura y facilitando procesos biológicos esenciales.",
                " En los seres multicelulares, las células trabajan juntas para formar tejidos y órganos complejos que permiten al organismo llevar a cabo sus funciones.",
                " Las células son capaces de reproducirse a través de la fisión binaria o otros medios, lo que permite el crecimiento y el desarrollo tanto en organismos unicelulares como en multicelulares.",
                " La membrana celular es un componente crucial de la célula, regulando el intercambio de materiales entre la célula y su entorno.",
                " Las células contienen varias organelas que realizan funciones específicas, como las mitocondrias que generan energía a través de la respiración celular o los cloroplastos en las células vegetales que llevan a cabo la fotosíntesis."
            ]
        ],
        "Validation LLM answers": [
            " 1. Las células son el bloque básico de la vida.\n2. La división celular es un proceso fundamental para la reproducción y el crecimiento.\n3. Cada célula contiene una copia completa del ADN, pero solo una pequeña parte se expresa en cualquier momento.\n4. Las células especializadas tienen funciones específicas en los organismos multicelulares.\n5. La investigación de las células ha revelado muchas verdades sobre la biología y la medicina.",
            [
                " Cells are the fundamental building blocks of life.",
                " The cell division process is a fundamental one for reproduction and growth.",
                " Each cell contains a complete copy of DNA, but only a small portion is expressed at any given time.",
                " 'The specialized cells have specific functions in multicellular organisms.'",
                " The investigation of cells has revealed many truths about biology and medicine."
            ]
        ],
        "Extraction translation": "célula",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 5,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "La entrada ha terminado su ejecución en la fase de extracción."
    })
    
    llm_answer_list_2 = [
            " 1. Las células son el bloque básico de la vida.\n2. La división celular es un proceso fundamental para la reproducción y el crecimiento.\n3. Cada célula contiene una copia completa del ADN, pero solo una pequeña parte se expresa en cualquier momento.\n4. Las células especializadas tienen funciones específicas en los organismos multicelulares.\n5. La investigación de las células ha revelado muchas verdades sobre la biología y la medicina.",
            [
                " Cells are the fundamental building blocks of life.",
                " The cell division process is a fundamental one for reproduction and growth.",
                " Each cell contains a complete copy of DNA, but only a small portion is expressed at any given time.",
                " 'The specialized cells have specific functions in multicellular organisms.'",
                " The investigation of cells has revealed many truths about biology and medicine."
            ]
        ]
        
    result_cell = componenteExtractor_faseValidacion.get_result(element_cell, llm_answer_list_2)
    
    expected_element_cell = ("eng-30-00006484-n_cell", {
        "Sense index": "2",
        "English gloss": "(biology) the basic structural and functional unit of all organisms; they may exist as independent units of life (as in monads) or may form colonies or tissues as in higher plants and animals.",
        "Spanish gloss": "(biología) la unidad estructural y funcional básica de todas las organizaciones vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " 1. The cell is a fundamental building block of all living organisms, providing structure and facilitating essential biological processes.\n2. In multicellular organisms, cells work together to form complex tissues and organs that enable the organism to carry out its functions.\n3. Cells are capable of reproducing through binary fission or other means, allowing for growth and development in both unicellular and multicellular organisms.\n4. The cell membrane is a crucial component of the cell, regulating the exchange of materials between the cell and its environment.\n5. Cells contain various organelles that perform specific functions, such as the mitochondria which generate energy through cellular respiration or the chloroplasts in plant cells that carry out photosynthesis.",
            [
                " La célula es el bloque básico de construcción fundamental en todas las entidades vivientes, proporcionando estructura y facilitando procesos biológicos esenciales.",
                " En los seres multicelulares, las células trabajan juntas para formar tejidos y órganos complejos que permiten al organismo llevar a cabo sus funciones.",
                " Las células son capaces de reproducirse a través de la fisión binaria o otros medios, lo que permite el crecimiento y el desarrollo tanto en organismos unicelulares como en multicelulares.",
                " La membrana celular es un componente crucial de la célula, regulando el intercambio de materiales entre la célula y su entorno.",
                " Las células contienen varias organelas que realizan funciones específicas, como las mitocondrias que generan energía a través de la respiración celular o los cloroplastos en las células vegetales que llevan a cabo la fotosíntesis."
            ]
        ],
        "Validation LLM answers": [
            " 1. Las células son el bloque básico de la vida.\n2. La división celular es un proceso fundamental para la reproducción y el crecimiento.\n3. Cada célula contiene una copia completa del ADN, pero solo una pequeña parte se expresa en cualquier momento.\n4. Las células especializadas tienen funciones específicas en los organismos multicelulares.\n5. La investigación de las células ha revelado muchas verdades sobre la biología y la medicina.",
            [
                " Cells are the fundamental building blocks of life.",
                " The cell division process is a fundamental one for reproduction and growth.",
                " Each cell contains a complete copy of DNA, but only a small portion is expressed at any given time.",
                " 'The specialized cells have specific functions in multicellular organisms.'",
                " The investigation of cells has revealed many truths about biology and medicine."
            ]
        ],
        "Extraction translation": "célula",
        "Validation translation": "célula",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 5,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "La entrada ha terminado su ejecución en la fase de extracción."
    })
    
    assert result_cell == expected_element_cell, "Should be True"
    
    # --------------------------------------   Prueba 2   -------------------------------------------
    
    element_object =  ("eng-30-00002684-n_object", {
        "Sense index": "1",
        "English gloss": "A tangible and visible entity; an entity that can cast a shadow.",
        "Spanish gloss": "Una entidad tangible y visible; una entidad que puede hacer sombra'.",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " The object on the table was a vase made of porcelain. Its delicate curves and intricate design were mesmerizing to behold. As I approached it, its shadow grew longer and more defined, casting a soft glow across the room.\n\nThe object in my hand was a small stone, smooth and polished by years of tumbling through streams and rivers. It felt heavy and substantial, as if it held within it some ancient wisdom or secret knowledge. As I held it up to the light, its shadow danced on the ground, a flickering reminder of its solidity and weight.\n\nThe object in front of me was a painting, a masterpiece of color and texture that seemed to come alive as I gazed upon it. Its brushstrokes were bold and confident, each one casting a distinct shadow against the wall behind it. The shadows added depth and dimension to the painting, transforming it from a mere image into a living, breathing entity",
            [
                " El objeto en la mesa era una jarra de porcelana.",
                " Sus delicadas curvas y su compleja forma eran hipnóticas de contemplar.",
                " Mientras me acercaba, su sombra se alargó y se definió más, proyectando una luz suave en la habitación.",
                " El objeto en mi mano era una pequeña piedra, lisa y pulida por años de rodar por arroyos y ríos.",
                " Se sintió pesado y sólido, como si albergara dentro de él alguna sabiduría antigua o conocimiento oculto. (Noun: objeto)",
                " Mientras lo sostuviera hacia la luz, su sombra bailaba en el suelo, una danza flickerante que recordaba su sólida y pesada realidad.",
                " El objeto que estaba delante de mí era una pintura, un maestrito de color y textura que parecía vivir mientras la miraba.",
                " Sus trazos eran audaces y confiados, cada uno dejando una sombra distintiva contra la pared detrás de él.",
                " Las sombras agregaron profundidad y dimensión al cuadro, transformándolo en una entidad viviente e respirante."
            ]
        ],
        "Validation LLM answers": [
            " 1. The object cast a shadow on the wall.\n2. The object was hidden behind the tree.\n3. The object was found at the bottom of the lake.\n4. The object was buried under the sand.\n5. The object was obscured by the fog.",
            [
                " The object (tangible and visible entity) cast a shadow on the wall.",
                " The item was concealed behind the tree.\n\n",
                " The item was discovered at the bottom of the lake.",
                " The item was buried beneath the sand.\n\n",
                " The object was hidden by the fog.\n\n"
            ]
        ],
        "Extraction translation": "objeto",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 5,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "La entrada ha terminado su ejecución en la fase de extracción."
    })

    llm_answer_list_3 = [
            " 1. The object cast a shadow on the wall.\n2. The object was hidden behind the tree.\n3. The object was found at the bottom of the lake.\n4. The object was buried under the sand.\n5. The object was obscured by the fog.",
            [
                " The object (tangible and visible entity) cast a shadow on the wall.",
                " The item was concealed behind the tree.\n\n",
                " The item was discovered at the bottom of the lake.",
                " The item was buried beneath the sand.\n\n",
                " The object was hidden by the fog.\n\n"
            ]
        ]
    
    result_object = componenteExtractor_faseValidacion.get_result(element_object, llm_answer_list_3)
    
    expected_element_object =  ("eng-30-00002684-n_object", {
        "Sense index": "1",
        "English gloss": "A tangible and visible entity; an entity that can cast a shadow.",
        "Spanish gloss": "Una entidad tangible y visible; una entidad que puede hacer sombra'.",
        "Part of speech": "n",
        "Language": "eng",
        "Extraction LLM answers": [
            " The object on the table was a vase made of porcelain. Its delicate curves and intricate design were mesmerizing to behold. As I approached it, its shadow grew longer and more defined, casting a soft glow across the room.\n\nThe object in my hand was a small stone, smooth and polished by years of tumbling through streams and rivers. It felt heavy and substantial, as if it held within it some ancient wisdom or secret knowledge. As I held it up to the light, its shadow danced on the ground, a flickering reminder of its solidity and weight.\n\nThe object in front of me was a painting, a masterpiece of color and texture that seemed to come alive as I gazed upon it. Its brushstrokes were bold and confident, each one casting a distinct shadow against the wall behind it. The shadows added depth and dimension to the painting, transforming it from a mere image into a living, breathing entity",
            [
                " El objeto en la mesa era una jarra de porcelana.",
                " Sus delicadas curvas y su compleja forma eran hipnóticas de contemplar.",
                " Mientras me acercaba, su sombra se alargó y se definió más, proyectando una luz suave en la habitación.",
                " El objeto en mi mano era una pequeña piedra, lisa y pulida por años de rodar por arroyos y ríos.",
                " Se sintió pesado y sólido, como si albergara dentro de él alguna sabiduría antigua o conocimiento oculto. (Noun: objeto)",
                " Mientras lo sostuviera hacia la luz, su sombra bailaba en el suelo, una danza flickerante que recordaba su sólida y pesada realidad.",
                " El objeto que estaba delante de mí era una pintura, un maestrito de color y textura que parecía vivir mientras la miraba.",
                " Sus trazos eran audaces y confiados, cada uno dejando una sombra distintiva contra la pared detrás de él.",
                " Las sombras agregaron profundidad y dimensión al cuadro, transformándolo en una entidad viviente e respirante."
            ]
        ],
        "Validation LLM answers": [
            " 1. The object cast a shadow on the wall.\n2. The object was hidden behind the tree.\n3. The object was found at the bottom of the lake.\n4. The object was buried under the sand.\n5. The object was obscured by the fog.",
            [
                " The object (tangible and visible entity) cast a shadow on the wall.",
                " The item was concealed behind the tree.\n\n",
                " The item was discovered at the bottom of the lake.",
                " The item was buried beneath the sand.\n\n",
                " The object was hidden by the fog.\n\n"
            ]
        ],
        "Extraction translation": "objeto",
        "Validation translation": "NULL",
        "Correctas": 0,
        "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,  
        "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 5,
        "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
        "Mensaje de información": "La entrada ha terminado su ejecución en la fase de validación."
    })
    
    assert result_object == expected_element_object, "Should be true"
    
def component_exporter_test():
    
    knowledge_table = {
        "eng-30-00002684-n_object": {
            "Sense index": "1",
            "English gloss": "A tangible and visible entity; an entity that can cast a shadow.",
            "Spanish gloss": "Una entidad tangible y visible; una entidad que puede hacer sombra'.",
            "Part of speech": "n",
            "Language": "eng",
            "Extraction LLM answers": [
                " The object on the table was a vase made of porcelain. Its intricate design caught my eye as I walked by. The object in the corner of the room was a large, wooden bookshelf. It towered over me, and I could see the shadows it cast on the floor. The object that lay at my feet was a small, red ball. It rolled away from me as soon as I picked it up, leaving behind a faint shadow. The object in the distance was a tall, metal fence. Its sharp edges created deep shadows on the ground below. The object that hung from the ceiling was a chandelier made of crystal. Its light cast long, shimmering shadows on the walls.",
                [
                    " El objeto en la mesa era una jarra hecha de porcelana.",
                    " Su compleja forma me llamó la atención mientras caminaba por allí.",
                    " El objeto en la esquina de la habitación era un gran estante de madera para libros.",
                    " 'Se elevaba sobre mí y podía ver las sombras que proyectaba en el suelo'.",
                    " El objeto que estaba en mis pies era una pequeña pelota roja.",
                    " 'Se deslizó lejos de mí al mismo tiempo que lo agarré, dejando atrás una sombra suave.'",
                    " El objeto en la distancia era una reja de metal alta. ",
                    " Sus bordes agudos crearon sombras profundas en el suelo debajo.",
                    " El objeto que colgaba del techo era una candelabro de cristal.",
                    " Su luz proyectaba largas sombras brillantes en las paredes."
                ]
            ],
            "Validation LLM answers": [
                " 1. The object cast a shadow on the ground.\n2. The ball is an object that can be thrown and caught.\n3. The statue in the park is an object of beauty.\n4. The car is an object that requires maintenance.\n5. The rock formation in the desert is an object that has been shaped by erosion over time.",
                [
                    "The object cast a shadow on the ground.",
                    "The ball is an object that can be thrown and caught.",
                    "The statue in the park is an object of beauty.",
                    "The car is an object that requires maintenance.",
                    "The rock formation in the desert is an object that has been shaped by erosion over time."
                ]
            ],
            "Extraction translation": "objeto",
            "Validation translation": "NULL",
            "Correctas": 0,
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 5,
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
            "Mensaje de información": "La entrada ha terminado su ejecución en la fase de validación."
        },
        "eng-30-00006484-n_cell": {
            "Sense index": "2",
            "English gloss": "(biology) the basic structural and functional unit of all organisms; they may exist as independent units of life (as in monads) or may form colonies or tissues as in higher plants and animals.",
            "Spanish gloss": "(biología) la unidad estructural y funcional básica de todas las entidades vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.",
            "Part of speech": "n",
            "Language": "eng",
            "Extraction LLM answers": [
                " 1. The cell is the fundamental building block of all living organisms, providing a protective environment for genetic material and facilitating essential metabolic processes.\n\n2. In multicellular organisms, cells work together to form complex tissues and organs, allowing for specialized functions and coordinated responses to environmental stimuli.\n\n3. The human body contains trillions of cells, each with its own unique set of characteristics and functions, yet all working in harmony to maintain homeostasis and promote overall health.\n\n4. Some organisms, such as bacteria and protists, exist as single cells or colonies of identical cells, known as monads. These unicellular organisms are capable of independent survival and reproduction.\n\n5. In higher plants and animals, cells may form tissues through the process of differentiation, whereby they specialize in specific functions such as photosynthesis, muscle contraction, or nerve condu",
                [
                    " La célula es la unidad estructural y funcional básica de todos los seres vivos, proporcionando un entorno protector para el material genético y facilitando procesos metabólicos esenciales.",
                    " En seres multicelulares, las células trabajan juntas para formar tejidos complejos y órganos, permitiendo funciones especializadas y respuestas coordinadas a estimulaciones ambientales.",
                    " El cuerpo humano contiene trillones de células, cada una con su propio conjunto único de características y funciones, sin embargo, todas trabajan en armonía para mantener la homeostasis y promover la salud global.",
                    " Algunos organismos, como las bacterias y los protistas, existen como células individuales o colonias de células idénticas, conocidas como monadas. Estas unicelulares son capaces de la supervivencia e reproducción independientes.",
                    " En las plantas y animales superiores, las células pueden formar tejidos a través del proceso de diferenciación, en el que se especializan en funciones específicas como la fotosíntesis, la contracción muscular o la conducción nerviosa."
                ]
            ],
            "Validation LLM answers": [
            " 1. La célula es el bloque básico de la vida.\n2. Cada célula tiene su propia estructura y funciones.\n3. Las células cooperan para formar organismos complejos.\n4. En los monadas, las células son unidades independientes.\n5. En los animales superiores, las células forman tejidos complejos.",
                [
                    "La célula es el bloque básico de la vida.",
                    "Cada célula tiene su propia estructura y funciones.",
                    "Las células cooperan para formar organismos complejos.",
                    "En los monadas, las células son unidades independientes.",
                    "En los animales superiores, las células forman tejidos complejos."
                ]
            ],
            "Extraction translation": "célula",
            "Validation translation": "célula",
            "Correctas": 0,
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
            "Mensaje de información": "NULL"
        },
        "eng-30-00007347-n_cause": {
            "Sense index": "4",
            "English gloss": "Any entity that produces an effect or is responsible for events or results.",
            "Spanish gloss": "Cualquier entidad que produce un efecto o es responsable de los eventos o resultados'.",
            "Part of speech": "n",
            "Language": "eng",
            "Extraction LLM answers": [
                " 1. The cause of the accident was a faulty brake system.\n2. The lack of rainfall is the primary cause of the drought.\n3. The cause of the disease outbreak can be traced back to contaminated food.\n4. The cause of the fire was an electrical malfunction in the building's wiring.\n5. The cause of the financial crisis was a combination of factors, including risky investments and lax regulation.",
                [
                    " La causa del accidente fue un sistema de frenos defectuoso.",
                    " La falta de precipitaciones es la causa principal de la sequía.",
                    " La causa de la salida de la enfermedad se puede rastrear hasta el alimento contaminado.",
                    " La causa del incendio fue una falla eléctrica en la instalación eléctrica de los edificios.",
                    " La causa de la crisis financiera fue una combinación de factores, incluyendo inversiones riesgosas y regulación poca."
                ]
            ],
            "Validation LLM answers": [
                " 1) La causa de la epidemia fue una virus mutante.\n2) El cambio climático es la causa principal de la erosión costera.\n3) La falta de educación es la causa principal del desempleo.\n4) La corrupción política es la causa principal de la pérdida de confianza en el gobierno.\n5) El abuso de drogas es la causa principal de la violencia en las calles.",
                [
                    "La causa de la epidemia fue una virus mutante.",
                    "El cambio climático es la causa principal de la erosión costera.",
                    "La falta de educación es la causa principal del desempleo.",
                    "La corrupción política es la causa principal de la pérdida de confianza en el gobierno.",
                    "El abuso de drogas es la causa principal de la violencia en las calles."
                ]
            ],
            "Extraction translation": "causa",
            "Validation translation": "causa",
            "Correctas": 0,
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
            "Mensaje de información": "NULL"
        },
        "eng-30-00007846-n_person": {
            "Sense index": "1",
            "English gloss": "A human being.",
            "Spanish gloss": "Una persona humana'.",
            "Part of speech": "n",
            "Language": "eng",
            "Extraction LLM answers": [
                " 1. The person sitting next to me on the bus is reading a book.\n2. The person who won the race was a professional athlete.\n3. The person I met at the party last night was very friendly.\n4. The person who invented the light bulb changed the world forever.\n5. The person who wrote this article has a degree in linguistics.",
                [
                    " La persona que está sentada al lado mío en el autobús está leyendo un libro.",
                    " La persona que ganó la carrera era un atleta profesional.",
                    " La persona que conocí en la fiesta de anoche era muy amable.",
                    " La persona que inventó la lámpara incandescente cambió el mundo por siempre. ",
                    " La persona que escribió este artículo tiene un grado en lingüística.\n"
                ]
            ],
            "Validation LLM answers": [
                " 1) La persona más importante en mi vida es mi madre.\n2) La persona que me ayudó a superar mis problemas es mi psicólogo.\n3) La persona que inventó la radio fue Guglielmo Marconi.\n4) La persona que ganó el premio Nobel de Química en 2015 fue Ada Yonath.\n5) La persona que escribió \"Hamlet\" es William Shakespeare.",
                [
                    "La persona más importante en mi vida es mi madre.",
                    "La persona que me ayudó a superar mis problemas es mi psicólogo.",
                    "La persona que inventó la radio fue Guglielmo Marconi.",
                    "La persona que ganó el premio Nobel de Química en 2015 fue Ada Yonath.",
                    "La persona que escribió Hamlet es William Shakespeare."
                ]
            ],
            "Extraction translation": "persona",
            "Validation translation": "persona",
            "Correctas": 0,
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
            "Mensaje de información": "NULL"
        },
        "eng-30-00015388-n_animal": {
            "Sense index": "1",
            "English gloss": "A living organism characterized by voluntary movement.",
            "Spanish gloss": "Un ser vivo con movimiento voluntario'.",
            "Part of speech": "n",
            "Language": "eng",
            "Extraction LLM answers": [
                " 1. The lion is an animal that roams the African savannahs in search of prey.\n2. The elephant is the largest land animal and can weigh up to six tons.\n3. The cheetah is a fast-running animal that can reach speeds of over 70 miles per hour.\n4. The gorilla is an endangered animal that lives in dense forests in Central Africa.\n5. The dolphin is a highly intelligent marine mammal that communicates with clicks and whistles.",
                [
                    " El león es un animal que pasea las sabana africanas en busca de presas.",
                    " El elefante es el mayor animal terrestre y puede pesar hasta seis toneladas.",
                    " La guepardo es un animal rápido que puede alcanzar velocidades superiores a los 70 millas por hora.",
                    " El gorila es un animal en peligro de extinción que vive en bosques densos en la región central de África.",
                    " El delfín es un mamífero marino de gran inteligencia que comúnmente se comunica con clics y silbidos."
                ]
            ],
            "Validation LLM answers": [
                " 1. El leopardo es un animal grande y poderoso.\n2. La gacela es un animal rápido y delicado.\n3. El elefante es un animal herbívoro de gran tamaño.\n4. La jirafa es un animal con el cuello muy largo.\n5. El panda rojo es un animal en peligro de extinción.",
                [
                    "El leopardo es un animal grande y poderoso.",
                    "La gacela es un animal rápido y delicado.",
                    "El elefante es un animal herbívoro de gran tamaño.",
                    "La jirafa es un animal con el cuello muy largo.",
                    "El panda rojo es un animal en peligro de extinción."
                ]
            ],
            "Extraction translation": "animal",
            "Validation translation": "animal",
            "Correctas": 0,
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
            "Mensaje de información": "NULL"
        },
        "eng-30-00017222-n_plant": {
            "Sense index": "2",
            "English gloss": "(botany) a living organism lacking the power of locomotion.",
            "Spanish gloss": "(botánica) una entidad viviente que no posee la capacidad de movimiento.",
            "Part of speech": "n",
            "Language": "eng",
            "Extraction LLM answers": [
                " 1. The plant's roots absorb water and nutrients from the soil.\n2. The flowering plant produces beautiful blooms in the spring.\n3. The succulent plant can survive for long periods without water.\n4. The carnivorous plant traps insects to obtain protein.\n5. The parasitic plant attaches itself to a host plant and steals its nutrients.",
                [
                    " Las raíces de las plantas absorben agua y nutrientes del suelo.",
                    " La planta florífera produce hermosas flores en la primavera.",
                    " La planta succulenta puede sobrevivir durante largos periodos sin agua.",
                    " La planta carnívora atrapa insectos para obtener proteína.",
                    " La planta parásita se adhiere a una planta huésped y roba sus nutrientes."
                ]
            ],
            "Validation LLM answers": [
                " 1. La planta de rosas es muy bonita.\n2. El jardín está lleno de plantas exóticas.\n3. Las plantas de cereales se cultivan en gran escala.\n4. La planta de bambú crece rápidamente.\n5. La planta de cactus es muy resistente al calor y a la sequía.",
                [
                    "La planta de rosas es muy bonita.",
                    "El jardín está lleno de plantas exóticas.",
                    "Las plantas de cereales se cultivan en gran escala.",
                    "La planta de bambú crece rápidamente.",
                    "La planta de cactus es muy resistente al calor y a la sequía."
                ]
            ],
            "Extraction translation": "planta",
            "Validation translation": "planta",
            "Correctas": 0,
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
            "Mensaje de información": "NULL"
        },
        "eng-30-00019613-n_substance": {
            "Sense index": "1",
            "English gloss": "The real physical matter of which a person or thing consists.",
            "Spanish gloss": "La materia física real de la que consta una persona o cosa.",
            "Part of speech": "n",
            "Language": "eng",
            "Extraction LLM answers": [
                " 1. The substance of the rock is primarily composed of granite.\n2. The substance of the metal was found to be iron.\n3. The substance of the plant is mostly made up of water and nutrients.\n4. The substance of the human body is a complex mixture of cells, tissues, and organs.\n5. The substance of the diamond is pure carbon in its crystalline form.",
                [
                    " La sustancia de la roca está principalmente compuesta de granito.",
                    " La sustancia del metal fue encontrada ser hierro.",
                    " La sustancia de la planta está principalmente compuesta por agua y nutrientes.",
                    " La sustancia del cuerpo humano es una compleja mezcla de células, tejidos y órganos.",
                    " La sustancia del diamante es carbono puro en su forma cristalina."
                ]
            ],
            "Validation LLM answers": [
                " 1. La sustancia del agua es hidrógeno y oxígeno.\n2. El sustancia del aire está compuesta principalmente por nitrógeno y oxígeno.\n3. La sustancia de la piedra caliza es carbonato de calcio.\n4. El sustancia del metal es un elemento químico.\n5. La sustancia del cuerpo humano está formada por tejidos, huesos, y otros componentes biológicos.",
                [
                    "La sustancia del agua es hidrógeno y oxígeno.",
                    "El sustancia del aire está compuesta principalmente por nitrógeno y oxígeno.",
                    "La sustancia de la piedra caliza es carbonato de calcio.",
                    "El sustancia del metal es un elemento químico.",
                    "La sustancia del cuerpo humano está formada por tejidos, huesos, y otros componentes biológicos."
                ]
            ],
            "Extraction translation": "sustancia",
            "Validation translation": "sustancia",
            "Correctas": 0,
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
            "Mensaje de información": "NULL"
        },
        "eng-30-00020827-n_matter": {
            "Sense index": "3",
            "English gloss": "That which has mass and occupies space.",
            "Spanish gloss": "Eso que tiene masa y ocupa espacio..",
            "Part of speech": "n",
            "Language": "eng",
            "Extraction LLM answers": [
                " 1. The matter in this room is mostly composed of air molecules, but there are also some solid particles like dust and fibers.\n2. The matter that makes up a star is primarily hydrogen gas, which undergoes nuclear fusion to produce energy.\n3. The matter on Earth's surface is mostly made up of rocks, soil, and water, with varying amounts of organic material.\n4. The matter in the universe is not evenly distributed; it forms galaxies, clusters, and superclusters that are separated by vast empty spaces.\n5. The matter in a living organism is constantly being broken down and rebuilt through metabolic processes, which maintain its structure and function over time.",
                [
                    " La materia en esta habitación está principalmente compuesta de moléculas de aire, pero también hay algunas partículas sólidas como polvo y fibras.",
                    " La materia que constituye una estrella es principalmente gas de hidrógeno, el cual sufre fusión nuclear para producir energía.",
                    " La materia en la superficie de los planetas es principalmente compuesta por rocas, tierra y agua, con cantidades variables de materia orgánica.",
                    " La materia en el universo no se distribuye de manera uniforme; forma galaxias, agrupaciones y superagrupaciones que están separadas por espacios vacíos enormes.",
                    " La materia en un organismo vivo se descompone y se reconstruye constantemente a través de procesos metabólicos, que mantienen su estructura y función a lo largo del tiempo."
                ]
            ],
            "Validation LLM answers": [
                " 1. La materia es la sustancia que constituye todo lo visible y tangible del universo.\n2. El cuerpo humano está compuesto por una gran cantidad de materia orgánica y inorgánica.\n3. La materia se divide en tres estados: sólido, líquido y gaseoso.\n4. La materia es la base de todo lo que existe en el universo, desde las rocas más duras hasta los seres vivos más complejos.\n5. El conocimiento de la materia ha sido una preocupación humana desde tiempos antiguos y sigue siendo una prioridad en la investigación científica moderna.",
                [
                    "La materia es la sustancia que constituye todo lo visible y tangible del universo.",
                    "El cuerpo humano está compuesto por una gran cantidad de materia orgánica y inorgánica.",
                    "La materia se divide en tres estados: sólido, líquido y gaseoso.",
                    "La materia es la base de todo lo que existe en el universo, desde las rocas más duras hasta los seres vivos más complejos.",
                    "El conocimiento de la materia ha sido una preocupación humana desde tiempos antiguos y sigue siendo una prioridad en la investigación científica moderna."
                ]
            ],
            "Extraction translation": "materia",
            "Validation translation": "materia",
            "Correctas": 0,
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
            "Mensaje de información": "NULL"
        },
        "eng-30-00021265-n_food": {
            "Sense index": "1",
            "English gloss": "Any substance that can be metabolized by an animal to give energy and build tissue.",
            "Spanish gloss": "Cualquier sustancia que pueda ser metabolizada por un animal para dar energía y construir tejido'.",
            "Part of speech": "n",
            "Language": "eng",
            "Extraction LLM answers": [
                " 1. The food we consume is essential for our survival as it provides us with the necessary nutrients to maintain a healthy body.\n2. The farmer's crops are a vital source of food for his community, ensuring that they have access to nourishing sustenance.\n3. The food industry plays a significant role in the global economy, providing employment opportunities and contributing to economic growth.\n4. The food chain is an essential concept in ecology as it illustrates how energy flows through different organisms, from producers to consumers.\n5. Food insecurity is a major issue affecting millions of people worldwide, with many struggling to access sufficient nutritious food to meet their basic needs.",
                [
                    " La comida que consumimos es fundamental para nuestra supervivencia, ya que proporciona las nutrientes necesarias para mantener un cuerpo saludable.",
                    " Las cosechas de los agricultores son una fuente vital de alimentos para su comunidad, asegurando que tengan acceso a la nutrición necesaria.",
                    " La industria alimentaria desempeña un papel significativo en la economía mundial, proporcionando oportunidades de empleo y contribuyendo al crecimiento económico.",
                    " La cadena alimentaria es un concepto fundamental en la ecología ya que ilustra cómo fluye la energía a través de diferentes organismos, desde los productores hasta los consumidores.",
                    " La inseguridad alimentaria es un problema importante que afecta millones de personas en todo el mundo, con muchas personas luchando para acceder a la cantidad suficiente de comida nutritiva para satisfacer sus necesidades básicas."
                ]
            ],
            "Validation LLM answers": [
                " 1) La comida es una mezcla de nutrientes que los animales necesitan para su supervivencia.\n2) El cuerpo humano necesita comida para obtener la energía y los nutrientes necesarios para funcionar correctamente.\n3) La comida es un producto natural que se consume por los seres vivos para obtener energía y nutrientes.\n4) La comida es una sustancia alimenticia que contiene carbohidratos, proteínas y grasas, necesarias para la salud y el crecimiento de los animales.\n5) La comida es un elemento básico en la dieta de cualquier animal, sin la cual no podría sobrevivir.",
                [
                    "La comida es una mezcla de nutrientes que los animales necesitan para su supervivencia.",
                    "El cuerpo humano necesita comida para obtener la energía y los nutrientes necesarios para funcionar correctamente.",
                    "La comida es un producto natural que se consume por los seres vivos para obtener energía y nutrientes.",
                    "La comida es una sustancia alimenticia que contiene carbohidratos, proteínas y grasas, necesarias para la salud y el crecimiento de los animales.",
                    "La comida es un elemento básico en la dieta de cualquier animal, sin la cual no podría sobrevivir."
                ]
            ],
            "Extraction translation": "comida",
            "Validation translation": "comida",
            "Correctas": 0,
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
            "Mensaje de información": "NULL"
        },
        "eng-30-00023271-n_knowledge": {
            "Sense index": "1",
            "English gloss": "The psychological result of perception and learning and reasoning.",
            "Spanish gloss": "El resultado psicológico de la percepción y el aprendizaje y la razón.",
            "Part of speech": "n",
            "Language": "eng",
            "Extraction LLM answers": [
                " 1. The acquisition of knowledge through reading and research has been a lifelong pursuit for this individual.\n\n2. The accumulation of knowledge over time has led to significant advancements in various fields, such as medicine and technology.\n\n3. Knowledge is the foundation upon which all other skills and abilities are built, making it an essential component of personal growth and development.\n\n4. The dissemination of knowledge through education and communication has been instrumental in shaping societies and cultures throughout history.\n\n5. The pursuit of knowledge for its own sake, rather than for practical applications or financial gain, is a noble and admirable endeavor that has enriched the human experience for centuries.",
                [
                    " La adquisición del conocimiento a través de la lectura y la investigación ha sido una búsqueda vital para esta persona.",
                    " La acumulación del conocimiento a lo largo del tiempo ha llevado a importantes avances en diversas áreas, como la medicina y la tecnología.",
                    " El conocimiento es la base sobre la que se construyen todas las otras habilidades y capacidades, lo que lo convierte en un componente esencial para el crecimiento y desarrollo personal.",
                    " La difusión del conocimiento a través de la educación y la comunicación ha sido fundamental en la conformación de las sociedades y culturas a lo largo de la historia.",
                    " La búsqueda del conocimiento por su propio interés, en lugar de buscar aplicaciones prácticas o ganancias financieras, es una noble y admirable empresa que ha enriquecido la experiencia humana durante siglos."
                ]
            ],
            "Validation LLM answers": [
                " 1. La experiencia educativa ha mejorado su conocimiento sobre la historia.\n2. El estudio científico ha ampliado nuestro conocimiento sobre la biología celular.\n3. Su viaje a Europa le ha dado un conocimiento más profundo de las artes y la cultura.\n4. La investigación médica ha aumentado nuestro conocimiento sobre el tratamiento del cáncer.\n5. El estudio lingüístico ha mejorado nuestra comprensión de la gramática y la sintaxis en inglés.",
                [
                    "La experiencia educativa ha mejorado su conocimiento sobre la historia.",
                    "El estudio científico ha ampliado nuestro conocimiento sobre la biología celular.",
                    "Su viaje a Europa le ha dado un conocimiento más profundo de las artes y la cultura.",
                    "La investigación médica ha aumentado nuestro conocimiento sobre el tratamiento del cáncer.",
                    "El estudio lingüístico ha mejorado nuestra comprensión de la gramática y la sintaxis en inglés."
                ]
            ],
            "Extraction translation": "conocimiento",
            "Validation translation": "conocimiento",
            "Correctas": 0,
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0,
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0,
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0,
            "Mensaje de información": "NULL"
        }
    }
    
    config = ConfigParser()
    config.read('./config.ini')
    
    componenteExporter = ComponenteExporter(config['file_path']['knowledge_table_file_path'])
    
    componenteExporter.export_knowledge(knowledge_table)
    
    # Abrir el archivo en modo lectura
    try:
        with open(config['file_path']['knowledge_table_file_path'], 'r') as archivo:
            # Leer el archivo línea por línea
            for linea in archivo:
                # Comprobar si la línea cumple con los criterios
                if validar_linea(linea):
                    assert True
                else:
                    assert False
    except FileNotFoundError:
        print(f'Archivo "{config["file_path"]["knowledge_table_file_path"]}" no encontrado. Vuelve a introducir una nueva ruta')
        
def validar_linea(linea):
    # Patrón de expresión regular para verificar cada elemento de la línea
    patron = r'^"eng-30-\d{8}-n", "[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+", "\d+", ".+", "n", "spa", "[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+", "------",$'
    # Comprobar si la línea coincide con el patrón
    if re.match(patron, linea.strip()):
        return True
    else:
        return False
    
def auxiliar_functions_test():
    
    # -----------------------------------   destokenize()   ---------------------------------------
    
    print('Testing destokenize() function')
    
    tokens = []
    new_tokens = []
    assert "" == auxFunctions.destokenize(tokens, new_tokens), "Should be ''"
    
    tokens_2 = ['Hola',',','soy','David''.']
    new_tokens_2 = ['Hola',',','soy','David''.']
    assert "Hola, soy David." == auxFunctions.destokenize(tokens_2, new_tokens_2), "Should be 'Hola, soy David.'"
    
    tokens_3 = ['Hola',',','soy','David''.']
    new_tokens_3 = ['Hola',',','soy']
    assert "Hola, soy" == auxFunctions.destokenize(tokens_3, new_tokens_3), "Should be 'Hola, soy David.'"
    
    print('destokenize() function tested correctly') 
    
    # -----------------------------------   extract_nouns_with_positions_english()   ---------------------------------------
    
    print('Testing extract_nouns_with_positions_english() function')
    
    phrase_1 = "The towering oak tree provided shade for the picnic on a hot summer day."
    expected_output_1 = [('tree', 3), ('shade', 5), ('picnic', 8), ('day', 13)]
    assert expected_output_1 == auxFunctions.extract_nouns_with_positions_english(phrase_1), "Should be true"
    
    phrase_2 = "The largest tree in the forest is an american oak, which is over 30 meters tall."
    expected_output_2 = [('tree', 2), ('forest', 5), ('oak', 9), ('meters', 15)]
    assert expected_output_2 == auxFunctions.extract_nouns_with_positions_english(phrase_2), "Should be true"
    
    phrase_3 = "The paper was smooth and glossy, perfect for printing high-quality images."
    expected_output_3 = [('paper', 1), ('images', 13)]
    assert expected_output_3 == auxFunctions.extract_nouns_with_positions_english(phrase_3), "Should be true"
    
    phrase_4 = ""
    expected_output_4 = []
    assert expected_output_4 == auxFunctions.extract_nouns_with_positions_english(phrase_4), "Should be true"
    
    print('extract_nouns_with_positions_english() function tested correctly') 
    
    # -----------------------------------   extract_nouns_with_positions_spanish()   ---------------------------------------
    
    print('Testing extract_nouns_with_positions_spanish() function')
    
    phrase_5 = "La fábrica de papel había estado en funcionamiento durante más de un siglo, proporcionando oportunidades de empleo a Generaciónes de familias en la zona."
    expected_output_5 = [('fábrica', 1), ('papel', 3), ('funcionamiento', 7), ('siglo', 12), ('oportunidades', 15), ('empleo', 17), ('generaciones', 19), ('familias', 21), ('zona', 24)]
    assert expected_output_5 == auxFunctions.extract_nouns_with_positions_spanish(phrase_5), "Should be true"

    phrase_6 = "El papel es un material muy utilizado para la impresión y la escritura."
    expected_output_6 = [('papel', 1), ('material', 4), ('impresión', 9), ('escritura', 12)]
    assert expected_output_6 == auxFunctions.extract_nouns_with_positions_spanish(phrase_6), "Should be true"
  
    phrase_7 = "El árbol más grande del bosque es un roble americano de más de 30 metros de altura."
    expected_output_7 = [('árbol', 1), ('metros', 14), ('altura', 16)]
    assert expected_output_7 == auxFunctions.extract_nouns_with_positions_spanish(phrase_7), "Should be true"

    phrase_8 = ""
    expected_output_8 = []
    assert expected_output_8 == auxFunctions.extract_nouns_with_positions_spanish(phrase_8), "Should be true"
    
    print('extract_nouns_with_positions_spanish() function tested correctly') 
    
    # -----------------------------------   pluralize_word_english()   ---------------------------------------
    
    print('Testing pluralize_word_english() function')
    
    eng_word_1 = "apple"
    expected_eng_word_1 = ['apple', 'apples']
    assert expected_eng_word_1 == auxFunctions.pluralize_word_english(eng_word_1), "Should be true"

    eng_word_2 = "book"
    expected_eng_word_2 = ['book', 'books']
    assert expected_eng_word_2 == auxFunctions.pluralize_word_english(eng_word_2), "Should be true"

    eng_word_3 = "car"
    expected_eng_word_3 = ['car', 'cars']
    assert expected_eng_word_3 == auxFunctions.pluralize_word_english(eng_word_3), "Should be true"

    eng_word_4 = "dog"
    expected_eng_word_4 = ['dog', 'dogs']
    assert expected_eng_word_4 == auxFunctions.pluralize_word_english(eng_word_4), "Should be true"

    eng_word_5 = "cat"
    expected_eng_word_5 = ['cat', 'cats']
    assert expected_eng_word_5 == auxFunctions.pluralize_word_english(eng_word_5), "Should be true"

    eng_word_6 = "house"
    expected_eng_word_6 = ['house', 'houses']
    assert expected_eng_word_6 == auxFunctions.pluralize_word_english(eng_word_6), "Should be true"

    eng_word_7 = "tree"
    expected_eng_word_7 = ['tree', 'trees']
    assert expected_eng_word_7 == auxFunctions.pluralize_word_english(eng_word_7), "Should be true"

    eng_word_8 = "child"
    expected_eng_word_8 = ['child', 'children']
    assert expected_eng_word_8 == auxFunctions.pluralize_word_english(eng_word_8), "Should be true"

    eng_word_9 = "foot"
    expected_eng_word_9 = ['foot', 'feet']
    assert expected_eng_word_9 == auxFunctions.pluralize_word_english(eng_word_9), "Should be true"

    eng_word_10 = "tooth"
    expected_eng_word_10 = ['tooth', 'teeth']
    assert expected_eng_word_10 == auxFunctions.pluralize_word_english(eng_word_10), "Should be true"

    eng_word_11 = "mouse"
    expected_eng_word_11 = ['mouse', 'mice']
    assert expected_eng_word_11 == auxFunctions.pluralize_word_english(eng_word_11), "Should be true"

    eng_word_12 = "woman"
    expected_eng_word_12 = ['woman', 'women']
    assert expected_eng_word_12 == auxFunctions.pluralize_word_english(eng_word_12), "Should be true"

    eng_word_13 = "man"
    expected_eng_word_13 = ['man', 'men']
    assert expected_eng_word_13 == auxFunctions.pluralize_word_english(eng_word_13), "Should be true"

    eng_word_14 = "person"
    expected_eng_word_14 = ['person', 'people']
    assert expected_eng_word_14 == auxFunctions.pluralize_word_english(eng_word_14), "Should be true"

    eng_word_15 = "goose"
    expected_eng_word_15 = ['goose', 'geese']
    assert expected_eng_word_15 == auxFunctions.pluralize_word_english(eng_word_15), "Should be true"

    eng_word_16 = "fish"
    expected_eng_word_16 = ['fish']
    assert expected_eng_word_16 == auxFunctions.pluralize_word_english(eng_word_16), "Should be true"

    eng_word_17 = "sheep"
    expected_eng_word_17 = ['sheep']
    assert expected_eng_word_17 == auxFunctions.pluralize_word_english(eng_word_17), "Should be true"

    eng_word_18 = "city"
    expected_eng_word_18 = ['city', 'cities']
    assert expected_eng_word_18 == auxFunctions.pluralize_word_english(eng_word_18), "Should be true"

    eng_word_19 = "baby"
    expected_eng_word_19 = ['baby', 'babies']
    assert expected_eng_word_19 == auxFunctions.pluralize_word_english(eng_word_19), "Should be true"

    eng_word_20 = "knife"
    expected_eng_word_20 = ['knife', 'knives']
    assert expected_eng_word_20 == auxFunctions.pluralize_word_english(eng_word_20), "Should be true"

    eng_word_21 = "leaf"
    expected_eng_word_21 = ['leaf', 'leaves']
    assert expected_eng_word_21 == auxFunctions.pluralize_word_english(eng_word_21), "Should be true"

    eng_word_22 = "wife"
    expected_eng_word_22 = ['wife', 'wives']
    assert expected_eng_word_22 == auxFunctions.pluralize_word_english(eng_word_22), "Should be true"

    eng_word_23 = "life"
    expected_eng_word_23 = ['life', 'lives']
    assert expected_eng_word_23 == auxFunctions.pluralize_word_english(eng_word_23), "Should be true"

    eng_word_24 = "half"
    expected_eng_word_24 = ['half', 'halves']
    assert expected_eng_word_24 == auxFunctions.pluralize_word_english(eng_word_24), "Should be true"

    eng_word_25 = "loaf"
    expected_eng_word_25 = ['loaf', 'loaves']
    assert expected_eng_word_25 == auxFunctions.pluralize_word_english(eng_word_25), "Should be true"

    eng_word_26 = "cactus"
    expected_eng_word_26 = ['cactus', 'cacti']
    assert expected_eng_word_26 == auxFunctions.pluralize_word_english(eng_word_26), "Should be true"

    eng_word_27 = "phenomenon"
    expected_eng_word_27 = ['phenomenon', 'phenomena']
    assert expected_eng_word_27 == auxFunctions.pluralize_word_english(eng_word_27), "Should be true"

    eng_word_28 = "analysis"
    expected_eng_word_28 = ['analysis', 'analyses']
    assert expected_eng_word_28 == auxFunctions.pluralize_word_english(eng_word_28), "Should be true"

    eng_word_29 = "thesis"
    expected_eng_word_29 = ['thesis', 'theses']
    assert expected_eng_word_29 == auxFunctions.pluralize_word_english(eng_word_29), "Should be true"

    eng_word_30 = "datum"
    expected_eng_word_30 = ['datum', 'data']
    assert expected_eng_word_30 == auxFunctions.pluralize_word_english(eng_word_30), "Should be true"

    print('pluralize_word_english() function tested correctly') 
    
    # -----------------------------------   pluralize_word_spanish()   ---------------------------------------
    
    print('Testing pluralize_word_spanish() function')
    
    # Primer conjunto de palabras en español
    spanish_words_1 = "casa"
    expected_spanish_words_1 = ['casa', 'casas']
    assert expected_spanish_words_1 == auxFunctions.pluralize_word_spanish(spanish_words_1), "Should be true"

    # Segundo conjunto de palabras en español
    spanish_words_2 = "perro"
    expected_spanish_words_2 = ['perro', 'perros']
    assert expected_spanish_words_2 == auxFunctions.pluralize_word_spanish(spanish_words_2), "Should be true"

    # Tercer conjunto de palabras en español
    spanish_words_3 = "gato"
    expected_spanish_words_3 = ['gato', 'gatos']
    assert expected_spanish_words_3 == auxFunctions.pluralize_word_spanish(spanish_words_3), "Should be true"

    # Cuarto conjunto de palabras en español
    spanish_words_4 = "libro"
    expected_spanish_words_4 = ['libro', 'libros']
    assert expected_spanish_words_4 == auxFunctions.pluralize_word_spanish(spanish_words_4), "Should be true"

    # Quinto conjunto de palabras en español
    spanish_words_5 = "mesa"
    expected_spanish_words_5 = ['mesa', 'mesas']
    assert expected_spanish_words_5 == auxFunctions.pluralize_word_spanish(spanish_words_5), "Should be true"

    # Sexto conjunto de palabras en español
    spanish_words_6 = "flor"
    expected_spanish_words_6 = ['flor', 'flores']
    assert expected_spanish_words_6 == auxFunctions.pluralize_word_spanish(spanish_words_6), "Should be true"

    # Séptimo conjunto de palabras en español
    spanish_words_7 = "niño"
    expected_spanish_words_7 = ['niño', 'niños']
    assert expected_spanish_words_7 == auxFunctions.pluralize_word_spanish(spanish_words_7), "Should be true"

    # Octavo conjunto de palabras en español
    spanish_words_8 = "mujer"
    expected_spanish_words_8 = ['mujer', 'mujeres']
    assert expected_spanish_words_8 == auxFunctions.pluralize_word_spanish(spanish_words_8), "Should be true"

    # Noveno conjunto de palabras en español
    spanish_words_9 = "hombre"
    expected_spanish_words_9 = ['hombre', 'hombres']
    assert expected_spanish_words_9 == auxFunctions.pluralize_word_spanish(spanish_words_9), "Should be true"

    # Décimo conjunto de palabras en español
    spanish_words_10 = "juego"
    expected_spanish_words_10 = ['juego', 'juegos']
    assert expected_spanish_words_10 == auxFunctions.pluralize_word_spanish(spanish_words_10), "Should be true"

    # Undécimo conjunto de palabras en español
    spanish_words_11 = "pelota"
    expected_spanish_words_11 = ['pelota', 'pelotas']
    assert expected_spanish_words_11 == auxFunctions.pluralize_word_spanish(spanish_words_11), "Should be true"

    # Duodécimo conjunto de palabras en español
    spanish_words_12 = "árbol"
    expected_spanish_words_12 = ['árbol', 'árboles']
    assert expected_spanish_words_12 == auxFunctions.pluralize_word_spanish(spanish_words_12), "Should be true"

    # Decimotercer conjunto de palabras en español
    spanish_words_13 = "coche"
    expected_spanish_words_13 = ['coche', 'coches']
    assert expected_spanish_words_13 == auxFunctions.pluralize_word_spanish(spanish_words_13), "Should be true"

    # Decimocuarto conjunto de palabras en español
    spanish_words_14 = "manzana"
    expected_spanish_words_14 = ['manzana', 'manzanas']
    assert expected_spanish_words_14 == auxFunctions.pluralize_word_spanish(spanish_words_14), "Should be true"

    # Decimoquinto conjunto de palabras en español
    spanish_words_15 = "camino"
    expected_spanish_words_15 = ['camino', 'caminos']
    assert expected_spanish_words_15 == auxFunctions.pluralize_word_spanish(spanish_words_15), "Should be true"

    # Decimosexto conjunto de palabras en español
    spanish_words_16 = "hijo"
    expected_spanish_words_16 = ['hijo', 'hijos']
    assert expected_spanish_words_16 == auxFunctions.pluralize_word_spanish(spanish_words_16), "Should be true"

    # Decimoséptimo conjunto de palabras en español
    spanish_words_17 = "ciudad"
    expected_spanish_words_17 = ['ciudad', 'ciudades']
    assert expected_spanish_words_17 == auxFunctions.pluralize_word_spanish(spanish_words_17), "Should be true"

    # Decimoctavo conjunto de palabras en español
    spanish_words_18 = "animal"
    expected_spanish_words_18 = ['animal', 'animales']
    assert expected_spanish_words_18 == auxFunctions.pluralize_word_spanish(spanish_words_18), "Should be true"

    # Decimonoveno conjunto de palabras en español
    spanish_words_19 = "reloj"
    expected_spanish_words_19 = ['reloj', 'relojes']
    assert expected_spanish_words_19 == auxFunctions.pluralize_word_spanish(spanish_words_19), "Should be true"

    # Vigésimo conjunto de palabras en español
    spanish_words_20 = "luz"
    expected_spanish_words_20 = ['luz', 'luces']
    assert expected_spanish_words_20 == auxFunctions.pluralize_word_spanish(spanish_words_20), "Should be true"

    # Vigésimo primer conjunto de palabras en español
    spanish_words_21 = "rey"
    expected_spanish_words_21 = ['rey', 'reyes']
    assert expected_spanish_words_21 == auxFunctions.pluralize_word_spanish(spanish_words_21), "Should be true"

    # Vigésimo segundo conjunto de palabras en español
    spanish_words_22 = "cielo"
    expected_spanish_words_22 = ['cielo', 'cielos']
    assert expected_spanish_words_22 == auxFunctions.pluralize_word_spanish(spanish_words_22), "Should be true"

    # Vigésimo tercer conjunto de palabras en español
    spanish_words_23 = "flor"
    expected_spanish_words_23 = ['flor', 'flores']
    assert expected_spanish_words_23 == auxFunctions.pluralize_word_spanish(spanish_words_23), "Should be true"

    # Vigésimo cuarto conjunto de palabras en español
    spanish_words_24 = "café"
    expected_spanish_words_24 = ['café', 'cafés']
    assert expected_spanish_words_24 == auxFunctions.pluralize_word_spanish(spanish_words_24), "Should be true"
    
    # Vigésimo quinto conjunto de palabras en español
    spanish_words_25 = "voz"
    expected_spanish_words_25 = ['voz', 'voces']
    assert expected_spanish_words_25 == auxFunctions.pluralize_word_spanish(spanish_words_25), "Should be true"
    
    print('pluralize_word_spanish() function tested correctly') 
    
    # -----------------------------------   normalize_list_english()   ---------------------------------------
    
    print('Testing normalize_list_english() function')
    
    element_transfer = [('transferring', 2), ('transfer', 3)]
    assert [('transferring', 2), ('transfer', 3)] == auxFunctions.normalize_list_english(element_transfer), "Should be true"
    
    element_agriculture = [('agriculture', 4), ('agricultures',1)]
    assert [('agriculture', 5)] == auxFunctions.normalize_list_english(element_agriculture), "Should be true"
    
    element_protection = [('protection', 5)]
    assert [('protection', 5)] == auxFunctions.normalize_list_english(element_protection), "Should be true"
    
    print('normalize_list_english() function tested correctly') 
    
    # -----------------------------------   normalize_list_spanish()   ---------------------------------------
    
    print('Testing normalize_list_spanish() function')
    
    element_compra = [('comprando', 1), ('compras', 1), ('compra', 1)]
    assert [('comprando', 1), ('compra', 2)] == auxFunctions.normalize_list_english(element_compra), "Should be true"
    
    element_agricultura = [('agricultura', 4), ('agriculturas',1)]
    assert [('agricultura', 5)] == auxFunctions.normalize_list_english(element_agricultura), "Should be true"
    
    element_proteccion = [('protección', 2)]
    assert [('protección', 2)] == auxFunctions.normalize_list_english(element_proteccion), "Should be true"
    
    print('normalize_list_spanish() function tested correctly') 
    
    # -----------------------------------   find_element_with_difference()   ---------------------------------------
    
    print('Testing find_element_with_difference() function')
    
    assert ('agricultura', 5) == auxFunctions.find_element_with_difference([('agricultura', 5)],1)
    assert ('agricultura', 5) == auxFunctions.find_element_with_difference([('agricultura', 5)],2)
    assert ('agricultura', 5) == auxFunctions.find_element_with_difference([('agricultura', 5)],3)
    assert ('agricultura', 5) == auxFunctions.find_element_with_difference([('agricultura', 5)],4)
    assert ('agricultura', 5) == auxFunctions.find_element_with_difference([('agricultura', 5)],5)
    assert [] == auxFunctions.find_element_with_difference([('agricultura', 5)],6)
    
    assert ('compra', 2) == auxFunctions.find_element_with_difference([('comprando', 1), ('compra', 2)],1)
    assert ('compra', 2) == auxFunctions.find_element_with_difference([('comprando', 1), ('compra', 2)],2)
    
    assert ('transfer', 3) == auxFunctions.find_element_with_difference([('transferring', 2), ('transfer', 3)],1)
    assert ('transfer', 3) == auxFunctions.find_element_with_difference([('transferring', 2), ('transfer', 3)],2)
    
    print('find_element_with_difference() function tested correctly')
    
    # -----------------------------------   is_possessive()   ---------------------------------------
    
    print('Testing is_possessive() function')
    
    # Primer conjunto de palabras en inglés
    tokens_1 = ["John", "'", "s", "book"]
    index_1 = 0
    expected_1 = True
    assert expected_1 == auxFunctions.is_possessive(tokens_1, index_1), "Test 1 failed"

    # Segundo conjunto de palabras en inglés
    tokens_2 = ["The", "cat", "'", "s", "tail"]
    index_2 = 1
    expected_2 = False
    assert expected_2 == auxFunctions.is_possessive(tokens_2, index_2), "Test 2 failed"

    # Tercer conjunto de palabras en inglés
    tokens_3 = ["This", "is", "Sarah", "'", "s", "pen"]
    index_3 = 2
    expected_3 = True
    assert expected_3 == auxFunctions.is_possessive(tokens_3, index_3), "Test 3 failed"

    # Cuarto conjunto de palabras en inglés
    tokens_4 = ["This", "is", "the", "book"]
    index_4 = 2
    expected_4 = False
    assert expected_4 == auxFunctions.is_possessive(tokens_4, index_4), "Test 4 failed"

    # Quinto conjunto de palabras en inglés
    tokens_5 = ["The", "dogs", "are", "playing"]
    index_5 = 1
    expected_5 = False
    assert expected_5 == auxFunctions.is_possessive(tokens_5, index_5), "Test 5 failed"

    print('is_possessive() function tested correctly')
    
    
    # -----------------------------------   extract_llm_answers_set_of_phrases()   ---------------------------------------
    
    print('Testing extract_llm_answers_set_of_phrases() function')
    
    elemento_prueba_piloto_masculino = "\n1. El gran desafío que enfrenta la tierra es combatir la erosión y mantener su fertilidad.\n2. La tierra está siendo devastada por los cambios climáticos y la deforestación.\n3. La tierra necesita que los humanos cambien su manera de pensar y actuar para protegerla.\n4. El hombre ha estado explotando y devastando la tierra durante siglos.\n5. La tierra ha sido la fuente de vida y prosperidad para millones de personas durante milenios.\n6. La tierra es un recurso limitado que necesita ser utilizado y preservado con cuidado.\n7. La tierra es un regalo de la naturaleza que ha sido y seguirá siendo vital para la supervivencia humana.\n8. La tierra es más que un lugar, es un sistema complejo que afecta a todas las formas de vida.\n9. La tierra es la fuente de todos los recursos que necesitamos para sobrevivir y prosperar.\n10. La tierra es un legado que debemos preservar para las Generaciónes futuras."

    expected_output_piloto_masculino = ["El gran desafío que enfrenta la tierra es combatir la erosión y mantener su fertilidad.",
                              "La tierra está siendo devastada por los cambios climáticos y la deforestación.",
                              "La tierra necesita que los humanos cambien su manera de pensar y actuar para protegerla.",
                              "El hombre ha estado explotando y devastando la tierra durante siglos.",
                              "La tierra ha sido la fuente de vida y prosperidad para millones de personas durante milenios.",
                              "La tierra es un recurso limitado que necesita ser utilizado y preservado con cuidado.",
                              "La tierra es un regalo de la naturaleza que ha sido y seguirá siendo vital para la supervivencia humana.",
                              "La tierra es más que un lugar, es un sistema complejo que afecta a todas las formas de vida.",
                              "La tierra es la fuente de todos los recursos que necesitamos para sobrevivir y prosperar.",
                              "La tierra es un legado que debemos preservar para las Generaciónes futuras."]
    
    assert expected_output_piloto_masculino == auxFunctions.extract_llm_answers_set_of_phrases(elemento_prueba_piloto_masculino), "Should be true"
    
    elemento_prueba_piloto_femenino = "1. La tierra es una madre generosa que nos da sustento. 2. La tierra es una hermosa dama que necesita nuestra atención y amor. 3. La tierra es una piel que nos cubre y protege. 4. La tierra es una madre que nos guía y nos da vida. 5. La tierra es una madre que nos da alimentos y agua. 6. La tierra es una madre que nos da un lugar en la que vivir y crecer. 7. La tierra es una madre que nos da un hogar y una casa. 8. La tierra es una madre que nos da un lugar en la que compartir nuestras vidas. 9. La tierra es una madre que nos da un lugar en la que vivir y crecer juntos. 10. La tierra es una madre que nos da una oportunidad de crecer y desarrollarnos."

    expected_output_piloto_femenino = ["La tierra es una madre generosa que nos da sustento.",
                                       "La tierra es una hermosa dama que necesita nuestra atención y amor.",
                                       "La tierra es una piel que nos cubre y protege.",
                                       "La tierra es una madre que nos guía y nos da vida.",
                                       "La tierra es una madre que nos da alimentos y agua.",
                                       "La tierra es una madre que nos da un lugar en la que vivir y crecer.",
                                       "La tierra es una madre que nos da un hogar y una casa.",
                                       "La tierra es una madre que nos da un lugar en la que compartir nuestras vidas.",
                                       "La tierra es una madre que nos da un lugar en la que vivir y crecer juntos.",
                                       "La tierra es una madre que nos da una oportunidad de crecer y desarrollarnos."]
    
    assert expected_output_piloto_femenino == auxFunctions.extract_llm_answers_set_of_phrases(elemento_prueba_piloto_femenino), "Should be true"
    
    print('extract_llm_answers_set_of_phrases() function tested correctly')
    
    # -----------------------------------   extract_llm_answers_translation()   ---------------------------------------
    
    print('Testing extract_llm_answers_translation() function')
    
    elemento_prueba_piloto = "Alguien que posee una licencia para operar un avión en vuelo."

    expected_output_piloto = "Alguien que posee una licencia para operar un avión en vuelo."
    assert expected_output_piloto == auxFunctions.extract_llm_answers_translation(elemento_prueba_piloto), "Should be true"

    elemento_prueba_accion = "'una acción'\n\n"

    expected_output_accion = "Una acción."
    assert expected_output_accion == auxFunctions.extract_llm_answers_translation(elemento_prueba_accion), "Should be true"

    print('extract_llm_answers_translation() function tested correctly') 
    
# Método main
if __name__ == "__main__":
    print("Test started: second pilot case")
    print("Testing over Importer component...")
    component_importer_test() # Tested correctly
    print("Everything in Importer component passed")
    print("Testing over Question Maker traduccion glosa component...")
    component_question_maker_traduccion_glosa_test() # Tested correctly
    print("Everything in Question Maker traduccion glosa  component passed")
    print("Testing over Question Maker traduccion inglés español component...")
    component_question_maker_traduccion_ingles_español_test() # Tested correctly
    print("Everything in Question Maker traduccion inglés español component passed")
    print("Testing over Question Maker traduccion español inglés component...")
    component_question_maker_traduccion_español_ingles_test() # Tested correctly
    print("Everything in Question Maker traduccion español inglés component passed")
    print("Testing over Question Maker extraccion component...")
    component_question_maker_extraccion_test() # Tested correctly
    print("Everything in Question Maker extraccion component passed")
    print("Testing over Question Maker validacion component...")
    component_question_maker_validacion_test() # Tested correctly
    print("Everything in Question Maker validacion component passed")
    print("Testing over LLM Communicator component...")
    component_llm_communicator_test() # Tested correctly
    print("Everything in LLM Communicator component passed")
    print("Testing over Extractor translation component...")
    component_extractor_translation_test() # Tested correctly
    print("Everything in Extractor translation component passed")
    print("Testing over Extractor set of phrases component...")
    component_extractor_set_of_phrases_test() # Tested correctly
    print("Everything in Extractor  set of phrases component passed")
    print("Testing over Extractor extraccion component...")
    component_extractor_extraccion_test() # Tested correctly
    print("Everything in Extractor extraccion component passed")
    print("Testing over Extractor validacion component...")
    component_extractor_validacion_test() # Tested correctly
    print("Everything in Extractor validacion component passed")
    print("Testing over Exporter component...")
    component_exporter_test() # Tested correctly
    print("Everything in Exporter component passed")
    print("Testing over Auxiliar funcitions...")
    auxiliar_functions_test() # Tested correctly
    print("Everything in Auxiliar funcitions passed")
    print("Everything passed")