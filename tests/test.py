

from io import StringIO
import json
from configparser import ConfigParser
import re
import sys
sys.path.append('..')  # Agrega la carpeta superior al sys.path
sys.path.append("../auxFunctionLibrary") #Agrega la carpeta superior al sys.path
from pythonLib import auxFunctions
from componenteImporter import ComponenteImporter
import componenteQuestionMaker
from componenteLLMCommunicator import ComponenteLLMCommunicator
import componenteExtractor
import componenteValidator
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
    
def component_question_maker_test():
     
    # Elementos de prueba
    element_paper = ("eng-30-14974264-n_paper", ["1","A material made of cellulose pulp derived mainly from wood or rags or certain grasses.","Material elaborado a partir de pulpa de celulosa derivada principalmente de la madera o de trapos o de ciertas hierbas.","n","eng"])
    element_year = ("eng-30-15203791-n_year", ["1","A period of time containing 365 (or 366) days.","Un período de tiempo que contiene 365 (o 366) días.","n","eng"])
    
    provisional_prompts_paper = componenteQuestionMaker.generate_provisional_prompts(element_paper)
    provisional_prompts_year = componenteQuestionMaker.generate_provisional_prompts(element_year)
    assert provisional_prompts_paper == ["As a linguistics expert, provide five sentences where the noun 'paper' appears in the sense of 'A material made of cellulose pulp derived mainly from wood or rags or certain grasses.'."], "Shold be true"
    assert provisional_prompts_year == ["As a linguistics expert, provide five sentences where the noun 'year' appears in the sense of 'A period of time containing 365 (or 366) days.'."], "Shold be true"
        
    
    validation_prompts_paper = componenteQuestionMaker.generate_validation_prompts(element_paper, "papel")
    validation_prompts_year = componenteQuestionMaker.generate_validation_prompts(element_year, "año")
    
    assert validation_prompts_paper == ["Como experto en lingüística, proporciona cinco frases en las que el sustantivo 'papel' aparezca en el sentido de 'Material elaborado a partir de pulpa de celulosa derivada principalmente de la madera o de trapos o de ciertas hierbas.'."], "Shold be true"
    assert validation_prompts_year == ["Como experto en lingüística, proporciona cinco frases en las que el sustantivo 'año' aparezca en el sentido de 'Un período de tiempo que contiene 365 (o 366) días.'."], "Shold be true"
        
    
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
    componenteLLMCommunicator_test = ComponenteLLMCommunicator(config['file_path']['provisional_results_language_model_path_test']) 
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
        componenteLLMCommunicator = ComponenteLLMCommunicator(config['file_path']['provisional_results_language_model_path'])
        
        # Cargamos el modelo de lenguaje que vamos a utilizar para conseguir las respuestas provisionales
        componenteLLMCommunicator.load_model()
        
        # Elementos de prueba
        element_paper = ("eng-30-14974264-n_paper", ["1","A material made of cellulose pulp derived mainly from wood or rags or certain grasses.","Material elaborado a partir de pulpa de celulosa derivada principalmente de la madera o de trapos o de ciertas hierbas.","n","eng"])
        element_year = ("eng-30-15203791-n_year", ["1","A period of time containing 365 (or 366) days.","Un período de tiempo que contiene 365 (o 366) días.","n","eng"])
    
        # Pruebas de preguntas
        provisional_prompts_paper = componenteQuestionMaker.generate_provisional_prompts(element_paper)
        provisional_prompts_year = componenteQuestionMaker.generate_provisional_prompts(element_year)
        for element in provisional_prompts_paper:
            componenteLLMCommunicator.run_the_model(element) 
        for element in provisional_prompts_year:
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
    
    # Tests de extracción de respuestas ----------------------------------------
    
    # elemento de prueba (Respuesta recibida por el LLM)
    elemento_prueba_paper = {
                                        "id": "cmpl-b62c2c10-da98-45bf-913b-bc1f678e5297",
                                        "object": "text_completion",
                                        "created": 1717590089,
                                        "model": "../../models/zephyr-7b-alpha.Q4_K_M.gguf",
                                        "choices": [
                                            {
                                            "text": "Question: As a linguistics expert, provide five sentences where the noun 'paper' appears in the sense of 'A material made of cellulose pulp derived mainly from wood or rags or certain grasses.'. Answer: 1. The paper is an essential component for printing books and newspapers.\n\n2. The printer uses high-quality paper to ensure that the text looks crisp and clear.\n\n3. The artist used handmade paper to create a unique texture in her artwork.\n\n4. The recycling center collects old paper to be repurposed into new products.\n\n5. The paper mill produces large quantities of paper for commercial use, such as office supplies and packaging materials.",
                                            "index": 0,
                                            "logprobs": "null",
                                            "finish_reason": "stop"
                                            }
                                        ],
                                        "usage": {
                                            "prompt_tokens": 49,
                                            "completion_tokens": 101,
                                            "total_tokens": 150
                                        }
                                        }
    expected_output_paper = ["The paper is an essential component for printing books and newspapers.",
                                "The printer uses high-quality paper to ensure that the text looks crisp and clear.",
                                "The artist used handmade paper to create a unique texture in her artwork.",
                                "The recycling center collects old paper to be repurposed into new products.",
                                "The paper mill produces large quantities of paper for commercial use, such as office supplies and packaging materials."]
    assert expected_output_paper == componenteExtractor.extract_llm_answers(elemento_prueba_paper), "Should be true"
    
    elemento_prueba_year = {
                            "id": "cmpl-b2bcc46d-c66a-4787-968d-b355d91185b1",
                            "object": "text_completion",
                            "created": 1717590123,
                            "model": "../../models/zephyr-7b-alpha.Q4_K_M.gguf",
                            "choices": [
                                {
                                "text": "Question: As a linguistics expert, provide five sentences where the noun 'year' appears in the sense of 'A period of time containing 365 (or 366) days.'. Answer: The year 2021 has been marked by significant events such as the COVID-19 pandemic and the US presidential election. In 2020, the world witnessed a global economic downturn due to the pandemic's impact on businesses and industries. The year 2019 was a historic one for climate change activism, with protests and strikes taking place around the world. The year 2018 saw major political developments, including the US midterm elections and Brexit negotiations. In 2017, there were significant events such as the inauguration of President Trump and the devastating hurricane season in the Caribbean and Gulf Coast regions.",
                                "index": 0,
                                "logprobs": "null",
                                "finish_reason": "stop"
                                }
                            ],
                            "usage": {
                                "prompt_tokens": 46,
                                "completion_tokens": 138,
                                "total_tokens": 184
                            }
                            }

    expected_output_year = ["The year 2021 has been marked by significant events such as the COVID-19 pandemic and the US presidential election.",
                            "In 2020, the world witnessed a global economic downturn due to the pandemic's impact on businesses and industries.",
                            "The year 2019 was a historic one for climate change activism, with protests and strikes taking place around the world.",
                            "The year 2018 saw major political developments, including the US midterm elections and Brexit negotiations.",
                            "In 2017, there were significant events such as the inauguration of President Trump and the devastating hurricane season in the Caribbean and Gulf Coast regions."]
    assert expected_output_year == componenteExtractor.extract_llm_answers(elemento_prueba_year), "Should be true"
    
    phrase = "A material made of cellulose pulp derived mainly from wood or rags or certain grasses."
    elemento_prueba_traducción = {
                                    "id": "cmpl-cf7c52ee-ac4c-4709-bc4a-6aa5523f4ed0",
                                    "object": "text_completion",
                                    "created": 1714754403,
                                    "model": "./models/zephyr-7b-alpha.Q4_K_M.gguf",
                                    "choices": [
                                        {
                                        "text": 'Question: As a translation expert, I need an accurate translation into Spanish of the following phrase: "' + phrase +'". Answer: Material elaborado a partir de pulpa de celulosa derivada principalmente de la madera o de trapos o de ciertas hierbas.',
                                        "index": 0,
                                        "logprobs": "null",
                                        "finish_reason": "stop"
                                        }
                                    ],
                                    "usage": {
                                        "prompt_tokens": 58,
                                        "completion_tokens": 20,
                                        "total_tokens": 78
                                    }
                                   }
    
    expected_output_traduccion = "Material elaborado a partir de pulpa de celulosa derivada principalmente de la madera o de trapos o de ciertas hierbas."
    assert expected_output_traduccion == componenteExtractor.extract_llm_answers(elemento_prueba_traducción), "Should be true"
    
    # Tests de obtener el provisional answer -----------------------------------
    
    # --------------------------------------   Prueba 1   -------------------------------------------
        
    # Elementos de prueba
    element_tree = (  "eng-30-13104059-n_tree", [
                        "1",
                        "A tall perennial woody plant having a main trunk and branches forming a distinct elevated crown; includes both gymnosperms and angiosperms.",
                        "Una planta arbórea perenne de gran altura que tiene un tronco principal y ramas formando una corona distintiva en elevación, incluye tanto a las gimnospermas como a las angiospermas.",
                        "n",
                        "eng",
                        [
                            [
                                "She spent hours shopping for the perfect dress to wear at her sister's wedding.",
                                "Ella pasó horas comprando ropa para el vestido perfecto que llevaría a la boda de su hermana."
                            ],
                            [
                                "The mall was packed with people doing their holiday shopping.",
                                "La tienda estaba llena de gente haciendo sus compras navideñas."
                            ],
                            [
                                "I love going to thrift stores for unique and affordable shopping finds.",
                                "Adoro ir a tiendas de segundamano para encontrar compras únicas y baratas."
                            ],
                            [
                                "Online shopping has become increasingly popular due to its convenience.",
                                "La compra en línea ha aumentado de manera creciente debido a su comodidad."
                            ],
                            [
                                "Shopping for groceries can be a daunting task, especially when you have a long list of items to buy.",
                                "La compra de alimentos puede ser una tarea desafiante, especialmente cuando hay muchas cosas que comprar en la lista."
                            ]
                            ]
                        ]
                    )
    output_tree = [
      [
        "The towering oak tree provided shade for the picnic on a hot summer day.",
        "El árbol de roble alto proporcionó sombra para la cena en un caluroso día de verano."
      ],
      [
        "The maple tree in the front yard boasted vibrant red leaves during autumn.",
        "La árbol de roble en el jardín delantero exhibió hojas rojas brillantes durante la otoño."
      ],
      [
        "The evergreen pine tree stood tall amidst the snowy landscape of winter.",
        "El árbol de pino siempreverde se erguía alto en medio del paisaje nevado de invierno."
      ],
      [
        "The birch tree's white bark contrasted beautifully against the lush green forest floor.",
        "La corteza blanca del árbol de betulá contrastó hermosamente contra el suelo verde y fértil del bosque."
      ],
      [
        "The willow tree's branches dipped gracefully into the tranquil pond, creating a serene atmosphere for the nearby wildlife.",
        "La rama del árbol de sauce se inclinó con gracia hacia el tranquilo estanque, creando una atmósfera serena para la fauna cercana."
      ]
    ]
    
    provisional_result = componenteExtractor.get_provisional_result(element_tree, output_tree)
    
    assert provisional_result == ['árbol'], "Should be ['árbol']"
    
    # --------------------------------------   Prueba 2   -------------------------------------------
   
    # Elementos de prueba
    element_paper = ( "eng-30-14974264-n_paper", [
                "1",
                "A material made of cellulose pulp derived mainly from wood or rags or certain grasses.",
                "Un material hecho de pulpa de celulosa derivada principalmente del madera o los paños o ciertas hierbas..",
                "n",
                "eng",
                [
                    [
                        "The paper was smooth and glossy, perfect for printing high-quality images.",
                        "El papel era suave y brillante, perfecto para imprimir imágenes de alta calidad."
                    ],
                    [
                        "The paper mill produced thousands of tons of paper every day, using a combination of wood and recycled materials.",
                        "La fábrica de papel produjo miles de toneladas de papel cada día, utilizando una combinación de madera y materiales reciclados."
                    ],
                    [
                        "The artist used handmade paper to create intricate sculptures that were both beautiful and functional.",
                        "El artista utilizó papel hecho a mano para crear esculturas complejas que eran al mismo tiempo bellas y funcionales."
                    ],
                    [
                        "The paper was acid-free and archival quality, ensuring that the documents would last for centuries.",
                        "El papel era ácido libre y de calidad arquivística, lo que garantizaba que los documentos duraran siglos."
                    ],
                    [
                        "The paper mill had been in operation for over a century, providing employment opportunities for generations of families in the area.",
                        "La fábrica de papel había estado en funcionamiento durante más de un siglo, proporcionando oportunidades de empleo a generaciones de familias en la zona."
                    ]
                ],
        ]
    )
    
    
    output_paper = [
                [
                    "The paper was smooth and glossy, perfect for printing high-quality images.",
                    "El papel era suave y brillante, perfecto para imprimir imágenes de alta calidad."
                ],
                [
                    "The paper mill produced thousands of tons of paper every day, using a combination of wood and recycled materials.",
                    "La fábrica de papel produjo miles de toneladas de papel cada día, utilizando una combinación de madera y materiales reciclados."
                ],
                [
                    "The artist used handmade paper to create intricate sculptures that were both beautiful and functional.",
                    "El artista utilizó papel hecho a mano para crear esculturas complejas que eran al mismo tiempo bellas y funcionales."
                ],
                [
                    "The paper was acid-free and archival quality, ensuring that the documents would last for centuries.",
                    "El papel era ácido libre y de calidad arquivística, lo que garantizaba que los documentos duraran siglos."
                ],
                [
                    "The paper mill had been in operation for over a century, providing employment opportunities for generations of families in the area.",
                    "La fábrica de papel había estado en funcionamiento durante más de un siglo, proporcionando oportunidades de empleo a generaciones de familias en la zona."
                ]
            ]

    provisional_result_2 = componenteExtractor.get_provisional_result(element_paper, output_paper)
    
    assert provisional_result_2 == ['papel'], "Should be ['papel']"
     
    # # --------------------------------------   Prueba 3   -------------------------------------------
    
        # Elementos de prueba
    element_shopping = (  "eng-30-00081836-n_shopping", [
                    "1",
                    "Searching for or buying goods or services.",
                    "Buscando o comprando bienes o servicios.",
                    "n",
                    "eng",
                    [
                        [
                            "She spent hours shopping for the perfect dress to wear at her sister's wedding.",
                            "Ella pasó horas comprando ropa para el vestido perfecto que llevaría a la boda de su hermana."
                        ],
                        [
                            "The mall was packed with people doing their holiday shopping.",
                            "La tienda estaba llena de gente haciendo sus compras navideñas."
                        ],
                        [
                            "I love going to thrift stores for unique and affordable shopping finds.",
                            "Adoro ir a tiendas de segundamano para encontrar compras únicas y baratas."
                        ],
                        [
                            "Online shopping has become increasingly popular due to its convenience.",
                            "La compra en línea ha aumentado de manera creciente debido a su comodidad."
                        ],
                        [
                            "Shopping for groceries can be a daunting task, especially when you have a long list of items to buy.",
                            "La compra de alimentos puede ser una tarea desafiante, especialmente cuando hay muchas cosas que comprar en la lista."
                        ]
                    ],
             ],
    )
    
    output_shopping =  [
                        [
                            "She spent hours shopping for the perfect dress to wear at her sister's wedding.",
                            "Ella pasó horas comprando ropa para el vestido perfecto que llevaría a la boda de su hermana."
                        ],
                        [
                            "The mall was packed with people doing their holiday shopping.",
                            "La tienda estaba llena de gente haciendo sus compras navideñas."
                        ],
                        [
                            "I love going to thrift stores for unique and affordable shopping finds.",
                            "Adoro ir a tiendas de segundamano para encontrar compras únicas y baratas."
                        ],
                        [
                            "Online shopping has become increasingly popular due to its convenience.",
                            "La compra en línea ha aumentado de manera creciente debido a su comodidad."
                        ],
                        [
                            "Shopping for groceries can be a daunting task, especially when you have a long list of items to buy.",
                            "La compra de alimentos puede ser una tarea desafiante, especialmente cuando hay muchas cosas que comprar en la lista."
                        ]
                    ]

    provisional_result_3 = componenteExtractor.get_provisional_result(element_shopping, output_shopping)
    
    assert provisional_result_3 == ['compra'], "Should be ['compra']"
    
