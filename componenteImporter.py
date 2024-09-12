import json
import sys
sys.path.append("./auxFunctionLibrary")
from pythonLib import auxFunctions
import random

class ComponenteImporter:
    
    def __init__(self, eng_variant_file, eng_synset_file, most_used_words_file):
        self.eng_variant_file = eng_variant_file 
        self.eng_synset_file = eng_synset_file
        self.most_used_words_file = most_used_words_file

    def generate_data_structure(self):
        
        """
        Método para generar una estructura de datos del WordNet en inglés.
           
            Parámetros:
                - self: instancia de la clase que contiene este método.

            Retorna:
                - knowledge_table (dict): Un diccionario que contiene los datos necesarios del WordNet en castellano
                                          para llevar a cabo el proceso de explotación de conocimiento en LLMs
                        - key: offset_word
                        - attributes: [sense, gloss, part_of_speech, language]
        """
        
        knowledge_table = {}
        offsets_glosses_array = {}
        words_dic = {}
        count = 0
        
        # Leer el archivo de las palabras más usadas y almacenar las palabras en un conjunto junto a su synset
        try:
            with open(self.most_used_words_file, "r", encoding="utf-8") as most_used_words_file:
                # Itera sobre cada línea del archivo
                for linea in most_used_words_file:
                    # Obtenemos una línea del archivo
                    line = linea.split("\t")
                    # Offset
                    offset = "eng-30-" + line[0]
                    # Word
                    word = line[1].split(',')[0]
                    # Comprobar si está bien 
                    if "(" in word and ")" in word:
                        word = word.replace(")","").replace("(","")
                    # Si el offset ya está en el diccionario, añadir la palabra a la lista asociada
                    if offset in words_dic:
                        words_dic[offset].append(word)
                    else:
                        # Si el offset no está en el diccionario, crear una nueva lista con la palabra
                        words_dic[offset] = [word]
            auxFunctions.save_json('words.json', json.dumps(words_dic, indent=2, ensure_ascii=False))
                
        except FileNotFoundError:
            print(f'Archivo "{self.most_used_words_file}" no encontrado. Vuelve a introducir una nueva ruta')
            
        # Leer el archivo que contiene los synset en inglés y almacenarlo en un diccionario auxiliar
        # llamado offsets_glosses_array. El esquema de este es: Key=offset. Value = [gloss]
        try:
            # Intentar abrir el archivo que se encuentra en la ruta proporcionada
            with open(self.eng_synset_file, 'r', encoding="utf-8") as archivo:
                # Recorremos cada línea
                for linea in archivo:
                    # Obtenemos una lista en la que cada elemento es una columna del synset
                    linea = linea.replace('"', '')
                    # Eliminamos las comillas de los elemento
                    synset = linea.strip().split(',')
                    # Añadimos a la lista una tupla (offset, gloss)
                    gloss = synset[6]
                    # Tratar el gloss
                    if gloss != "NULL":
                        if ":" in gloss:
                            gloss = gloss.split(':')[0]
                        gloss = gloss.strip().capitalize()
                        if not gloss.endswith('.'):
                            gloss += '.'
                    offsets_glosses_array[synset[0]] = gloss
        except FileNotFoundError:
            print(f'Archivo "{self.eng_synset_file}" no encontrado. Vuelve a introducir una nueva ruta')
        
        # Leer el archivo que contiene los variant en inglés y almacenarlo en un diccionario llamado knowledge_table
        # El esquema que sigue es: Key=offset_word. Value = [sense, part_of_speech, language]
        try:
            # Intentar abrir el archivo que se encuentra en la ruta proporcionada
            with open(self.eng_variant_file, 'r', encoding="utf-8") as archivo:
                # Recorremos cada línea
                for linea in archivo:
                    # Obtenemos una lista en la que cada elemento es una columna del synset
                    linea = linea.replace('"', '')
                    # Eliminamos las comillas de los elemento
                    synset = linea.strip().split(',')
                    # Obtenemos la palabra
                    word = synset[0]
                    # Si es una palabra compuesta eliminamos la barra baja ( '_' )
                    word = word.replace('_', ' ')
                    # Obtenemos el sense (sentido: indice de tasa de ocurrencia de la palabra en el synset)
                    sense = synset[1]
                    # Obtenemos el offset
                    offset = synset[2]
                    # Tipo de la palabra
                    part_of_speech = synset[3]
                    # Idioma del synset
                    language = offset.split('-')[0]
                    # Clave compuesta (offset_word)
                    offset_word = offset + '_' + word
                    # Si es un synset en inglés y el tipo de palabra es sustantivo (noun=n)
                    if language == "eng" and part_of_speech == "n" and offset in words_dic.keys():
                        if word in words_dic[offset]:
                            # # Generar un número aleatorio entre 1 y 10
                            # numero_aleatorio = random.randint(1, 10)

                            # # Verificar si el número aleatorio es 1
                            # if numero_aleatorio == 10:
                                # Añadimos al diccionario: Key=word. Value = [synset, sense, part_of_speech, language]
                                knowledge_table[offset_word] = [sense, part_of_speech, language]
                                count += 1
                    if count > 499: 
                        break
                        
        except FileNotFoundError:
            print(f'Archivo "{self.eng_variant_file}" no encontrado. Vuelve a introducir una nueva ruta')   
            
        # Definir los atributos de element que tienen un valor por defecto al inicio del proceso
        spanish_gloss = {
            "Spanish gloss": "NULL"
        }
        extraction_llm_answers = {
            "Extraction LLM answers": []
        }
        validation_llm_answers = {   
            "Validation LLM answers": []
        }
        extraction_translation = {
            "Extraction translation": "NULL"
        }
        validation_translation = {
            "Validation translation": "NULL"
        }  
        correct_phrases = {
            "Correctas": 0
        }
        incorrect_phrases_1 = {
            "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": 0
        }
        incorrect_phrases_2 = {
            "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": 0
        }
        incorrect_phrases_3 = {
            "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": 0
        }
        information_message = {
            "Mensaje de información": "NULL"
        }

        # Modificar el knowledge_table añadiendo los glosses del offsets_glosses_array
        # Sigue el siguiente esquema:  Key=offset_word. Value= [sense_index, english_gloss, spanish_gloss, part_of_speech, language, extraction_llm_answers, validation_llm_answers, extraction_translation, validation_translation, correct_phrases, incorrect_phrases_1, incorrect_phrases_2, incorrect_phrases_3, information_message]
        for word, element in knowledge_table.items():
            sense_index = element[0]
            english_gloss = offsets_glosses_array[word.split('_')[0]].replace('_', ' ')
            part_of_speech = element[1]
            language = element[2]
            
            # Crear el nuevo formato de diccionario
            item_dict = {
                "Sense index": sense_index,
                "English gloss": english_gloss,
                "Spanish gloss": spanish_gloss["Spanish gloss"],
                "Part of speech": part_of_speech,
                "Language": language,
                "Extraction LLM answers": extraction_llm_answers["Extraction LLM answers"],
                "Validation LLM answers": validation_llm_answers["Validation LLM answers"],
                "Extraction translation": extraction_translation["Extraction translation"],
                "Validation translation": validation_translation["Validation translation"],
                "Correctas": correct_phrases["Correctas"],
                "Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase": incorrect_phrases_1["Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase"],
                "Incorrectas de tipo 2: la palabra a analizar no aparece en la frase": incorrect_phrases_2["Incorrectas de tipo 2: la palabra a analizar no aparece en la frase"],
                "Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo": incorrect_phrases_3["Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo"],
                "Mensaje de información": information_message["Mensaje de información"]
            }
            
            # Actualizar el knowledge_table con el nuevo formato
            knowledge_table[word] = item_dict

        return knowledge_table