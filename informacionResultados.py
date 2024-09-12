import json
import sys
sys.path.append("./auxFunctionLibrary")
from pythonLib import auxFunctions 


# Variables globales para contar errores
incorrect_1_count = 0
incorrect_2_count = 0
incorrect_3_count = 0
correct_count = 0
cantidad_exito = 0
total_frases = 0
null_extraccion = 0
null_validacion = 0

# Leer el archivo JSON
with open('./knowledge_table.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Procesar cada elemento en el archivo JSON
for key, value in data.items():
    
    if value["Extraction translation"] != "NULL" and value["Validation translation"] != "NULL":
        cantidad_exito += 1

    if value["Extraction translation"] == "NULL" or value["Validation translation"] == "NULL":
        correct_count += value["Correctas"]
        incorrect_1_count += value["Incorrectas de tipo 1: Generación de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase"]
        incorrect_2_count += value["Incorrectas de tipo 2: la palabra a analizar no aparece en la frase"]
        incorrect_3_count += value["Incorrectas de tipo 3: La relación obtenida no corresponde con un sustantivo"]  
        if value["Extraction translation"] == "NULL":          
            total_frases += len(auxFunctions.extract_llm_answers_set_of_phrases(value["Extraction LLM answers"][0]))
        elif value["Validation translation"] == "NULL":
            total_frases += len(auxFunctions.extract_llm_answers_set_of_phrases(value["Validation LLM answers"][0]))
        if value["Mensaje de información"] == "La entrada ha terminado su ejecución en la fase de extracción.":
            null_extraccion += 1
        elif value["Mensaje de información"] == "La entrada ha terminado su ejecución en la fase de validación.":
            null_validacion += 1

# Calcular los porcentajes de errores
porcentaje_incorrecto_1 = (incorrect_1_count / total_frases) * 100 if total_frases > 0 else 0
porcentaje_incorrecto_2 = (incorrect_2_count / total_frases) * 100 if total_frases > 0 else 0
porcentaje_incorrecto_3 = (incorrect_3_count / total_frases) * 100 if total_frases > 0 else 0
porcentaje_correcto = (correct_count / total_frases) * 100 if total_frases > 0 else 0

# Calcular la suma de las entradas analizadas
suma_total = cantidad_exito + null_extraccion + null_validacion

# Calcular la suma total de los NULL
suma_total_null = null_extraccion + null_validacion

# Calcular porcentajes de 'Femenino' y 'NULL' respecto al total de 'Masculino', 'Femenino' y 'NULL'
porcentaje_exito = (cantidad_exito / suma_total) * 100
porcentaje_null = (suma_total_null / suma_total) * 100
porcentaje_null_extraccion = (null_extraccion / suma_total) * 100
porcentaje_null_validacion = (null_validacion / suma_total) * 100

# Guardar los resultados en un archivo de texto
with open('./resultados.txt', 'w', encoding='utf-8') as result_file:
    result_file.write(f"\n\nINFORMACIÓN DE LOS RESULTADOS DE LA EXPERIMENTACIÓN DEL SEGUNDO CASO PILOTO\n\n")
    result_file.write(f"Entradas totales: {suma_total} (100.00%)\n")
    result_file.write(f"Cantidad de conocimiento obtenido: {cantidad_exito} ({porcentaje_exito:.2f}%)\n")
    result_file.write(f"Cantidad de casos sin traducir ('NULL') obtenidos: {suma_total_null} ({porcentaje_null:.2f}%)\n")
    result_file.write(f"Cantidad de casos sin traducir ('NULL') obtenidos en la fase de extracción: {null_extraccion} ({porcentaje_null_extraccion:.2f}%)\n")
    result_file.write(f"Cantidad de casos sin traducir ('NULL') obtenidos en la fase de validación: {null_validacion} ({porcentaje_null_validacion:.2f}%)\n")
    result_file.write(f"Total de frases analizadas de casos sin traducir ('NULL'): {total_frases}\n")
    result_file.write(f"Correctas: {correct_count} ({porcentaje_correcto:.2f}%)\n")
    result_file.write(f"Incorrectas de tipo 1 (Generacion de palabras con otro part of speech. la palabra a analizarno está como sustantivo en la frase.): {incorrect_1_count} ({porcentaje_incorrecto_1:.2f}%)\n")
    result_file.write(f"Incorrectas de tipo 2 (la palabra a analizarno aparece en la frase.): {incorrect_2_count} ({porcentaje_incorrecto_2:.2f}%)\n")
    result_file.write(f"Incorrectas de tipo 3 (La relación obtenida no corresponde con un sustantivo.): {incorrect_3_count} ({porcentaje_incorrecto_3:.2f}%)\n")
