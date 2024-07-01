

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
import componenteExtractor_faseExtraccion
import componenteExtractor_conjuntoFrases
import componenteExtractor_traduccion
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
    element_paper = ("eng-30-14974264-n_paper", ["1","A material made of cellulose pulp derived mainly from wood or rags or certain grasses.","n","eng"])
    assert (element_paper[0], element_paper[1]) in knowledge_table.items(), "Should appear"
    
    # Elemento que debe contener el knowledge_table
    element_year = ("eng-30-15203791-n_year", ["1","A period of time containing 365 (or 366) days.","n","eng"])
    assert (element_year[0], element_year[1]) in knowledge_table.items(), "Should appear"
    
    # print the output
    # print(json.dumps(knowledge_table, indent=2, ensure_ascii=False))
    
    
def component_question_maker_traduccion_glosa_test():
     
    # Elementos de prueba
    element_paper = ("eng-30-14974264-n_paper", ["1","A material made of cellulose pulp derived mainly from wood or rags or certain grasses.","n","eng"])
    element_year = ("eng-30-15203791-n_year", ["1","A period of time containing 365 (or 366) days.","n","eng"])
    
    prompts_paper = componenteQuestionMaker_traduccionGlosa.generate_prompts(element_paper)
    prompts_year = componenteQuestionMaker_traduccionGlosa.generate_prompts(element_year)
    
    assert prompts_paper == ["As a translation expert, I need an accurate translation into Spanish of the following phrase: 'A material made of cellulose pulp derived mainly from wood or rags or certain grasses.'."], "Shold be true"
    assert prompts_year == ["As a translation expert, I need an accurate translation into Spanish of the following phrase: 'A period of time containing 365 (or 366) days.'."], "Shold be true"
 
def component_question_maker_traduccion_ingles_español_test():
     
    # Elementos de prueba
    element_plant = ("eng-30-00017222-n_plant", [
        "2",
        "(botany) a living organism lacking the power of locomotion.",
        "n",
        "eng",
        [
            " 1. The plant, with its green leaves and sturdy stem, stood tall amidst the barren landscape.\n2. The botanist carefully examined the plant's intricate structure, noting the arrangement of its roots and branches.\n3. The plant's delicate petals opened to reveal a vibrant array of colors, attracting bees and butterflies alike.\n4. The plant's leaves, once lush and green, now wilted under the scorching sun, a victim of drought and neglect.\n5. The plant's seeds, carefully nurtured in the soil, sprouted into a new life, a testament to the power of nature and the cycle of life.",
            [
                "The plant, with its green leaves and sturdy stem, stood tall amidst the barren landscape.",
                "The botanist carefully examined the plant's intricate structure, noting the arrangement of its roots and branches.",
                "The plant's delicate petals opened to reveal a vibrant array of colors, attracting bees and butterflies alike.",
                "The plant's leaves, once lush and green, now wilted under the scorching sun, a victim of drought and neglect.",
                "The plant's seeds, carefully nurtured in the soil, sprouted into a new life, a testament to the power of nature and the cycle of life."
            ]
        ]
    ])
    
    elemet_substance = ("eng-30-00019613-n_substance", [
        "1",
        "The real physical matter of which a person or thing consists.",
        "n",
        "eng",
        [
            " 1. The substance of the rock is primarily composed of granite.\n2. The chemical substance of water is H2O.\n3. The substance of the human body is made up of various organs and tissues.\n4. The substance of the diamond is carbon, arranged in a crystalline structure.\n5. The substance of the air we breathe is primarily composed of nitrogen, oxygen, and trace amounts of other gases.",
            [
                "The substance of the rock is primarily composed of granite.",
                "The chemical substance of water is H2O.",
                "The substance of the human body is made up of various organs and tissues.",
                "The substance of the diamond is carbon, arranged in a crystalline structure.",
                "The substance of the air we breathe is primarily composed of nitrogen, oxygen, and trace amounts of other gases."
            ]
        ]
    ])
    
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
    
