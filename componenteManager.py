

import json
from configparser import ConfigParser
import sys
sys.path.append("./auxFunctionLibrary")
from pythonLib import auxFunctions
from componenteImporter import ComponenteImporter
import componenteQuestionMaker_extraccion
import componenteQuestionMaker_validacion
import componenteQuestionMaker_traduccionGlosa
import componenteQuestionMaker_traduccionInglesEspañol
import componenteQuestionMaker_traduccionEspañolIngles
from componenteLLMCommunicator import ComponenteLLMCommunicator
import componenteExtractor_faseExtraccion
import componenteExtractor_faseValidacion
import componenteExtractor_traduccion
import componenteExtractor_conjuntoFrases
from componenteExporter import ComponenteExporter


def knowledge_exploitation_process():
    
    """
    Método para llevar a cabo el proceso completo de explotación de conocimiento en LLMs.
                    
        Retorna:
            - knowledge_table (dic): Diccionario que contiene el conocimiento extraído junto a otros atributos.
    """
    
    print('Knowledge exploitation process STARTED')
    
    config = ConfigParser()
    config.read('./config.ini')
    
    # Ruta del archivo donde escribir la estructura de datos 'knowledge_table'
    file_path_knowledge_table_json = config['file_path']['knowledge_table']
    
    # Componente Importer para importar los datos de las fuentes 
    componenteImporter = ComponenteImporter(config['file_path']['eng_variant_file'], config['file_path']['eng_synset_file'], config['file_path']['most_used_words_eng_file'])
    
    # componente LLMCommunicator para la fase de extracción y validación
    componenteLLMCommunicator = ComponenteLLMCommunicator(config['file_path']['language_model_path'])
    
    # Carga del modelo de lenguaje
    componenteLLMCommunicator.load_model()
    
    # Estructura de datos con la que realizar el proceso de explotación de conocimiento
    knowledge_table = componenteImporter.generate_data_structure()
    
    # Fase 1: Recorrer el 'knowledge_table' para conseguir por cada entrada un conjunto de frases en la que aparece el word y sense
    # de un elemento del 'knowledge_table', con sus respectivas traducciones
    for (offset_word, attributes) in knowledge_table.items():
        llm_trads_answer_list = []
        prompt_list = componenteQuestionMaker_extraccion.generate_prompts((offset_word,attributes))
        for prompt in prompt_list:
            # Realizar la pregunta al modelo de lenguaje 
            llm_answer = componenteLLMCommunicator.run_the_model(prompt)
            attributes["Extraction LLM answers"] = [llm_answer]
            # Extraer la parte de la respuesta para su posterior tratado
            (offset_word, attributes) = componenteExtractor_conjuntoFrases.get_result((offset_word,attributes), [llm_answer])
            # Obtener los prompts
            trad_prompt_list = componenteQuestionMaker_traduccionInglesEspañol.generate_prompts((offset_word, attributes))
            # Recorrer las frases
            for trad_prompt in trad_prompt_list:
                # Traducirla al español
                translated_llm_answer = componenteLLMCommunicator.run_the_model(trad_prompt)
                # Añadirlo a la lista
                llm_trads_answer_list.append(translated_llm_answer)
        # Obtener los prompts  
        gloss_prompt_list = componenteQuestionMaker_traduccionGlosa.generate_prompts((offset_word, attributes))     
        # Traducir el gloss al español
        translated_gloss_llm_answer = componenteLLMCommunicator.run_the_model(gloss_prompt_list[0])
        # Extraer la parte de la respuesta para su posterior tratado
        (offset_word, attributes) = componenteExtractor_traduccion.get_result((offset_word, attributes), [translated_gloss_llm_answer])
        # Añadirlo al knowledge_table
        attributes["Extraction LLM answers"] = [attributes["Extraction LLM answers"][0], llm_trads_answer_list]
        # Conseguir el element del knowledge_table con el resultado de la fase de extracción en
        # base a lo devuelto por el modelo de lenguaje
        (offset_word, attributes) = componenteExtractor_faseExtraccion.get_result((offset_word,attributes),[attributes["Extraction LLM answers"][0], llm_trads_answer_list])

    # Fase 2: Validar los resultados de la fase de extracción que no tengan NULL como valor. 
    # Para ello, se procede a recorrer el 'knowledge_table' para conseguir por cada entrada un conjunto
    # de frases en español en las que aparecen el 
    #     - word (Extraction translation answer) 
    #     - sense (Traducido del inglés)
    # con sus respectivas traducciones al inglés.
    for (offset_word, attributes) in knowledge_table.items():
        llm_trads_answer_list = []
        extraction_translation = attributes["Extraction translation"]
        if extraction_translation != "NULL":
            prompt_list = componenteQuestionMaker_validacion.generate_prompts((offset_word,attributes))
            for prompt in prompt_list:
                # Realizar la pregunta al modelo de lenguaje 
                llm_answer = componenteLLMCommunicator.run_the_model(prompt)
                attributes["Validation LLM answers"] = [llm_answer]
                # Extraer la parte de la respuesta para su posterior tratado
                (offset_word, attributes) = componenteExtractor_conjuntoFrases.get_result((offset_word, attributes), [llm_answer])
                # Obtener los prompts
                trad_prompt_list = componenteQuestionMaker_traduccionEspañolIngles.generate_prompts((offset_word, attributes))
                # Recorremos las frases
                for trad_prompt in trad_prompt_list:
                    # Traducirla al inglés
                    translated_llm_answer = componenteLLMCommunicator.run_the_model(trad_prompt)
                    # Añadirlo a la lista
                    llm_trads_answer_list.append(translated_llm_answer)
            # Añadirlo al knowledge_table
            attributes["Validation LLM answers"] = [attributes["Validation LLM answers"][0], llm_trads_answer_list]
            # Modificar element
            (offset_word, attributes) = componenteExtractor_faseValidacion.get_result((offset_word,attributes), [attributes["Validation LLM answers"][0], llm_trads_answer_list])
        
    print('Knowledge exploitation process FINISHED')
    
    # Generar un JSON con la estructura de datos, para una mejor visualizacion
    json_knowledge_table = json.dumps(knowledge_table, indent=2, ensure_ascii=False)
    
    # Guardar el 'knowledge_table' en formato json en un archivo    
    auxFunctions.save_json(file_path_knowledge_table_json,json_knowledge_table)
    
    # Inicializar la instancia del Componente Exporter con la ruta del archivo a exportar
    componenteExporter = ComponenteExporter(config['file_path']['knowledge_table_file_path'])
    
    print('Knowledge export process STARTED')
    componenteExporter.export_knowledge(knowledge_table)
    print('Knowledge export process FINISHED')
    
    return knowledge_table

if __name__ == "__main__":
    knowledge_exploitation_process()