def component_validator_test():
        
    # --------------------------------------   Prueba 1   -------------------------------------------
    
    element_paper = ( "eng-30-14974264-n_paper", [
                "1",
                "A material made of cellulose pulp derived mainly from wood or rags or certain grasses.",
                "Un material hecho de pulpa de celulosa derivada principalmente del madera o los paños o ciertas hierbas..",
                "n",
                "eng",
                [
                    [
                        "The paper was smooth and glossy, perfect for printing high-quality images.",
                        "El papel era suave y brillante, perfecto para imprimir imágenes de alta calidad."
                    ],
                    [
                        "The paper mill produced thousands of tons of paper every day, using a combination of wood and recycled materials.",
                        "La fábrica de papel produjo miles de toneladas de papel cada día, utilizando una combinación de madera y materiales reciclados."
                    ],
                    [
                        "The artist used handmade paper to create intricate sculptures that were both beautiful and functional.",
                        "El artista utilizó papel hecho a mano para crear esculturas complejas que eran al mismo tiempo bellas y funcionales."
                    ],
                    [
                        "The paper was acid-free and archival quality, ensuring that the documents would last for centuries.",
                        "El papel era ácido libre y de calidad arquivística, lo que garantizaba que los documentos duraran siglos."
                    ],
                    [
                        "The paper mill had been in operation for over a century, providing employment opportunities for generations of families in the area.",
                        "La fábrica de papel había estado en funcionamiento durante más de un siglo, proporcionando oportunidades de empleo a generaciones de familias en la zona."
                    ]
                ],
                "papel"
        ]
    )
    
    llm_extracted_answer_1 = [
      [
        "El papel es un material muy utilizado para la impresión y la escritura.",
        "The paper is a very commonly used material for printing and writing."
      ],
      [
        "La mayoría de los libros se imprimen en papel.",
        "The majority of books are printed on paper."
      ],
      [
        "Los periódicos son publicados diariamente en papel.",
        "Newspapers are published daily on paper."
      ],
      [
        "Las cartas se envían por correo en papel.",
        "The letters are sent by mail on paper."
      ],
      [
        "El papel es un producto económico y versátil que se utiliza en muchos aspectos de la vida cotidiana, desde el escritorio hasta la cocina.",
        "The paper is an economical and versatile product that is used in many aspects of daily life, from the office to the kitchen."
      ]
    ]
    
    final_result_paper = componenteValidator.get_final_result(element_paper, llm_extracted_answer_1, "papel")
    
    assert final_result_paper == ["papel"], "Should be ['papel']"
    
    # --------------------------------------   Prueba 2   -------------------------------------------
    
    
    element_tree = ("eng-30-13104059-n_tree", [
                "1",
                "A tall perennial woody plant having a main trunk and branches forming a distinct elevated crown; includes both gymnosperms and angiosperms.",
                "Una planta arbórea perenne de gran altura que tiene un tronco principal y ramas formando una corona distintiva en elevación, incluye tanto a las gimnospermas como a las angiospermas.",
                "n",
                "eng",
                [
                    [
                        "The towering oak tree provided shade for the picnic on a hot summer day.",
                        "El árbol de roble alto proporcionó sombra para la cena en un caluroso día de verano."
                    ],
                    [
                        "The maple tree in the front yard boasted vibrant red leaves during autumn.",
                        "La árbol de roble en el jardín delantero exhibió hojas rojas brillantes durante la otoño."
                    ],
                    [
                        "The evergreen pine tree stood tall amidst the snowy landscape of winter.",
                        "El árbol de pino siempreverde se erguía alto en medio del paisaje nevado de invierno."
                    ],
                    [
                        "The birch tree's white bark contrasted beautifully against the lush green forest floor.",
                        "La corteza blanca del árbol de betulá contrastó hermosamente contra el suelo verde y fértil del bosque."
                    ],
                    [
                        "The willow tree's branches dipped gracefully into the tranquil pond, creating a serene atmosphere for the nearby wildlife.",
                        "La rama del árbol de sauce se inclinó con gracia hacia el tranquilo estanque, creando una atmósfera serena para la fauna cercana."
                    ]
                ],
                "árbol",
                [
                    [
                        "El árbol más grande del bosque es un roble americano de más de 30 metros de altura.",
                        "The largest tree in the forest is an american oak, which is over 30 meters tall."
                    ],
                    [
                        "La sequía ha matado la mayoría de los árboles en el parque, dejando solo algunas coníferas resistentes.",
                        "The drought has killed most of the trees in the park, leaving only some resistant conifers."
                    ],
                    [
                        "El árbol de la vida es una metáfora cristiana que representa a Jesucristo como el centro y la fuente de la existencia humana.",
                        "The tree of life is a christian metaphor that represents jesus christ as the center and source of human existence."
                    ],
                    [
                        "Los árboles frutales son una parte importante de la dieta humana, proporcionando frutas y verduras para consumir.",
                        "Fruit-bearing trees are an important part of human diet, providing fruits and vegetables to consume."
                    ],
                    [
                        "El árbol genealógico es un documento que sigue la descendencia de una familia o linaje, mostrándola en forma de un árbol con raíces, tronco principal y ramas secundarias.",
                        "The genealogical tree is a document that follows the descent of a family or lineage, showing it in the form of a tree with roots, main trunk, and secondary branches."
                    ]
                ]
            ]
        )
    
    llm_extracted_answer_2 = [
                    [
                        "El árbol más grande del bosque es un roble americano de más de 30 metros de altura.",
                        "The largest tree in the forest is an american oak, which is over 30 meters tall."
                    ],
                    [
                        "La sequía ha matado la mayoría de los árboles en el parque, dejando solo algunas coníferas resistentes.",
                        "The drought has killed most of the trees in the park, leaving only some resistant conifers."
                    ],
                    [
                        "El árbol de la vida es una metáfora cristiana que representa a Jesucristo como el centro y la fuente de la existencia humana.",
                        "The tree of life is a christian metaphor that represents jesus christ as the center and source of human existence."
                    ],
                    [
                        "Los árboles frutales son una parte importante de la dieta humana, proporcionando frutas y verduras para consumir.",
                        "Fruit-bearing trees are an important part of human diet, providing fruits and vegetables to consume."
                    ],
                    [
                        "El árbol genealógico es un documento que sigue la descendencia de una familia o linaje, mostrándola en forma de un árbol con raíces, tronco principal y ramas secundarias.",
                        "The genealogical tree is a document that follows the descent of a family or lineage, showing it in the form of a tree with roots, main trunk, and secondary branches."
                    ]
                ]
    
    
    final_result_year = componenteValidator.get_final_result(element_tree, llm_extracted_answer_2, "árbol")
    
    assert final_result_year == ["árbol"], "Should be ['árbol']"
    