def component_question_maker_traduccion_españolingles_test():
    
    # Elementos de prueba
    elemet_animal = ("eng-30-00015388-n_animal", [
        "1",
        "A living organism characterized by voluntary movement.",
        "Un ser vivo con capacidad de movimiento voluntario.",
        "n",
        "eng",
        [
            " 1. The lion is a majestic animal that roams the African savannah.\n2. The elephant is the largest land animal and can weigh up to six tons.\n3. The cheetah is the fastest animal on land, capable of reaching speeds of over 70 miles per hour.\n4. The monkey is a primate animal that lives in trees and has opposable thumbs.\n5. The shark is a predatory animal that inhabits oceans around the world and can grow up to 30 feet long.",
            [
                " El león es un animal majestuoso que pasea por las praderas africanas.",
                " El elefante es el mayor animal terrestre y puede pesar hasta seis toneladas.",
                " La gueparda es el animal más rápido en tierra, capaz de alcanzar velocidades superiores a los 110 km/h.",
                " El mono es un animal primate que vive en árboles y tiene dedos opuestos.",
                " El tiburón es un animal depredador que habita los océanos en todo el mundo y puede alcanzar una longitud de hasta 30 pies."
            ]
        ],
        "animal",
        [
            " 1. El leopardo es un animal grande y poderoso.\n2. La jirafa es un animal herbívoro que puede alcanzar alturas de hasta 5,5 metros.\n3. El elefante es un animal inteligente y social que vive en grupos.\n4. El tigre es un animal carnívoro que habita en las selvas tropicales.\n5. La ballena es un animal marino gigante que puede pesar hasta 180 toneladas.",
            [
               "El leopardo es un animal grande y poderoso.",
               "La jirafa es un animal herbívoro que puede alcanzar alturas de hasta 5,5 metros.",
               "El elefante es un animal inteligente y social que vive en grupos.",
               "El tigre es un animal carnívoro que habita en las selvas tropicales.",
               "La ballena es un animal marino gigante que puede pesar hasta 180 toneladas."
            ]
        ]
    ])
    
    element_cell = ("eng-30-00006484-n_cell", [
        "2",
        "(biology) the basic structural and functional unit of all organisms; they may exist as independent units of life (as in monads) or may form colonies or tissues as in higher plants and animals.",
        "(biología) la unidad estructural y funcional básica de todas las organizaciones vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.",
        "n",
        "eng",
        [
            " 1. The cell is a fundamental building block of all living organisms, providing structure and facilitating essential biological processes.\n2. In multicellular organisms, cells work together to form complex tissues and organs that enable the organism to carry out its functions.\n3. Cells are capable of reproducing through binary fission or other means, allowing for growth and development in both unicellular and multicellular organisms.\n4. The cell membrane is a crucial component of the cell, regulating the exchange of materials between the cell and its environment.\n5. Cells contain various organelles that perform specific functions, such as the mitochondria which generate energy through cellular respiration or the chloroplasts in plant cells that carry out photosynthesis.",
            [
                " La célula es el bloque básico de construcción fundamental en todas las entidades vivientes, proporcionando estructura y facilitando procesos biológicos esenciales.",
                " En los seres multicelulares, las células trabajan juntas para formar tejidos y órganos complejos que permiten al organismo llevar a cabo sus funciones.",
                " Las células son capaces de reproducirse a través de la fisión binaria o otros medios, lo que permite el crecimiento y el desarrollo tanto en organismos unicelulares como en multicelulares.",
                " La membrana celular es un componente crucial de la célula, regulando el intercambio de materiales entre la célula y su entorno.",
                " Las células contienen varias organelas que realizan funciones específicas, como las mitocondrias que generan energía a través de la respiración celular o los cloroplastos en las células vegetales que llevan a cabo la fotosíntesis."
            ]
        ],
        "célula",
        [
            " 1. Las células son el bloque básico de la vida.\n2. La división celular es un proceso fundamental para la reproducción y el crecimiento.\n3. Cada célula contiene una copia completa del ADN, pero solo una pequeña parte se expresa en cualquier momento.\n4. Las células especializadas tienen funciones específicas en los organismos multicelulares.\n5. La investigación de las células ha revelado muchas verdades sobre la biología y la medicina.",
            [
                "Las células son el bloque básico de la vida.",
                "La división celular es un proceso fundamental para la reproducción y el crecimiento.",
                "Cada célula contiene una copia completa del ADN, pero solo una pequeña parte se expresa en cualquier momento.",
                "Las células especializadas tienen funciones específicas en los organismos multicelulares.",
                "La investigación de las células ha revelado muchas verdades sobre la biología y la medicina."
            ]
        ],
        "célula"
    ])
    
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
    element_paper = ("eng-30-14974264-n_paper", ["1","A material made of cellulose pulp derived mainly from wood or rags or certain grasses.","n","eng"])
    element_year = ("eng-30-15203791-n_year", ["1","A period of time containing 365 (or 366) days.","n","eng"])
    
    prompts_paper = componenteQuestionMaker_extraccion.generate_prompts(element_paper)
    prompts_year = componenteQuestionMaker_extraccion.generate_prompts(element_year)
    
    assert prompts_paper == ["As a linguistics expert, provide five sentences where the noun 'paper' appears in the sense of 'A material made of cellulose pulp derived mainly from wood or rags or certain grasses.'."], "Shold be true"
    assert prompts_year == ["As a linguistics expert, provide five sentences where the noun 'year' appears in the sense of 'A period of time containing 365 (or 366) days.'."], "Shold be true"
   
