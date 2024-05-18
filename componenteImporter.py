import json

class ComponenteImporter:
    
    def __init__(self, eng_variant_file, eng_synset_file, most_used_words_file):
        self.eng_variant_file = eng_variant_file 
        self.eng_synset_file = eng_synset_file
        self.most_used_words_file = most_used_words_file

    # Método para generar el 'source_information'
    # Esta estructura será un diccionario, la cual seguirá el siguiente esquema: 
    # Key=offset_word. Value = gloss, sense, part_of_speech, language
    def generate_data_structure(self):
        source_information = {}
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
            self.save_json('words.json', json.dumps(words_dic, indent=2, ensure_ascii=False))
                
        except FileNotFoundError:
            print(f'Archivo "{self.most_used_words_file}" no encontrado. Vuelve a introducir una nueva ruta')
            
        # Leer el archivo que contiene los synset en inglés y almacenarlo en un diccionario llamado offsets_glosses_array
        # El esquema de este es: Key=offset. Value = gloss
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
        
        # Leer el archivo que contiene los variant en inglés y almacenarlo en un diccionario llamado source_information
        # El esquema de este es: Key=offset_word. Value = sense, part_of_speech, language
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
                            # Añadimos al diccionario: Key=word. Value = [synset, sense, part_of_speech, language]
                            source_information[offset_word] = [sense, part_of_speech, language]
                            count += 1
                    if count > 4: 
                        break
                        
        except FileNotFoundError:
            print(f'Archivo "{self.eng_variant_file}" no encontrado. Vuelve a introducir una nueva ruta')   
          
        # Modificar el source_information añadiendo los glosses del offsets_glosses_array
        # El esquema del source_information será:  Key=offset_word. Value = sense, gloss, part_of_speech, language
        for word, element in source_information.items(): 
            item_list = []
            item_list = [element[0], offsets_glosses_array[word.split('_')[0]].replace('_',' '), element[1], element[2]]
            source_information[word] = item_list
        
        return source_information  

    # Método para guardar un archivo json en la ruta proporcionada
    def save_json(self, file_path, json):
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json)