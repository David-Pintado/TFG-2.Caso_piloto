def find_element_with_difference(lista, difference):
    # Ordenar la lista de forma descendente según el segundo elemento de las tuplas
    sorted_list = sorted(lista, key=lambda x: x[1], reverse=True)

    # Tomar el primer elemento como referencia para la comparación
    reference = sorted_list[0]

    # Verificar si la diferencia es mayor o igual a la diferencia especificada con respecto a los demás elementos
    for element in sorted_list[1:]:
        if reference[1] - element[1] < difference:
            return []
    return reference

# Lista de ejemplo
lista = [('persona', 5), ('otra_persona', 10), ('más_personas', 3), ('alguien', 7)]

# Diferencia deseada
desired_difference = 5

# Encontrar elemento que cumpla con las condiciones
found_element = find_element_with_difference(lista, desired_difference)

if found_element:
    print("Element found:", found_element)
else:
    print("No element found that meets the conditions.")