def component_question_maker_validacion_test():
    
    # Elementos de prueba
    element_plant = ("eng-30-00017222-n_plant", [
        "2",
        "(botany) a living organism lacking the power of locomotion.",
        "(botánica) una entidad viviente que no posee la capacidad de movimiento.",
        "n",
        "eng",
        [
            " 1. The plant, with its green leaves and sturdy stem, stood tall amidst the barren landscape.\n2. The botanist carefully examined the plant's intricate structure, noting the arrangement of its roots and branches.\n3. The plant's delicate petals opened to reveal a vibrant array of colors, attracting bees and butterflies alike.\n4. The plant's leaves, once lush and green, now wilted under the scorching sun, a victim of drought and neglect.\n5. The plant's seeds, carefully nurtured in the soil, sprouted into a new life, a testament to the power of nature and the cycle of life.",
            [
                " La planta, con sus hojas verdes y su tronco firme, se erguía en medio del paisaje árido.",
                " El botánico examinó cuidadosamente la estructura intrincada de la planta, notando la disposición de sus raíces y ramas.",
                " Las delicadas pétalos de la planta se abrieron para revelar un espectacular arreglo de colores, atraendo a las abejas y mariposas igualmente.",
                " Las hojas de la planta, que una vez eran vives y verdes, ahora están marchitando bajo el sol ardiente, víctima de la sequía y la negligencia.",
                " Las semillas de la planta, cuidadosamente nutridas en el suelo, brotaron en una nueva vida, un testimonio del poder de la naturaleza y el ciclo de la vida.",      
            ]
        ],
        "planta"
    ])
    
    elemet_substance = ("eng-30-00019613-n_substance", [
        "1",
        "The real physical matter of which a person or thing consists.",
        "La materia física real de la que consta una persona o cosa.",
        "n",
        "eng",
        [
            " 1. The substance of the rock is primarily composed of granite.\n2. The chemical substance of water is H2O.\n3. The substance of the human body is made up of various organs and tissues.\n4. The substance of the diamond is carbon, arranged in a crystalline structure.\n5. The substance of the air we breathe is primarily composed of nitrogen, oxygen, and trace amounts of other gases.",
            [
                " La sustancia de la roca está principalmente compuesta de granito.",
                " La sustancia química del agua es H2O.",
                " La sustancia del cuerpo humano está compuesta por varios órganos y tejidos.",
                " La sustancia del diamante es carbono, dispuesto en una estructura cristalina.",
                " La sustancia principal del aire que respiramos está compuesta por nitrógeno, oxígeno y pequeñas cantidades de otros gases.",
            ]
        ],
        "sustancia"
    ])
     
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
        element_paper = ("eng-30-14974264-n_paper", ["1","A material made of cellulose pulp derived mainly from wood or rags or certain grasses.","n","eng"])
        element_year = ("eng-30-15203791-n_year", ["1","A period of time containing 365 (or 366) days.","n","eng"])
    
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