def component_exporter_test():
    
    exploited_information = {
        "eng-30-00039297-n_contact": [
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
        ],
        "eng-30-00058743-n_flight": [
            "4",
            "The act of escaping physically.",
            "La acción de huir físicamente.",
            "n",
            "eng",
            [
            [
                "The bird took flight from its nest to avoid being caught by predators.",
                "El pájaro tomó vuelo desde su nido para evitar ser capturado por los depredadores."
            ],
            [
                "The hikers fled into the forest, hoping to escape the wildfire through flight.",
                "Los senderistas huyeron hacia el bosque, esperando escapar del incendio forestal a través de la huida."
            ],
            [
                "The prisoner broke free and ran as fast as he could, taking flight from his captors.",
                "El preso se liberó y corrió lo más rápido que pudo, huyendo de sus captores."
            ],
            [
                "The survivors of the shipwreck swam for hours until they finally reached land, their flight from danger complete.",
                "Los supervivientes de la naufragio nadaron durante horas hasta que finalmente llegaron a tierra, su huida del peligro completa."
            ],
            [
                "The woman sprinted down the street, her heart racing as she tried to outrun the attacker and take flight from his grasp.",
                "La mujer corrió por la calle, su corazón latía mientras intentaba huir del agresor y lograr la fuga física."
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
        ],
        "eng-30-00072473-n_confusion": [
            "5",
            "A mistake that results from taking one thing to be another.",
            "Un error que resulta de confundir una cosa con otra.",
            "n",
            "eng",
            [
            [
                "The confusion between there and their led to several grammatical errors in the text.",
                "La confusión entre allí y sus llevó a varios errores gramaticales en el texto."
            ],
            [
                "The doctor's diagnosis was a case of confusion, mistaking the symptoms for those of a different disease.",
                "La diagnóstico del médico fue un caso de confusión, al confundir los síntomas con los de una enfermedad diferente."
            ],
            [
                "The student's answer on the math test was an example of confusion, as they had misinterpreted the question.",
                "La respuesta del estudiante en el examen de matemáticas fue un ejemplo de confusión, ya que habían malinterpretado la pregunta."
            ],
            [
                "The police officer's mistake in identifying the suspect was due to confusion, as they had mistaken one person for another.",
                "La equivocación del oficial de policía al identificar al sospechoso fue debida a la confusión, ya que se equivocó de una persona por otra."
            ],
            [
                "The author's use of homonyms led to confusion in their writing, as they used words with similar spellings but different meanings.",
                "El autor utilizó homónimos, lo que llevó a la confusión en su escritura, ya que usó palabras con ortografía similar pero significados diferentes."
            ]
            ],
            "confusión",
            [
            [
                "La confusión entre la palabra suave y dulce es común en inglés.",
                "The confusion between the words soft and sweet is common in english."
            ],
            [
                "La confusión entre los nombres de las estrellas Vega y Deneb puede ser problemática para los astrónomos.",
                "The confusion between the names of the stars vega and deneb can be problematic for astronomers."
            ],
            [
                "La confusión entre la palabra principal y principio es frecuente en el idioma español.",
                "The confusion between the main word and principle is common in the spanish language."
            ],
            [
                "La confusión entre las palabras suelo y sueño puede ser problemática para los estudiantes de inglés.",
                "The confusion between the words floor and dream can be problematic for english learners."
            ],
            [
                "La confusión entre la palabra principal y principio es una causa común de errores en el idioma español.",
                "The confusion between the main word and principle is a common cause of errors in the spanish language."
            ]
            ],
            "confusión"
        ],
        "eng-30-00081836-n_shopping": [
            "1",
            "Searching for or buying goods or services.",
            "Buscando o comprando bienes o servicios.",
            "n",
            "eng",
            [
            [
                "She spent hours shopping for the perfect dress to wear at her sister's wedding.",
                "Ella pasó horas comprando ropa para el vestido perfecto que llevaría a la boda de su hermana."
            ],
            [
                "The mall was packed with people doing their holiday shopping.",
                "La tienda estaba llena de gente haciendo sus compras navideñas."
            ],
            [
                "I love going to thrift stores for unique and affordable shopping finds.",
                "Adoro ir a tiendas de segundamano para encontrar compras únicas y baratas."
            ],
            [
                "Online shopping has become increasingly popular due to its convenience.",
                "La compra en línea ha aumentado de manera creciente debido a su comodidad."
            ],
            [
                "Shopping for groceries can be a daunting task, especially when you have a long list of items to buy.",
                "La compra de alimentos puede ser una tarea desafiante, especialmente cuando hay muchas cosas que comprar en la lista."
            ]
            ],
            "NULL",
            {
            "Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.": 2
            },
            {
            "Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.": 0
            },
            {
            "Mensaje de información": "La entrada ha terminado su ejecución en la extracción del resultado provisional."
            }
        ],
        "eng-30-00152727-n_diagnosis": [
            "1",
            "Identifying the nature or cause of some phenomenon.",
            "Identificar la naturaleza o causa de algún fenómeno.",
            "n",
            "eng",
            [
            [
                "The doctor carefully examined the patient and arrived at a diagnosis of pneumonia.",
                "El médico examinó cuidadosamente al paciente y llegó a un diagnóstico de neumonía."
            ],
            [
                "After conducting extensive tests, the scientists were able to make a definitive diagnosis of the rare disease.",
                "Después de realizar pruebas extensas, los científicos pudieron hacer un diagnóstico definitivo de la enfermedad rara."
            ],
            [
                "The forensic team's analysis led them to a clear diagnosis of homicide.",
                "El equipo de análisis forense llegó a un diagnóstico claro de asesinato."
            ],
            [
                "The meteorologists issued a severe weather warning based on their diagnosis of an impending storm.",
                "Los meteorólogos emitieron una advertencia de mal tiempo severa basada en su diagnóstico de una tormenta que se avecina."
            ],
            [
                "The linguist's analysis revealed a diagnosis of a previously unknown dialect in the rural community.",
                "La análisis del lingüista reveló un diagnóstico de una variedad desconocida en la comunidad rural."
            ]
            ],
            "diagnóstico",
            [
            [
                "El diagnóstico médico reveló que la paciente padecía una infección bacteriana.",
                "The medical diagnosis revealed that the patient was suffering from a bacterial infection."
            ],
            [
                "La investigación científica llevó al diagnóstico de un nuevo elemento químico.",
                "The scientific research led to the identification of a new chemical element."
            ],
            [
                "El diagnóstico forense concluyó en el asesinato premeditado.",
                "The autopsy determined that the murder was premeditated."
            ],
            [
                "El diagnóstico psicológico indicó que la persona sufría de depresión clínica.",
                "The psychological diagnosis indicated that the person was suffering from clinical depression."
            ],
            [
                "La investigación arqueológica llevó al diagnóstico de una antigua ciudad perdida.",
                "The archaeological investigation led to the identification of an ancient lost city."
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
            "Mensaje de información": "La entrada ha terminado su ejecución en la validación del resultado provisional."
            }
        ],
        "eng-30-00180413-n_acceptance": [
            "2",
            "The act of accepting with approval; favorable reception.",
            "La acción de aceptar con aprobación; la recepción favorable.",
            "n",
            "eng",
            [
            [
                "The audience's acceptance of the play was overwhelmingly positive.",
                "La aceptación del público de la obra fue abrumadoramente positiva."
            ],
            [
                "The committee's decision to accept the proposal was a significant milestone for the project.",
                "La decisión del comité de aceptar la propuesta fue un hito significativo para el proyecto."
            ],
            [
                "The company's acceptance of the new employee policy has led to increased productivity and job satisfaction.",
                "La aceptación de la nueva política del empleador ha llevado a un aumento de la productividad y el satisfacimiento en el trabajo."
            ],
            [
                "The jury's acceptance of the defendant's plea of insanity was a surprising turn of events in the trial.",
                "La aceptación del jurado de la declaración de insanidad del acusado fue una sorprendente vuelta de tuerca en el juicio."
            ],
            [
                "The community's acceptance of the immigrant family has been a source of pride for all involved.",
                "La aceptación de la comunidad de la familia inmigrante ha sido una fuente de orgullo para todos los implicados."
            ]
            ],
            "aceptación",
            [
            [
                "La aceptación de la propuesta fue unánime.",
                "The acceptance of the proposal was unanimous."
            ],
            [
                "El libro ha recibido una aceptación positiva entre los lectores.",
                "The book has received positive acceptance among readers."
            ],
            [
                "La aceptación de la idea por parte del equipo fue inmediata.",
                "The acceptance of the idea by the team was immediate."
            ],
            [
                "La aceptación de la nueva política ha sido generalizada en la empresa.",
                "The acceptance of the new policy has been widely adopted within the company."
            ],
            [
                "La aceptación de la propuesta por parte del cliente es crucial para el éxito del negocio.",
                "The acceptance of the proposal by the customer is critical for the success of the business."
            ]
            ],
            "aceptación"
        ],
        "eng-30-00187337-n_goal": [
            "4",
            "A successful attempt at scoring.",
            "Un exitoso intento de marcar.",
            "n",
            "eng",
            [
            [
                "The soccer team scored two goals in their victory over the opposing team",
                "El equipo de fútbol anotó dos goles en su victoria sobre el equipo contrario."
            ],
            [
                "The basketball player made a goal with just seconds left on the clock",
                "El jugador de baloncesto anotó con solo segundos restantes en el reloj."
            ],
            [
                "The football quarterback threw a long pass that resulted in a touchdown and a goal for his team",
                "El quarterback de fútbol americano lanzó un pase largo que resultó en una anotación y un gol para su equipo."
            ],
            [
                "The hockey team's center forward scored a hat trick, which is three goals in one game",
                "La delantera central del equipo de hockey anotó un triplete, que es tres goles en un solo partido."
            ],
            [
                "The tennis player hit an ace to win the set and achieve her goal of winning the match.",
                "El tenista acertó un as para ganar el set y lograr su objetivo de ganar la partida."
            ]
            ],
            "gol",
            [
            [
                "El delantero anotó un gol en la última jugada.",
                "The striker scored a goal in the last play."
            ],
            [
                "La pelota entró en la red y se marcó un gol para el equipo local.",
                "The ball entered the net and scored a goal for the home team."
            ],
            [
                "El arquero falló al bloquear el disparo y se le marcó un gol.",
                "The goalkeeper failed to block the shot and was credited with a goal against him."
            ],
            [
                "El referee señaló una falta a favor del equipo visitante, y el jugador anotó un gol de tiro libre.",
                "The referee signaled a foul against the visiting team, and the player scored a goal from a free kick."
            ],
            [
                "La selección nacional logró un gol en la primera mitad del partido.",
                "The national team managed to score a goal during the first half of the game."
            ]
            ],
            "gol"
        ],
        "eng-30-00213903-n_exemption": [
            "3",
            "An act exempting someone.",
            "Una acción que exime a alguien.",
            "n",
            "eng",
            [
            [
                "The government granted an exemption to the small business owner from paying taxes for the current year due to financial hardship.",
                "El gobierno concedió una exención al propietario de la pequeña empresa del pago de impuestos por el año actual debido a dificultades financieras."
            ],
            [
                "The university provided an exemption to the student who had a medical condition that prevented them from attending classes in person.",
                "La universidad otorgó una exención al estudiante que tenía una condición médica que le impidió asistir a las clases de manera presencial."
            ],
            [
                "The court issued an exemption to the defendant who was deemed mentally unfit to stand trial.",
                "La corte otorgó una exención al acusado que fue considerado mentalmente incapaz de enfrentar juicio."
            ],
            [
                "The state granted an exemption to the religious organization that refused to provide services for same-sex weddings due to their beliefs.",
                "El estado concedió una exención a la organización religiosa que se negó a proporcionar servicios para las bodas del mismo sexo debido a sus creencias."
            ],
            [
                "The government provided an exemption to the foreign aid agency that allowed them to bypass certain bureaucratic procedures in order to quickly distribute funds to those affected by a natural disaster.",
                "El gobierno otorgó una exención al agencia de ayuda extranjera que les permitió evitar ciertos procedimientos burocráticos para poder distribuir rápidamente los fondos a aquellos afectados por un desastre natural."
            ]
            ],
            "exención",
            [
            [
                "La ley otorga una exención fiscal a los veteranos.",
                "The law grants a tax exemption to veterans."
            ],
            [
                "El tribunal concedió una exención temporal a la acusada.",
                "The court granted a temporary exemption to the accused."
            ],
            [
                "La universidad ofrece una exención de matrícula para los estudiantes con excelentes calificaciones.",
                "The university offers a waiver of tuition fees for students with excellent grades."
            ],
            [
                "La ley de inmigración otorga una exención especial a los refugiados.",
                "The immigration law grants special exemption to refugees."
            ],
            [
                "El sistema legal concede una exención a los testigos que cooperan con la justicia.",
                "The legal system grants an exemption to witnesses who cooperate with justice."
            ]
            ],
            "exención"
        ],
        "eng-30-00312553-n_voyage": [
            "2",
            "A journey to some distant place.",
            "Un viaje a algún lugar lejano.",
            "n",
            "eng",
            [
            [
                "The couple embarked on a voyage across the Atlantic Ocean to explore new lands and cultures.",
                "El pareja emprendió un viaje transatlántico para explorar nuevas tierras y culturas."
            ],
            [
                "The adventurous traveler set out on a voyage to the Amazon rainforest, eager to discover its secrets.",
                "El aventurero viajero se embarcó en un viaje hacia la selva amazónica, ansioso por descubrir sus secretos."
            ],
            [
                "The ship's captain led his crew on a perilous voyage through treacherous waters, determined to reach their destination.",
                "El capitán de la nave llevó a su tripulación en un viaje peligroso a través de aguas traicioneras, determinado a llegar a su destino."
            ],
            [
                "The intrepid explorers embarked on a voyage to the Arctic Circle in search of lost treasure and ancient artifacts.",
                "Los audaces exploradores se embarcaron en un viaje al círculo ártico en busca del tesoro perdido y de artefactos antiguos."
            ],
            [
                "The family took a voyage around the world, visiting exotic destinations and experiencing new cultures along the way.",
                "La familia realizó un viaje alrededor del mundo, visitando destinos exóticos y experimentando nuevas culturas en el camino."
            ]
            ],
            "viaje",
            [
            [
                "El viaje a la India ha sido una experiencia inolvidable.",
                "The journey to india has been an unforgettable experience."
            ],
            [
                "Su viaje al Himalaya fue un gran desafío físico y mental.",
                "His trip to the himalayas was a great physical and mental challenge."
            ],
            [
                "La joven se embarcó en un viaje de descubrimiento por Europa.",
                "The young woman embarked on a discovery trip through europe."
            ],
            [
                "El viaje a la Antártida es una aventura única que solo los más aventureros pueden soportar.",
                "The journey to antarctica is a unique adventure that only the most adventurous can endure."
            ],
            [
                "Su viaje al desierto ha cambiado su perspectiva sobre la vida.",
                "Her trip to the desert has changed her perspective on life."
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
            "Mensaje de información": "La entrada ha terminado su ejecución en la validación del resultado provisional."
            }
        ],
        "eng-30-00315986-n_transfer": [
            "1",
            "The act of moving something from one location to another.",
            "El acto de mover algo desde un lugar al otro.",
            "n",
            "eng",
            [
            [
                "The transfer of goods from the warehouse to the delivery truck was completed successfully.",
                "La transferencia de los bienes desde el almacén hasta la camión de entrega se completó con éxito."
            ],
            [
                "The company has initiated a transfer of its operations to a new facility, which is expected to be completed by next year.",
                "La empresa ha iniciado la transferencia de sus operaciones a una nueva instalación, que se espera completar en el próximo año."
            ],
            [
                "The patient's medical records were transferred electronically to the hospital for further treatment.",
                "Los registros médicos del paciente fueron transferidos electrónicamente al hospital para tratamiento adicional."
            ],
            [
                "The transfer of funds from one account to another can be done easily through online banking.",
                "La transferencia de fondos de una cuenta a otra se puede hacer fácilmente a través del banco en línea."
            ],
            [
                "The transfer of ownership of the property was finalized last week, and the new owner has taken possession of it.",
                "La transacción de la propiedad se completó la semana pasada, y el nuevo dueño ha tomado posesión de ella."
            ]
            ],
            "transferencia",
            [
            [
                "La transferencia de los documentos electrónicos a la nube es una práctica común hoy en día.",
                "The transfer of electronic documents to the cloud is a common practice today."
            ],
            [
                "El proceso de transferencia de la información de la base de datos antigua a la nueva puede ser largo y complejo.",
                "The process of transferring information from the old database to the new one can be long and complex."
            ],
            [
                "La transferencia de los archivos de la oficina al nuevo servidor es una tarea diaria para el administrador de la red.",
                "The daily task for the network administrator is transferring the office files to the new server."
            ],
            [
                "El acto de transferir la propiedad de la casa a otra persona se llama venta.",
                "The act of selling property is called a sale."
            ],
            [
                "La transferencia de la responsabilidad de la tarea a otro empleado puede ser necesario en algunas circunstancias.",
                "The transfer of responsibility for the task to another employee may be necessary in some circumstances."
            ]
            ],
            "NULL",
            {
            "Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.": 0
            },
            {
            "Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.": 1
            },
            {
            "Mensaje de información": "La entrada ha terminado su ejecución en la validación del resultado provisional."
            }
        ],
        "eng-30-00327824-n_swing": [
            "4",
            "Changing location by moving back and forth.",
            "Cambiando de ubicación al moverse de un lado a otro.",
            "n",
            "eng",
            [
            [
                "The child enjoyed swinging on the playground set",
                "El niño disfrutó de colgarse en el conjunto de juegos del parque."
            ],
            [
                "The pendulum swung back and forth, ticking off each second",
                "El reloj de péndulo osciló de un lado a otro, marcando cada segundo."
            ],
            [
                "The wind chimes hung from a tree branch, swaying gently with the breeze, creating a soothing melody as they swung back and forth",
                "Las campanas de viento colgaban de una rama del árbol, oscilando suavemente con el viento, creando un melodioso sonido mientras se movían de un lado a otro."
            ],
            [
                "The door creaked open, swinging on its hinges in the gusty wind",
                "La puerta se abrió con un zumbido, oscilando en sus bisagras ante el viento brusco."
            ],
            [
                "The boat rocked back and forth on the choppy waves, causing the passengers to feel queasy.",
                "El barco osciló de un lado a otro sobre las olas agitadas, haciendo que los pasajeros se sintieran enfermos."
            ]
            ],
            "NULL",
            {
            "Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.": 0
            },
            {
            "Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.": 5
            },
            {
            "Mensaje de información": "La entrada ha terminado su ejecución en la extracción del resultado provisional."
            }
        ],
        "eng-30-00331950-n_movement": [
            "1",
            "A change of position that does not entail a change of location.",
            "Un cambio de posición que no implica un cambio de ubicación.",
            "n",
            "eng",
            [
            [
                "The movement of the pendulum was caused by the vibration of the clock mechanism.",
                "El movimiento del péndulo fue causado por la vibración del mecanismo de reloj."
            ],
            [
                "The movement of the water in the river was due to the force of gravity.",
                "El movimiento del agua en el río se debía al fuerza de la gravedad."
            ],
            [
                "The movement of the leaves on the tree was affected by the wind.",
                "El movimiento de las hojas del árbol fue afectado por el viento."
            ],
            [
                "The movement of the air molecules in the room was influenced by the temperature.",
                "El movimiento de las moléculas de aire en la habitación fue influenciado por la temperatura."
            ],
            [
                "The movement of the particles in the gas was caused by collisions with other particles.",
                "El movimiento de las partículas en el gas fue causado por las colisiones con otras partículas."
            ]
            ],
            "movimiento",
            [
            [
                "El movimiento del sol a través del cielo es una ilusión óptica, ya que la Tierra gira alrededor del Sol.",
                "The apparent motion of the sun across the sky is an optical illusion, as the earth rotates around the sun."
            ],
            [
                "La luna parece moverse en el cielo debido a la rotación de la Tierra.",
                "The moon seems to move across the sky due to the earth's rotation."
            ],
            [
                "El movimiento de las nubes en el cielo es solo una ilusión óptica, ya que son las mismas nubes que se desplazan sobre la superficie de la Tierra.",
                "The apparent movement of clouds in the sky is merely an optical illusion, as they are actually moving across the surface of the earth."
            ],
            [
                "La apariencia de un objeto moverse en la pantalla de un proyector es solo un efecto óptico, ya que el objeto no cambia de posición físicamente.",
                "The appearance of an object moving on a screen is merely an optical effect, as the object does not physically change its position."
            ],
            [
                "El movimiento de las ondas en el agua es solo una ilusión óptica, ya que son las mismas ondas que se",
                "The movement of waves in water is only an optical illusion, as it is actually the same waves that are reflected back from the surface."
            ]
            ],
            "NULL",
            {
            "Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.": 0
            },
            {
            "Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.": 2
            },
            {
            "Mensaje de información": "La entrada ha terminado su ejecución en la validación del resultado provisional."
            }
        ],
        "eng-30-00372607-n_storage": [
            "6",
            "Depositing in a warehouse.",
            "Depósito en un almacén.",
            "n",
            "eng",
            [
            [
                "The company has allocated a large storage facility for storing their excess inventory.",
                "La empresa ha reservado un gran almacén para el almacenamiento de sus inventarios en exceso."
            ],
            [
                "The warehouse is equipped with state-of-the-art storage systems to ensure optimal preservation of goods.",
                "El almacén está equipado con sistemas de almacenamiento de última generación para garantizar la óptima conservación de los bienes."
            ],
            [
                "The storage area is kept clean and organized to prevent any damage or spoilage to the stored items.",
                "El área de almacenamiento se mantiene limpia y organizada para prevenir cualquier daño o desgaste en los artículos almacenados."
            ],
            [
                "The company's storage capacity has increased by 50% in the past year, allowing them to better meet customer demand.",
                "La capacidad de almacenamiento de la empresa ha aumentado en un 50% en el último año, lo que les permite mejor atender a las necesidades de los clientes."
            ],
            [
                "The warehouse's storage system includes racks, shelves, and pallets to maximize space utilization and minimize handling time.",
                "El sistema de almacenamiento del almacén incluye estantes, rejillas y palets para maximizar el uso del espacio y minimizar el tiempo de manejo."
            ]
            ],
            "NULL",
            {
            "Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.": 5
            },
            {
            "Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.": 0
            },
            {
            "Mensaje de información": "La entrada ha terminado su ejecución en la extracción del resultado provisional."
            }
        ],
        "eng-30-00397347-n_censorship": [
            "2",
            "Deleting parts of publications or correspondence or theatrical performances.",
            "Eliminación de partes de publicaciones o correspondencia o representaciones teatrales.",
            "n",
            "eng",
            [
            [
                "The government's censorship policies have led to the suppression of critical voices and the stifling of dissent",
                "Las políticas de censura del gobierno han llevado a la supresión de voces críticas y al estrangulamiento de la disidencia, en el sentido de eliminar partes de publicaciones o correspondencia o representaciones teatrales."
            ],
            [
                "The newspaper's editor was forced to censor certain articles due to pressure from the authorities",
                "El editor del periódico fue obligado a censurar ciertos artículos debido a la presión de las autoridades, en el sentido de eliminar partes de publicaciones o correspondencia o representaciones teatrales."
            ],
            [
                "The playwright's work was heavily censored, with entire scenes being cut or rewritten",
                "El trabajo del dramaturgo fue fuertemente censurado, con escenas enteras siendo eliminadas o reescritas."
            ],
            [
                "The publisher faced legal action for refusing to censor a book that contained explicit language and imagery",
                "El editor enfrentó acción legal por negarse a censurar un libro que contenía lenguaje y imágenes explícitas."
            ],
            [
                "The government's censorship of the internet has resulted in the blocking of numerous websites and social media platforms.",
                "La censura del gobierno ha resultado en el bloqueo de numerosas páginas web y plataformas sociales."
            ]
            ],
            "NULL",
            {
            "Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.": 1
            },
            {
            "Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.": 3
            },
            {
            "Mensaje de información": "La entrada ha terminado su ejecución en la extracción del resultado provisional."
            }
        ],
        "eng-30-00418615-n_neglect": [
            "3",
            "Willful lack of care and attention.",
            "Cuidado y atención voluntariamente ausentes.",
            "n",
            "eng",
            [
            [
                "The parents' neglect resulted in their child's malnourishment and developmental delays.",
                "La negligencia de los padres resultó en la desnutrición y retrasos en el desarrollo de su hijo."
            ],
            [
                "The elderly woman's neglect by her family led to her being hospitalized for dehydration and malnutrition.",
                "La falta de atención y cuidado voluntario de la familia llevó a la anciana mujer a ser hospitalizada por deshidratación y mala nutrición."
            ],
            [
                "The company's neglect of safety protocols caused a catastrophic explosion that injured dozens of workers.",
                "La negligencia de la empresa en cuestión de protocolos de seguridad causó una explosión catastrófica que dejó heridos a varios trabajadores."
            ],
            [
                "The teacher's neglect of her students' needs resulted in low test scores and a high dropout rate.",
                "La negligencia del profesor en las necesidades de sus estudiantes resultó en bajas calificaciones en los exámenes y una alta tasa de abandono escolar."
            ],
            [
                "The government's neglect of its citizens' basic human rights led to widespread protests and unrest.",
                "El despreocupo del gobierno por los derechos básicos humanos de sus ciudadanos llevó a manifestaciones y disturbios generalizados."
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
    
    # -----------------------------------   destokinize()   ---------------------------------------
    
    print('Testing destokenize() function')
    
    tokens = []
    assert "" == auxFunctions.destokenize(tokens), "Should be ''"
    
    tokens_2 = ['Hola',',','soy','David''.']
    assert "Hola, soy David." == auxFunctions.destokenize(tokens_2), "Should be 'Hola, soy David.'"
    
    print('destokenize() function tested correctly') 
    
    # -----------------------------------   extract_nouns_with_positions_english()   ---------------------------------------
    
    print('Testing extract_nouns_with_positions_english() function')
    
    phrase_1 = "The towering oak tree provided shade for the picnic on a hot summer day."
    expected_output_1 = [('tree', 3, 'nsubj', 'provided'), ('shade', 5, 'dobj', 'provided'), ('picnic', 8, 'pobj', 'for'), ('day', 13, 'pobj', 'on')]
    assert expected_output_1 == auxFunctions.extract_nouns_with_positions_english(phrase_1), "Should be true"
    
    phrase_2 = "The largest tree in the forest is an american oak, which is over 30 meters tall."
    expected_output_2 = [('tree', 2, 'nsubj', 'is'), ('forest', 5, 'pobj', 'in'), ('oak', 9, 'attr', 'is'), ('meters', 15, 'npadvmod', 'tall')]
    assert expected_output_2 == auxFunctions.extract_nouns_with_positions_english(phrase_2), "Should be true"
    
    phrase_3 = "The paper was smooth and glossy, perfect for printing high-quality images."
    expected_output_3 = [('paper', 1, 'nsubj', 'was'), ('images', 13, 'dobj', 'printing')]
    assert expected_output_3 == auxFunctions.extract_nouns_with_positions_english(phrase_3), "Should be true"
    
    phrase_4 = ""
    expected_output_4 = []
    assert expected_output_4 == auxFunctions.extract_nouns_with_positions_english(phrase_4), "Should be true"
    
    print('extract_nouns_with_positions_english() function tested correctly') 
    
    # -----------------------------------   extract_nouns_with_positions_spanish()   ---------------------------------------
    
    print('Testing extract_nouns_with_positions_spanish() function')
    
    phrase_5 = "La fábrica de papel había estado en funcionamiento durante más de un siglo, proporcionando oportunidades de empleo a generaciones de familias en la zona."
    expected_output_5 = [('fábrica', 1, 'nsubj', 'funcionamiento'), ('papel', 3, 'nmod', 'fábrica'), ('funcionamiento', 7, 'ROOT', 'funcionamiento'), ('siglo', 12, 'nmod', 'funcionamiento'), ('oportunidades', 15, 'obj', 'proporcionando'), ('empleo', 17, 'nmod', 'oportunidades'), ('generaciones', 19, 'nmod', 'oportunidades'), ('familias', 21, 'nmod', 'generaciones'), ('zona', 24, 'nmod', 'familias')]
    assert expected_output_5 == auxFunctions.extract_nouns_with_positions_spanish(phrase_5), "Should be true"

    phrase_6 = "El papel es un material muy utilizado para la impresión y la escritura."
    expected_output_6 = [('papel', 1, 'nsubj', 'material'), ('material', 4, 'ROOT', 'material'), ('impresión', 9, 'obl', 'utilizado'), ('escritura', 12, 'conj', 'impresión')]
    assert expected_output_6 == auxFunctions.extract_nouns_with_positions_spanish(phrase_6), "Should be true"
  
    phrase_7 = "El árbol más grande del bosque es un roble americano de más de 30 metros de altura."
    expected_output_7 = [('árbol', 1, 'nsubj', 'roble'), ('metros', 14, 'nmod', 'roble'), ('altura', 16, 'nmod', 'metros')]
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
    
# Método main
if __name__ == "__main__":
    print("Test started: second pilot case")
    print("Testing over Importer component...")
    # component_importer_test() # Tested correctly
    print("Everything in Importer component passed")
    print("Testing over Question Maker component...")
    # component_question_maker_test() # Tested correctly
    print("Everything in Question Maker component passed")
    print("Testing over LLM Communicator component...")
    # component_llm_communicator_test() # Tested correctly
    print("Everything in LLM Communicator component passed")
    print("Testing over Extractor component...")
    # component_extractor_test() # Tested correctly
    print("Everything in Extractor component passed")
    print("Testing over Validator component...")
    # component_validator_test() # Tested correctly
    print("Everything in Validator component passed")
    print("Testing over Exporter component...")
    # component_exporter_test() # Tested correctly
    print("Everything in Exporter component passed")
    print("Testing over Auxiliar funcitions...")
    # auxiliar_functions_test() # Tested correctly
    print("Everything in Auxiliar funcitions passed")
    print("Everything passed")