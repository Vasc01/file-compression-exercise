def int_array_to_bytes(input_int_array):

    # bin(int) is used to convert and obtain an integer value's binary string equivalent.
    # Slice operator omits the prefix "0b" in the string.
    # rjust() does right alignment of the string,
    # while filling the left empty spaces with "0" until total length of 8 is reached.
    bits = bin(b)[2:].rjust(8, '0')
    bit_string += bits

    # Stores
    bytes_data = bytearray()

    for i in range(0, len(padded_converted_data), 8):
        byte = padded_converted_data[i:i + 8]
        bytes_data.append(int(byte, 2))

    encoded_data = bytes(bytes_data)


def bytes_to_int_array(input_bytes):
    pass