def component_extractor_test():
    
    # --------------------------------------   Prueba 1   -------------------------------------------
        
    # Elementos de prueba
    element_cell = ("eng-30-00006484-n_cell", [
        "2",
        "(biology) the basic structural and functional unit of all organisms; they may exist as independent units of life (as in monads) or may form colonies or tissues as in higher plants and animals.",
        "(biología) la unidad estructural y funcional básica de todas las organizaciones vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.",
        "n",
        "eng",
        [
            " 1. The cell is a fundamental building block of all living organisms, providing structure and facilitating essential biological processes.\n2. In multicellular organisms, cells work together to form complex tissues and organs that enable the organism to carry out its functions.\n3. Cells are capable of reproducing through binary fission or other means, allowing for growth and development in both unicellular and multicellular organisms.\n4. The cell membrane is a crucial component of the cell, regulating the exchange of materials between the cell and its environment.\n5. Cells contain various organelles that perform specific functions, such as the mitochondria which generate energy through cellular respiration or the chloroplasts in plant cells that carry out photosynthesis.",
            [
                " La célula es el bloque básico de construcción fundamental en todas las entidades vivientes, proporcionando estructura y facilitando procesos biológicos esenciales.",
                " En los seres multicelulares, las células trabajan juntas para formar tejidos y órganos complejos que permiten al organismo llevar a cabo sus funciones.",
                " Las células son capaces de reproducirse a través de la fisión binaria o otros medios, lo que permite el crecimiento y el desarrollo tanto en organismos unicelulares como en multicelulares.",
                " La membrana celular es un componente crucial de la célula, regulando el intercambio de materiales entre la célula y su entorno.",
                " Las células contienen varias organelas que realizan funciones específicas, como las mitocondrias que generan energía a través de la respiración celular o los cloroplastos en las células vegetales que llevan a cabo la fotosíntesis."
            ]
        ]
    ])
    
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
    
    assert result_cell == ['célula'], "Should be ['célula']"
    
    # --------------------------------------   Prueba 2   -------------------------------------------
   
    # Elementos de prueba
    element_cause = ("eng-30-00007347-n_cause", [
        "4",
        "Any entity that produces an effect or is responsible for events or results.",
        "Cualquier entidad que produce un efecto o es responsable de los eventos o resultados'.",
        "n",
        "eng",
        [
            " 1. The cause of the accident was a malfunctioning brake system.\n2. The lack of rainfall is the primary cause of the drought.\n3. The cause of the disease outbreak can be traced back to contaminated food.\n4. The cause of the financial crisis was a combination of factors, including risky investments and lax regulation.\n5. The cause of the explosion was a gas leak in the pipeline.",
            [
                " La causa del accidente fue un sistema de frenos defectuoso.",
                " La falta de lluvias es la causa principal de la sequía.",
                " La causa de la salida de la enfermedad se puede rastrear hasta la comida contaminada.",
                " La causa de la crisis financiera fue una combinación de factores, incluyendo inversiones riesgosas y regulación relajada.",
                " La causa de la explosión fue una fuga de gas en el conducto."
            ]
        ]
    ])
    
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
    
    assert result_cause == ['causa'], "Should be ['causa']"
    
    # --------------------------------------   Prueba 3   -------------------------------------------
    
    llm_answer_list_3 =     llm_answer_list_1 = [
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
    
    assert result_cell_2 == ['NULL', {'Correctas.': 0}, {'Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.': 0}, {'Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.': 5}, {'Mensaje de información': 'La entrada ha terminado su ejecución en la extracción del resultado provisional.'}], "Should be true"
     

    
def component_validator_test():
        
    # --------------------------------------   Prueba 1   -------------------------------------------
    
    element_cause = ("eng-30-00007347-n_cause", [
        "4",
        "Any entity that produces an effect or is responsible for events or results.",
        "Cualquier entidad que produce un efecto o es responsable de los eventos o resultados'.",
        "n",
        "eng",
        [
            " 1. The cause of the accident was a malfunctioning brake system.\n2. The lack of rainfall is the primary cause of the drought.\n3. The cause of the disease outbreak can be traced back to contaminated food.\n4. The cause of the financial crisis was a combination of factors, including risky investments and lax regulation.\n5. The cause of the explosion was a gas leak in the pipeline.",
            [
                " La causa del accidente fue un sistema de frenos defectuoso.",
                " La falta de lluvias es la causa principal de la sequía.",
                " La causa de la salida de la enfermedad se puede rastrear hasta la comida contaminada.",
                " La causa de la crisis financiera fue una combinación de factores, incluyendo inversiones riesgosas y regulación relajada.",
                " La causa de la explosión fue una fuga de gas en el conducto."
            ]
        ],
        "causa",
        [
            " 1) La causa del accidente fue la falta de atención del conductor.\n2) El cambio climático es una causa preocupante para la supervivencia de las especies en peligro.\n3) La pobreza es una causa importante de la mortalidad infantil en muchos países.\n4) La falta de educación es una causa de la desigualdad social.\n5) El estrés es una causa común de problemas de salud mental.",
            [
                " The cause of the accident was the lack of attention by the driver.",
                " The climate change is a concerning cause for the survival of endangered species.",
                " Poverty is a significant cause of childhood mortality in many countries.",
                " The lack of education is a cause of social inequality.",
                " Stress is a common cause of mental health problems."
            ]
        ]
    ])
    
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
    
    result_cause = componenteExtractor_faseValidacion.get_result(element_cause, llm_answer_list_1)
    
    assert result_cause == ['causa'], "Should be ['causa']"
    
    # --------------------------------------   Prueba 2   -------------------------------------------
    
    element_cell = ("eng-30-00006484-n_cell", [
        "2",
        "(biology) the basic structural and functional unit of all organisms; they may exist as independent units of life (as in monads) or may form colonies or tissues as in higher plants and animals.",
        "(biología) la unidad estructural y funcional básica de todas las organizaciones vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.",
        "n",
        "eng",
        [
            " 1. The cell is a fundamental building block of all living organisms, providing structure and facilitating essential biological processes.\n2. In multicellular organisms, cells work together to form complex tissues and organs that enable the organism to carry out its functions.\n3. Cells are capable of reproducing through binary fission or other means, allowing for growth and development in both unicellular and multicellular organisms.\n4. The cell membrane is a crucial component of the cell, regulating the exchange of materials between the cell and its environment.\n5. Cells contain various organelles that perform specific functions, such as the mitochondria which generate energy through cellular respiration or the chloroplasts in plant cells that carry out photosynthesis.",
            [
                " La célula es el bloque básico de construcción fundamental en todas las entidades vivientes, proporcionando estructura y facilitando procesos biológicos esenciales.",
                " En los seres multicelulares, las células trabajan juntas para formar tejidos y órganos complejos que permiten al organismo llevar a cabo sus funciones.",
                " Las células son capaces de reproducirse a través de la fisión binaria o otros medios, lo que permite el crecimiento y el desarrollo tanto en organismos unicelulares como en multicelulares.",
                " La membrana celular es un componente crucial de la célula, regulando el intercambio de materiales entre la célula y su entorno.",
                " Las células contienen varias organelas que realizan funciones específicas, como las mitocondrias que generan energía a través de la respiración celular o los cloroplastos en las células vegetales que llevan a cabo la fotosíntesis."
            ]
        ],
        "célula",
        [
            " 1. Las células son el bloque básico de la vida.\n2. La división celular es un proceso fundamental para la reproducción y el crecimiento.\n3. Cada célula contiene una copia completa del ADN, pero solo una pequeña parte se expresa en cualquier momento.\n4. Las células especializadas tienen funciones específicas en los organismos multicelulares.\n5. La investigación de las células ha revelado muchas verdades sobre la biología y la medicina.",
            [
                " Cells are the fundamental building blocks of life.",
                " The cell division process is a fundamental one for reproduction and growth.",
                " Each cell contains a complete copy of DNA, but only a small portion is expressed at any given time.",
                " 'The specialized cells have specific functions in multicellular organisms.'",
                " The investigation of cells has revealed many truths about biology and medicine."
            ]
        ]
    ])
    
    llm_answer_list_2 =         [
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
    
    assert result_cell == ['célula'], "Should be ['célula']"
    
    # --------------------------------------   Prueba 2   -------------------------------------------
    
    element_object =  ("eng-30-00002684-n_object", [
        "1",
        "A tangible and visible entity; an entity that can cast a shadow.",
        "Una entidad tangible y visible; una entidad que puede hacer sombra'.",
        "n",
        "eng",
        [
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
        "objeto",
        [
            " 1. The object cast a shadow on the wall.\n2. The object was hidden behind the tree.\n3. The object was found at the bottom of the lake.\n4. The object was buried under the sand.\n5. The object was obscured by the fog.",
            [
                " The object (tangible and visible entity) cast a shadow on the wall.",
                " The item was concealed behind the tree.\n\n",
                " The item was discovered at the bottom of the lake.",
                " The item was buried beneath the sand.\n\n",
                " The object was hidden by the fog.\n\n"
            ]
        ]
    ])
    
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
    
    assert result_object == ["NULL",
    {
      "Correctas.": 0
    },
    {
      "Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.": 0
    },
    {
      "Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.": 5
    },
    {
      "Mensaje de información": "La entrada ha terminado su ejecución en la validación del resultado provisional."
    }], "Should be true"
    
def component_exporter_test():
    
    exploited_information = {
        "eng-30-00002684-n_object": [
            "1",
            "A tangible and visible entity; an entity that can cast a shadow.",
            "Una entidad tangible y visible; una entidad que puede proyectar sombra.'.",
            "n",
            "eng",
            [
            " The object on the table was a vase made of porcelain. Its delicate curves and intricate design were mesmerizing to behold. As I approached it, its shadow grew longer and more defined, casting a soft glow across the room.\n\nThe object in my hand was a smooth stone, cool to the touch. It had been worn down by years of tumbling through streams and rivers, leaving behind a textured surface that felt almost alive beneath my fingertips. As I held it up to the light, its shadow danced across the ground, a testament to its solidity and weight.\n\nThe object in front of me was a book, bound in leather and filled with pages of wisdom and knowledge. Its cover bore the imprint of an ancient symbol, a reminder of the secrets that lay within. As I opened it, its shadow stretched out behind me, casting a long, dark line across the floor.\n\nThe object on the wall was",
            [
                " El objeto en la mesa era una jarra hecha de porcelana.",
                " Sus delicadas curvas y su compleja forma eran hipnóticas de contemplar.",
                " Mientras me acercaba, su sombra se alargó y se definió más, proyectando una luz suave en la habitación.",
                " El objeto en mi mano era una piedra lisa, fría al tacto.",
                " 'Había sido desgastado durante años de ser arrastrado por corrientes y ríos, dejando atrás una superficie texturizada que sentía casi viva bajo mis dedos.'",
                " Mientras la sostuviese hacia la luz, su sombra bailaba por el suelo, una prueba de su sólida y pesada naturaleza.",
                " El objeto que estaba delante de mí era un libro, recubierto de cuero y lleno de páginas de sabiduría y conocimiento.",
                " Su tapadera llevaba la impresión de un antiguo símbolo, una recordatoria de los secretos que se escondían dentro.",
                " Al abrirlo, su sombra se extendió detrás de mí, dibujando una larga línea oscura en el piso.",
                " El objeto en la pared era."
            ]
            ],
            "objeto",
            [
            " 1. The object cast a long shadow on the ground.\n2. The ball was an object that rolled across the floor.\n3. The statue in the park is an object that has been there for years.\n4. The car's headlights illuminated the object in front of it.\n5. The rock formation in the desert is an object that has stood the test of time.",
            [
                " The object cast a long shadow on the ground.\n\n",
                " The ball was a tangible and visible entity that could project a shadow, which rolled across the floor.\n\n",
                " The statue in the park is a tangible and visible entity that can cast a shadow, which has been there for years.",
                " The car's headlights illuminated the tangible and visible entity that could cast a shadow.\n\n",
                " The rock formation in the desert is a tangible and visible entity that can cast a shadow, which has withstood the test of time."
            ]
            ],
            "NULL",
            {
            "Correctas.": 0
            },
            {
            "Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.": 0
            },
            {
            "Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.": 5
            },
            {
            "Mensaje de información": "La entrada ha terminado su ejecución en la validación del resultado provisional."
            }
        ],
        "eng-30-00006484-n_cell": [
            "2",
            "(biology) the basic structural and functional unit of all organisms; they may exist as independent units of life (as in monads) or may form colonies or tissues as in higher plants and animals.",
            "(biología) la unidad estructural y funcional básica de todas las entidades vivientes; pueden existir como unidades independientes de la vida (como en los monadas), o pueden formar colonias o tejidos, como en las plantas y animales superiores.",
            "n",
            "eng",
            [
            " 1. The cell is the fundamental building block of all living organisms, providing a protective environment for the genetic material to function properly.\n2. In multicellular organisms, cells work together to form tissues and organs that carry out specialized functions.\n3. The human body contains trillions of cells, each with its own unique role in maintaining homeostasis and carrying out essential processes.\n4. Some organisms, such as bacteria and protists, exist as single cells called monads, while others form colonies or tissues through cell division and differentiation.\n5. The study of cell biology has led to significant advances in medicine, allowing for the development of new treatments and therapies for a variety of diseases.",
            [
                " La celda es el bloque básico de construcción fundamental de todas las entidades vivas, proporcionando un entorno protector para que la materia genética funcione correctamente.",
                " En organismos multicelulares, las células trabajan juntas para formar tejidos y órganos que llevan a cabo funciones especializadas.",
                " El cuerpo humano contiene trillones de células, cada una con su propio papel único en mantener la homeostasis y llevar a cabo procesos esenciales.",
                " Algunos organismos, como las bacterias y los protistas, existen como células individuales llamadas monadas, mientras que otros forman colonias o tejidos a través de la división celular y la diferenciación.",
                " El estudio de la biología celular ha llevado a importantes avances en la medicina, permitiendo el desarrollo de nuevas terapias y tratamientos para una variedad de enfermedades."
            ]
            ],
            "células",
            [
            " 1. Las células son el bloque básico de la vida.\n2. Cada organismo está compuesto por millones de células.\n3. La división celular es un proceso fundamental en la biología.\n4. Los científicos están investigando cómo las células se comunican entre sí.\n5. Las células cancerosas son una amenaza para la salud humana.",
            [
                " 'Cells are the basic building block of life.'",
                " 'Each organism is composed of millions of cells.'",
                " 'Cell division is a fundamental process in biology.'",
                " The scientists are investigating how cells communicate with each other.",
                " Cancerous cells are a threat to human health."
            ]
            ],
            "células"
        ],
        "eng-30-00007347-n_cause": [
            "4",
            "Any entity that produces an effect or is responsible for events or results.",
            "Cualquier entidad que produce un efecto o es responsable de los eventos o resultados.'.",
            "n",
            "eng",
            [
            " 1. The cause of the accident was a malfunctioning brake system.\n2. The lack of rainfall is the primary cause of the drought.\n3. The cause of the disease outbreak can be traced back to contaminated food.\n4. The cause of the fire was an electrical fault in the wiring.\n5. The cause of the financial crisis was a combination of factors, including excessive borrowing and risky investments.",
            [
                " La causa del accidente fue un sistema de frenos defectuoso.",
                " La falta de precipitaciones es la causa principal de la sequía.",
                " La causa de la salida de la enfermedad se puede rastrear hasta el alimento contaminado.",
                " La causa del incendio fue una falla eléctrica en la instalación de cables.",
                " La causa de la crisis financiera fue una combinación de factores, incluyendo el exceso de préstamos y las inversiones riesgosas."
            ]
            ],
            "causa",
            [
            " 1. La causa de la epidemia fue una mutación genética.\n2. El cambio climático es la causa principal del deshielo polar.\n3. La falta de educación es la causa principal de la pobreza en muchas partes del mundo.\n4. El estrés es la causa más común de enfermedades mentales.\n5. La corrupción política es la causa principal de la desconfianza en el gobierno.",
            [
                " The cause of the epidemic was a genetic mutation.\n\n",
                " The primary cause of polar ice melting is climate change.",
                " The lack of education is the main cause of poverty in many parts of the world.",
                " Stress is the most common cause of mental illnesses.\n\n",
                " Political corruption is the main cause of distrust in government."
            ]
            ],
            "causa"
        ],
        "eng-30-00007846-n_person": [
            "1",
            "A human being.",
            "Una persona'.",
            "n",
            "eng",
            [
            " 1. The person sitting next to me on the bus is reading a book.\n2. The person who helped me with my project was very kind.\n3. The person I met at the party last night had an interesting accent.\n4. The person in charge of the event is making sure everything runs smoothly.\n5. The person who won the race set a new world record.",
            [
                " La persona que está sentada al lado mío en el autobús está leyendo un libro.",
                " La persona que me ayudó con mi proyecto fue muy amable.",
                " La persona que conocí en la fiesta de anoche tenía un acento interesante.",
                " La persona encargada del evento está asegurándose de que todo fluya sin problemas.",
                " La persona que ganó la carrera estableció un nuevo récord mundial."
            ]
            ],
            "persona",
            [
            " 1) La mujer que estaba sentada a mi lado era una persona muy amable. 2) El hombre que leyó el libro es una persona muy inteligente. 3) La niña que cantó la canción es una persona muy talentosa. 4) El hombre que ganó el premio es una persona muy exitosa. 5) La mujer que ayudó a los necesitados es una persona muy generosa.",
            [
                " The woman who was sitting next to me was very kind.",
                " The man who read the book is a very intelligent person.\n\n",
                " The girl who sang the song is a very talented person.",
                " The man who won the prize is a very successful person.\n\n",
                " The woman who helped those in need is a very generous person."
            ]
            ],
            "persona"
        ],
        "eng-30-00015388-n_animal": [
            "1",
            "A living organism characterized by voluntary movement.",
            "Un ser vivo que se mueve de manera voluntaria.",
            "n",
            "eng",
            [
            " 1. The lion is an animal that roams the savannah in search of prey.\n2. The elephant is the largest land animal and can weigh up to six tons.\n3. The cheetah is a fast-running animal that can reach speeds of over 70 miles per hour.\n4. The gorilla is an intelligent animal that lives in groups called troops.\n5. The kangaroo is a marsupial animal that has powerful hind legs for jumping long distances.",
            [
                " El león es un animal que pasea la sabana en busca de presas.",
                " El elefante es el mayor animal terrestre y puede pesar hasta seis toneladas.",
                " La gueparda es un animal rápido que puede alcanzar velocidades superiores a los 70 millas por hora.",
                " El gorila es un animal inteligente que vive en bandadas llamadas tropas.",
                " El kanguro es un animal marsupial que tiene patas traseras poderosas para saltar largas distancias."
            ]
            ],
            "animal",
            [
            " 1. El leopardo es un animal grande y poderoso que habita en los bosques tropicales.\n2. Los elefantes son animales herbívoros que pueden pesar hasta tres toneladas.\n3. La gacela es un animal rápido y ágil que corre a velocidades de hasta 80 kilómetros por hora.\n4. El panda rojo es un animal en peligro de extinción que habita en los bosques de China.\n5. La orca es un animal inteligente y social que vive en grupos llamados podas.",
            [
                " The leopard is a large and powerful animal that lives in tropical forests.",
                " Elephants are herbivorous animals that can weigh up to three tons.",
                " The gazelle is a fast and agile animal that runs at speeds up to 80 kilometers per hour.",
                " The red panda is an endangered animal that lives in the forests of China.",
                " The killer whale is an intelligent and social animal that lives in groups called pods."
            ]
            ],
            "animal"
        ]
        }
    
    config = ConfigParser()
    config.read('./config.ini')
    
    componenteExporter = ComponenteExporter(config['file_path']['exploited_information_file_path'])
    
    componenteExporter.export_knowledge(exploited_information)
    
    # Abrir el archivo en modo lectura
    try:
        with open(config['file_path']['exploited_information_file_path'], 'r') as archivo:
            # Leer el archivo línea por línea
            for linea in archivo:
                # Comprobar si la línea cumple con los criterios
                if validar_linea(linea):
                    assert True
                else:
                    assert False
    except FileNotFoundError:
        print(f'Archivo "{config["file_path"]["exploited_information_file_path"]}" no encontrado. Vuelve a introducir una nueva ruta')
        
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
    
    phrase_5 = "La fábrica de papel había estado en funcionamiento durante más de un siglo, proporcionando oportunidades de empleo a generaciones de familias en la zona."
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
    
    elemento_prueba_piloto_masculino = "\n1. El gran desafío que enfrenta la tierra es combatir la erosión y mantener su fertilidad.\n2. La tierra está siendo devastada por los cambios climáticos y la deforestación.\n3. La tierra necesita que los humanos cambien su manera de pensar y actuar para protegerla.\n4. El hombre ha estado explotando y devastando la tierra durante siglos.\n5. La tierra ha sido la fuente de vida y prosperidad para millones de personas durante milenios.\n6. La tierra es un recurso limitado que necesita ser utilizado y preservado con cuidado.\n7. La tierra es un regalo de la naturaleza que ha sido y seguirá siendo vital para la supervivencia humana.\n8. La tierra es más que un lugar, es un sistema complejo que afecta a todas las formas de vida.\n9. La tierra es la fuente de todos los recursos que necesitamos para sobrevivir y prosperar.\n10. La tierra es un legado que debemos preservar para las generaciones futuras."

    expected_output_piloto_masculino = ["El gran desafío que enfrenta la tierra es combatir la erosión y mantener su fertilidad.",
                              "La tierra está siendo devastada por los cambios climáticos y la deforestación.",
                              "La tierra necesita que los humanos cambien su manera de pensar y actuar para protegerla.",
                              "El hombre ha estado explotando y devastando la tierra durante siglos.",
                              "La tierra ha sido la fuente de vida y prosperidad para millones de personas durante milenios.",
                              "La tierra es un recurso limitado que necesita ser utilizado y preservado con cuidado.",
                              "La tierra es un regalo de la naturaleza que ha sido y seguirá siendo vital para la supervivencia humana.",
                              "La tierra es más que un lugar, es un sistema complejo que afecta a todas las formas de vida.",
                              "La tierra es la fuente de todos los recursos que necesitamos para sobrevivir y prosperar.",
                              "La tierra es un legado que debemos preservar para las generaciones futuras."]
    
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
    component_question_maker_traduccion_españolingles_test() # Tested correctly
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
    print("Testing over Extractor component...")
    component_extractor_test() # Tested correctly
    print("Everything in Extractor component passed")
    print("Testing over Validator component...")
    # component_validator_test() # Tested correctly
    print("Everything in Validator component passed")
    print("Testing over Exporter component...")
    component_exporter_test() # Tested correctly
    print("Everything in Exporter component passed")
    print("Testing over Auxiliar funcitions...")
    auxiliar_functions_test() # Tested correctly
    print("Everything in Auxiliar funcitions passed")
    print("Everything passed")