# https://stackoverflow.com/questions/6834388/basic-lzw-compression-help-in-python
# https://www.dspguide.com/graphics/F_27_7.gif

# ----LZW-data-in-----------------------------------------------------

def compress(uncompressed):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}

    # stores sequences for entry in the dictionary
    word = ""

    # encoded output
    result = []

    for character in uncompressed:
        word_and_character = word + character
        if word_and_character in dictionary:
            word = word_and_character
        else:
            # output the stored sequence
            result.append(dictionary[word])

            # Add word_and_character to the dictionary.
            dictionary[word_and_character] = dict_size
            dict_size += 1

            # stores sequences for entry in the dictionary
            word = character

    # Output the code for word.
    if word:
        result.append(dictionary[word])

    # output for inspection
    print(dictionary)
    print(dict_size)

    return result

# ----LZW-data-out----------------------------------------------------


input_data = "bla bla bla elkkhfs;hlk;s;lka;a;a;sjjfjfjehfue"
compressed_data = compress(input_data)
print(input_data)
print(len(input_data))
print(compressed_data)
print(len(compressed_data))
