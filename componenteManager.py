

import json
from configparser import ConfigParser
import re

from componenteImporter import ComponenteImporter
import componenteQuestionMaker
from componenteLLMCommunicator import ComponenteLLMCommunicator
import componenteExtractor
from componenteValidator import ComponenteValidator
from componenteExporter import ComponenteExporter


def knowledge_exploitation():
    
    config = ConfigParser()
    config.read('./config.ini')
    
    # Ruta del archivo donde escribir la estructura de datos 'source_information'
    file_path_source_information_json = config['file_path']['source_information']
    
    # Inicializamos el ComponenteImporter para importar los datos de las fuentes 
    componenteImporter = ComponenteImporter(config['file_path']['eng_variant_file'], config['file_path']['eng_synset_file'], config['file_path']['most_used_words_spa_file'])
    
    # Inicializamos el componenteLLMCommunicator con el llm que vamos a utilizar para conseguir las respuestas provisionales
    componenteLLMCommunicator_provisional = ComponenteLLMCommunicator(config['file_path']['provisional_answers_language_model_path'])
    
    # Cargamos el modelo de lenguaje que vamos a utilizar para conseguir las respuestas provisionales
    componenteLLMCommunicator_provisional.load_model()
    
    # Generar la estructura de datos con la que realizar el proceso de explotación de conocimiento
    source_information = componenteImporter.generate_data_structure()
    
    # Creamos la estructura de datos que guardará el conocimiento que se haya explotado en los modelos de lenguaje, 
    # junto con la información extraída de la(s) fuente(s).
    exploited_information = {}
    
    # Recorrer el 'source_information', para conseguir frases en las que aparezca la palabra con el gloss
    for (offset_word, attributes) in source_information.items():
        llm_extracted_provisional_answers_list = []
        provisional_prompt_list = componenteQuestionMaker.generate_provisional_prompts((offset_word,attributes))
        for prompt in provisional_prompt_list:
            # Realizar la pregunta al modelo de lenguaje 
            llm_answer = componenteLLMCommunicator_provisional.run_the_model(prompt)
            # Extraer la parte de la respuesta para su posterior tratado
            llm_extracted_answer = componenteExtractor.extract_llm_answers(llm_answer)
            # Recorremos las frases
            for phrase in llm_extracted_answer:
                # Traducirla al español
                translated_llm_answer = componenteLLMCommunicator_provisional.run_the_model('Como experto en traducción, necesito una traducción precisa al español de la siguiente frase: "' + phrase +'".')
                # Extraer la parte de la respuesta para su posterior tratado
                translated_llm_extracted_answer = componenteExtractor.extract_llm_answers(translated_llm_answer)
                # Añadirlo a la lista
                llm_extracted_provisional_answers_list.append([phrase, translated_llm_extracted_answer])
        # Añadirlo al source_information
        item_list = [attributes[0], attributes[1], attributes[2], attributes[3], llm_extracted_provisional_answers_list]
        exploited_information[offset_word] = item_list
        source_information[offset_word] = item_list
    
    # Recorrer el 'source_information', para ver que si no tiene el gloss (está NULL) acceder al de
    # 'source_gloss_structure_eng' y traducirlo
    # for offset_word, element in source_information.items():
    #     if element[1] == 'NULL':
    #         offset = offset_word.split('_')[0]
    #         eng_gloss = source_gloss_structure_eng[offset]
    #         llm_answer = componenteLLMCommunicator_provisional.run_the_model('Como experto en traducción, necesito una traducción precisa al español de la siguiente frase: "' + eng_gloss +'".')
    #         spa_gloss = componenteExtractor.extract_llm_answers(llm_answer)
    #         if type(spa_gloss) is list:
    #             if len(spa_gloss) > 0:
    #                 spa_gloss = spa_gloss[0]
    #             elif len(spa_gloss) == 0:
    #                 spa_gloss = ""
    #         spa_gloss = spa_gloss.split(". ")[0].strip()
    #         if ": " in spa_gloss and ": " not in eng_gloss:
    #             spa_gloss = spa_gloss.split(': ')[0]
    #         if not spa_gloss.endswith('.'):
    #             spa_gloss += '.'
    #         spa_gloss = spa_gloss.strip().replace('"', '').replace("\"", "").replace('\\', '').replace("\\\"", "").capitalize()
    #         source_information[offset_word] = [element[0], spa_gloss, element[2], element[3]]
            
    
    # Explotar conocimiento (Al parecer da problemas si se cargan dos modelos a la vez, 
    # ya que ocupa demasiada memoria y ralentiza el proceso de forma importante)
    # Es por ello que se recorrerá el source_information dos veces:
    #     La primera para conseguir las respuesta provisionales, y para validar las que tienen 'Neutro' como resultado provisional
    #     La segunda para validar las que tienen el valor del resultado provisional 'Femenino' o 'Masculino'
    
    # for (offset_word,attributes) in source_information.items():
    #     llm_extracted_provisional_answers_list = []  
    #     llm_extracted_final_answers_list = []
    #     provisional_answer = ""
    #     final_answer = ""
        
    #     # (respuesta provisional)
    #     provisional_prompt_list = componenteQuestionMaker.generate_provisional_prompts((offset_word,attributes))
    #     for prompt in provisional_prompt_list:
    #         # Reallizar la pregunta al modelo de lenguaje 
    #         llm_answer = componenteLLMCommunicator_provisional.run_the_model(prompt)
    #         # Extraer la parte de la respuesta para su posterior tratado
    #         llm_extracted_answer = componenteExtractor.extract_llm_answers(llm_answer)
    #         # Añadir la lista de las respuestas al data structure
    #         llm_extracted_provisional_answers_list.append(llm_extracted_answer)
    #     # Conseguir la respuesta provisional en base a lo devuelto por el modelo de lenguaje
    #     provisional_answer = componenteExtractor.get_provisional_answer4((offset_word,attributes),llm_extracted_provisional_answers_list)
            
    #     # Añadirlo al source_information
    #     item_list = [attributes[0], attributes[1], attributes[2], attributes[3], llm_extracted_provisional_answers_list, provisional_answer]
    #     exploited_information[offset_word] = item_list
    #     source_information[offset_word] = item_list
        
    # componenteLLMCommunicator_provisional.llm = None
        
    # # Inicializamos el componenteLLMCommunicator con el llm que vamos a utilizar para validar las respuestas provisionales
    # componenteLLMCommunicator_final = ComponenteLLMCommunicator(config['file_path']['final_answers_language_model_path'])
    
    # # Cargamos el modelo de lenguaje que vamos a utilizar para validar las respuestas provisionales
    # componenteLLMCommunicator_final.load_model()    
    
    # for (offset_word,attributes) in exploited_information.items():    
    #     # (validacion de 'Femenino' o 'Masculino')
    #     final_answer = ""
    #     llm_extracted_final_answers_list = []
    #     if attributes[5] == "Femenino" or attributes[5] == "Masculino":
    #         final_prompt_list = componenteQuestionMaker.generate_validation_prompts((offset_word,attributes), attributes[5])
            
    #         for prompt in final_prompt_list:
    #             # Reallizar la pregunta al modelo de lenguaje 
    #             llm_answer = componenteLLMCommunicator_final.run_the_model(prompt)
    #             # Extraer la parte de la respuesta para su posterior tratado
    #             llm_extracted_answer = componenteExtractor.extract_llm_answers(llm_answer)
    #             # Añadir la lista de las respuestas al data structure
    #             llm_extracted_final_answers_list.append(llm_extracted_answer)
            
    #         # Inicializamos la clase 5 con los datos necesarios
    #         componenteValidator = ComponenteValidator(len(attributes[4][0]))
    #         # Conseguir la respuesta provisional en base a lo devuelto por el modelo de lenguaje
    #         final_answer = componenteValidator.get_final_answer((offset_word,attributes), llm_extracted_final_answers_list, attributes[5])

            
    #     answer = ""
    #     if final_answer == "":
    #         answer = attributes[5]
    #     else:
    #         answer = final_answer
        
    #     # Añadirlo al exploited_information
    #     item_list = [attributes[0], attributes[1], attributes[2], attributes[3], answer]
    #     exploited_information[offset_word] = item_list
    #     source_information[offset_word] = [attributes[0], attributes[1], attributes[2], attributes[3], attributes[4], llm_extracted_final_answers_list, answer]
    
    # Generamos un JSON con la estructura de datos, para una mejor visualizacion
    json_exploited_information = json.dumps(exploited_information, indent=2, ensure_ascii=False)
    
    # Guardar el 'source_information' en formato json en un archivo    
    componenteImporter.save_json(file_path_source_information_json,json_exploited_information)
    
    return exploited_information

def knowledge_exploitation_process():
    
    config = ConfigParser()
    config.read('./config.ini')
    
    print('Knowledge exploitation process STARTED')
    exploited_information = knowledge_exploitation() 
    print('Knowledge exploitation process FINISHED')
    
    # Inicializamos la clase para con la ruta del archivo a exportar
    # componenteExporter = ComponenteExporter(config['file_path']['exploited_information_file_path'])
    
    print('Knowledge export process STARTED')
    # componenteExporter.export_knowledge(exploited_information)
    print('Knowledge export process FINISHED')


if __name__ == "__main__":
    knowledge_exploitation_process()