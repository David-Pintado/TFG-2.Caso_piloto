

import json
from configparser import ConfigParser
import sys
sys.path.append("./auxFunctionLibrary")
from componenteImporter import ComponenteImporter
import componenteQuestionMaker_extraccion
import componenteQuestionMaker_validacion
import componenteQuestionMaker_traduccionGlosa
import componenteQuestionMaker_traduccionInglesEspañol
import componenteQuestionMaker_traduccionEspañolIngles
from componenteLLMCommunicator import ComponenteLLMCommunicator
import componenteExtractor
import componenteValidator
from componenteExporter import ComponenteExporter


def knowledge_exploitation():
    
    config = ConfigParser()
    config.read('./config.ini')
    
    # Ruta del archivo donde escribir la estructura de datos 'knowledge_table'
    file_path_knowledge_table_json = config['file_path']['knowledge_table']
    
    # Componente Importer para importar los datos de las fuentes 
    componenteImporter = ComponenteImporter(config['file_path']['eng_variant_file'], config['file_path']['eng_synset_file'], config['file_path']['most_used_words_spa_file'])
    
    # componente LLMCommunicator para la fase de extracción y validación
    componenteLLMCommunicator = ComponenteLLMCommunicator(config['file_path']['language_model_path'])
    
    # Carga del modelo de lenguaje
    componenteLLMCommunicator.load_model()
    
    # Estructura de datos con la que realizar el proceso de explotación de conocimiento
    knowledge_table = componenteImporter.generate_data_structure()
    
    # Fase 1: Recorrer el 'knowledge_table' para conseguir por cada entrada un conjunto de frases en la que aparece el word y sense
    # de un elemento del 'knowledge_table', con sus respectivas traducciones
    for (offset_word, attributes) in knowledge_table.items():
        word = offset_word.split('_')[1]
        llm_answer_list = []
        prompt_list = componenteQuestionMaker_extraccion.generate_prompts((offset_word,attributes))
        for prompt in prompt_list:
            # Realizar la pregunta al modelo de lenguaje 
            llm_answer = componenteLLMCommunicator.run_the_model(prompt)
            # Extraer la parte de la respuesta para su posterior tratado
            llm_extracted_answer = componenteExtractor.extract_llm_answers(llm_answer)
            # Obtener los prompts
            llm_answer_list[0] = llm_answer
            llm_answer_list[1] = llm_extracted_answer
            attributes[5] = llm_answer_list
            trad_prompt_list = componenteQuestionMaker_traduccionInglesEspañol.generate_prompts((offset_word, attributes))
            # Recorremos las frases
            for trad_prompt in trad_prompt_list:
                # Traducirla al español
                translated_llm_answer = componenteLLMCommunicator.run_the_model(trad_prompt)
                # Añadirlo a la lista
                llm_extracted_provisional_results_list.append([phrase, translated_llm_extracted_answer])
        # Traducir el gloss al español
        translated_gloss_llm_answer = componenteLLMCommunicator.run_the_model('As a translation expert, I need an accurate translation into Spanish of the following phrase: "' + attributes[1] +'".')
        # Extraer la parte de la respuesta para su posterior tratado
        spa_gloss = componenteExtractor.extract_llm_answers(translated_gloss_llm_answer)
        # Añadirlo al knowledge_table
        item_list = [attributes[0], attributes[1], spa_gloss, attributes[2], attributes[3], llm_extracted_provisional_results_list]
        knowledge_table[offset_word] = item_list
    
    # Fase 2: Recorrer el knowledge_table para obtener el resultado de la fase de extraccion
    # Ruta del archivo JSON
    # (FASE 2 completada)
    # file_path = 'files/examples_to_work_with(X).json'

    # # Leer el archivo JSON y convertirlo a un diccionario
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     knowledge_table = json.load(file)
    
    for (offset_word, attributes) in knowledge_table.items():
        # Ahora en forma de pruebas y para ahorrar tiempo llm_extracted_provisional_results_list se va a coger de attributes
        llm_extracted_provisional_results_list = attributes[5]
        # Conseguir el resultado provisional en base a lo devuelto por el modelo de lenguaje
        provisional_result = componenteExtractor.get_provisional_result((offset_word,attributes),llm_extracted_provisional_results_list)
        # Añadirlo al knowledge_table
        if len(provisional_result) == 1:  
            item_list = [attributes[0], attributes[1], attributes[2], attributes[3], attributes[4], llm_extracted_provisional_results_list, provisional_result[0]]
            knowledge_table[offset_word] = item_list
            exploited_information[offset_word] = item_list   
        elif len(provisional_result) == 5:
            item_list = [attributes[0], attributes[1], attributes[2], attributes[3], attributes[4], llm_extracted_provisional_results_list, provisional_result[0], provisional_result[1], provisional_result[2], provisional_result[3], provisional_result[4]]
            knowledge_table[offset_word] = item_list
            exploited_information[offset_word] = item_list    
                
    # Fase 3: Validar las respuestas provisionales que no tengan NULL como valor. Para ello, se va a proceder a recorrer
    # el 'knowledge_table' para conseguir por cada entrada un conjunto de frases en español en las que aparecen el 
    #     - word (Provisional answer) 
    #     - sense (Traducido del inglés)
    # con sus respectivas traducciones
    # (FASE 3 completada)
    for (offset_word, attributes) in knowledge_table.items():
        word = offset_word.split('_')[1]
        llm_extracted_validation_answers_list = []
        provisional_result = attributes[6]
        if provisional_result != "NULL":
            validation_prompt_list = componenteQuestionMaker.generate_validation_prompts((offset_word,attributes), provisional_result)
            for prompt in validation_prompt_list:
                # Realizar la pregunta al modelo de lenguaje 
                llm_answer = componenteLLMCommunicator.run_the_model(prompt)
                # Extraer la parte de la respuesta para su posterior tratado
                llm_extracted_answer = componenteExtractor.extract_llm_answers(llm_answer)
                # Recorremos las frases
                for phrase in llm_extracted_answer:
                   # Traducirla al inglés
                    translated_llm_answer = componenteLLMCommunicator.run_the_model('As an Spanish to English translation expert, I need an accurate translation into English of the Spanish sentence "' + phrase +'", where the noun "' + word + '" appears in the sense "' + attributes[1] + '".')
                    # Extraer la parte de la respuesta para su posterior tratado
                    translated_llm_extracted_answer = componenteExtractor.extract_llm_answers(translated_llm_answer)
                    # Añadirlo a la lista
                    llm_extracted_validation_answers_list.append([phrase, translated_llm_extracted_answer])
            # Añadirlo al knowledge_table
            item_list = [attributes[0], attributes[1], attributes[2], attributes[3], attributes[4], attributes[5], attributes[6], llm_extracted_validation_answers_list]
            exploited_information[offset_word] = item_list
            knowledge_table[offset_word] = item_list 
    
    # Fase 4: Recorrer el knowledge_table para obtener la respuesta final de las entradas de 'knowledge_table'
    # como provisional_result    
    for (offset_word, attributes) in knowledge_table.items():
        # final_result
        final_result = "NULL"
        # Obtener el resultado provisional
        provisional_result = attributes[6]
        # Obtener el word
        word = offset_word.split('_')[1]
        if provisional_result != "NULL":
            # Ahora en forma de pruebas y para ahorrar tiempo llm_extracted_validation_answers_list se va a coger de attributes
            llm_extracted_validation_answers_list = attributes[7]
            # Obtener la respuesta final
            final_result = componenteValidator.get_final_result((offset_word,attributes), llm_extracted_validation_answers_list, provisional_result)
            # Añadirlo al knowledge_table
            if len(final_result) == 1:  
                item_list = [attributes[0], attributes[1], attributes[2], attributes[3], attributes[4], attributes[5], attributes[6], attributes[7], final_result[0]]
                exploited_information[offset_word] = item_list
                knowledge_table[offset_word] = item_list
            elif len(final_result) == 5:
                item_list = [attributes[0], attributes[1], attributes[2], attributes[3], attributes[4], attributes[5], attributes[6], attributes[7], final_result[0], final_result[1], final_result[2], final_result[3], final_result[4]]
                exploited_information[offset_word] = item_list
                knowledge_table[offset_word] = item_list
        
    # Generamos un JSON con la estructura de datos, para una mejor visualizacion
    json_exploited_information = json.dumps(exploited_information, indent=2, ensure_ascii=False)
    
    # Guardar el 'knowledge_table' en formato json en un archivo    
    componenteImporter.save_json(file_path_knowledge_table_json,json_exploited_information)
    
    return exploited_information

def knowledge_exploitation_process():
    
    config = ConfigParser()
    config.read('./config.ini')
    
    print('Knowledge exploitation process STARTED')
    exploited_information = knowledge_exploitation() 
    print('Knowledge exploitation process FINISHED')
    
    # Inicializamos la clase para con la ruta del archivo a exportar
    componenteExporter = ComponenteExporter(config['file_path']['exploited_information_file_path'])
    
    print('Knowledge export process STARTED')
    componenteExporter.export_knowledge(exploited_information)
    print('Knowledge export process FINISHED')


if __name__ == "__main__":
    knowledge_exploitation_process()