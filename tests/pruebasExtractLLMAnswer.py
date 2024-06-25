import re

a = {
  "id": "cmpl-4dd15b7c-635a-4020-91fc-776b842b2c2b",
  "object": "text_completion",
  "created": 1717001082,
  "model": "../models/zephyr-7b-alpha.Q4_K_M.gguf",
  "choices": [
    {
      "text": "Question: As a linguistics expert, please provide five sentences containing the word 'object', with the meaning of 'A tangible and visible entity; an entity that can cast a shadow.'. Answer: The objects on the table was a heavy book with a worn-out cover. Its pages were yellowed with age, and its spine creaked as I opened it. The object-oriented in my hand was a smooth stone, cool to the touch and perfectly round. It glinted in the sunlight, casting a shadow on the ground. The object that caught my eye was a red balloon, bobbing gently in the breeze. Its shadow danced along the pavement as I approached it. The object that lay before me was a bowl of fruit, overflowing with juicy oranges and plump grapes. Their shadows stretched out like fingers, reaching for the ground. The object that stood between us was a tall fence, its shadow casting a dark line across the grass. It seemed to loom over us, blocking our path.",
      "index": 0,
      "logprobs": "null",
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 42,
    "completion_tokens": 170,
    "total_tokens": 212
  }
}

def extract_llm_answers(llm_answer):
    # Extraer el texto devuelto
    return_answer_value = llm_answer['choices'][0]['text']
    # Dividirlo en dos partes (la parte de la pregunta, la parte de la respuesta)
    llm_extracted_answer = return_answer_value.split('Answer:')[1]
    # Obtener la palabra
    word = ""
    if "please provide five sentences containing the word " in return_answer_value:
        word = return_answer_value.split("please provide five sentences containing the word '")[1].split("'")[0]
    elif "por favor, proporciona cinco frases que contengan la palabra " in return_answer_value:
        word = return_answer_value.split("por favor, proporciona cinco frases que contengan la palabra '")[1].split("'")[0]
    # Eliminar los saltos de linea
    llm_extracted_answer = llm_extracted_answer.replace('\n',' ').replace('\n\n',' ').strip()
    # Comprabar si tiene separadores de frases. Si no tiene es que es una traduccion
    if(re.split(r'\d+\)|\d+\.', llm_extracted_answer)[1:] != []):    
        # Dividir el texto en frases utilizando cualquier secuencia de un número seguido de un punto como criterio de separación
        llm_extracted_answer = re.split(r'\d+\)|\d+\.', llm_extracted_answer)[1:]
        # Quitar los espacios blancos del principio y final de las frases 
        llm_extracted_answer = [answer.strip() for answer in llm_extracted_answer]
        # Quitar las comillas y barras de las frases
        llm_extracted_answer = [answer.replace('"', '').replace("\"", "").replace('\\', '').replace("\\\"", "") for answer in llm_extracted_answer]
    # Comprobar si tiene más de una frase. En ese caso puede que no tenga separadores pero que sean un conjunto de frases
    elif(len(llm_extracted_answer.split('. ')) >= 4):
        # Compilar la expresión regular directamente sin escapar
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        llm_extracted_answer = [phrase for phrase in llm_extracted_answer.split('. ') if pattern.search(phrase)]
    return llm_extracted_answer


print(extract_llm_answers(a))
