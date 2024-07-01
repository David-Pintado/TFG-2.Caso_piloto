import json
import sys
sys.path.append("./auxFunctionLibrary")
from pythonLib import auxFunctions 


# Variables globales para contar errores
incorrect_1_count = 0
incorrect_2_count = 0
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
    # Validar la longitud de la lista value
    if len(value) > 8:
        if value[6] != "NULL" and value[8] != "NULL":
            cantidad_exito += 1

    if len(value) > 5 and value[6] == "NULL":
        if len(value) > 8:
            correct_count += value[7].get("Correctas.", 0)
            incorrect_1_count += value[8].get("Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.", 0)
            incorrect_2_count += value[9].get("Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.", 0)
            total_frases += len(auxFunctions.extract_llm_answers_set_of_phrases(value[5][0]))
        if len(value) > 10:
            if value[10].get("Mensaje de información") == "La entrada ha terminado su ejecución en la extracción del resultado provisional.":
                null_extraccion += 1
            elif value[10].get("Mensaje de información") == "La entrada ha terminado su ejecución en la validación del resultado provisional.":
                null_validacion += 1

    if len(value) > 8 and value[8] == "NULL":
        if len(value) > 10:
            correct_count += value[9].get("Correctas.", 0)
            incorrect_1_count += value[10].get("Incorrectas de tipo 1: Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.", 0)
            incorrect_2_count += value[11].get("Incorrectas de tipo 2: La palabra que buscamos no aparece en la frase.", 0)
            total_frases += len(auxFunctions.extract_llm_answers_set_of_phrases(value[7][0]))
        if len(value) > 12:
            if value[12].get("Mensaje de información") == "La entrada ha terminado su ejecución en la extracción del resultado provisional.":
                null_extraccion += 1
            elif value[12].get("Mensaje de información") == "La entrada ha terminado su ejecución en la validación del resultado provisional.":
                null_validacion += 1

# Calcular los porcentajes de errores
porcentaje_incorrecto_1 = (incorrect_1_count / total_frases) * 100 if total_frases > 0 else 0
porcentaje_incorrecto_2 = (incorrect_2_count / total_frases) * 100 if total_frases > 0 else 0
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
    result_file.write(f"Cantidad de casos sin clasificar ('NULL') obtenidos: {suma_total_null} ({porcentaje_null:.2f}%)\n")
    result_file.write(f"Cantidad de casos sin clasificar ('NULL') obtenidos en la fase de extracción: {null_extraccion} ({porcentaje_null_extraccion:.2f}%)\n")
    result_file.write(f"Cantidad de casos sin clasificar ('NULL') obtenidos en la fase de validación: {null_validacion} ({porcentaje_null_validacion:.2f}%)\n")
    result_file.write(f"Total de frases analizadas de casos sin clasificar ('NULL'): {total_frases}\n")
    result_file.write(f"Correctas: {correct_count} ({porcentaje_correcto:.2f}%)\n")
    result_file.write(f"Incorrectas de tipo 1 (Generacion de palabras con otro part of speech. La palabra que buscamos no está como noun en la frase.): {incorrect_1_count} ({porcentaje_incorrecto_1:.2f}%)\n")
    result_file.write(f"Incorrectas de tipo 2 (La palabra que buscamos no aparece en la frase.): {incorrect_2_count} ({porcentaje_incorrecto_2:.2f}%)\n")
