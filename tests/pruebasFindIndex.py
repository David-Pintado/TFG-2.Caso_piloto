def find_first_index(lst, condition):
    for index, element in enumerate(lst):
        if condition(element):
            return index
    return -1

word_position = find_first_index(['The', 'object', 'on', 'the', 'table', 'was', 'a', 'heavy', 'vase', 'made', 'of', 'ceramic', ',', 'casting', 'a', 'long', 'shadow', 'on', 'the', 'floor', '.'], lambda x: x == 'object')
print(word_position)