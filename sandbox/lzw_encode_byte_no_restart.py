from core.compression import CompressionABC


class LZWCompressionBytesNoRestart(CompressionABC):

    INITIAL_CODEBOOK_SIZE = 256
    MAXIMUM_CODEBOOK_SIZE = 4096

    def __init__(self):

        # tracks the current size of the codebook
        self.codebook_size = None
        # Contains the current codebook as it changes through the file encoding.
        self.codebook = None
        # maximum bit size for codes in the code array
        self.bit_size = None

    def encode(self, uncompressed_data: bytes):
        """Compress bytes input to bytes output"""

        # Build the initial codebook.
        self.create_codebook()
        code_array = self.create_code(uncompressed_data)
        self.calculate_max_bit_size(code_array)
        compressed_code = self.compress_code(code_array, self.bit_size)

        return compressed_code

    def create_codebook(self):
        """Initiation of the base code.
        """
        # Starts with the amount of entries for the identical code 256
        # k:v str:int
        self.codebook_size = self.INITIAL_CODEBOOK_SIZE
        self.codebook = {chr(i): i for i in range(self.codebook_size)}

    def create_code(self, uncompressed_data):

        # Stores sequences of one or more bytes/symbols for entry in the codebook.
        string = ""

        # encoded output in codepoints int array of codes
        code_array = []

        # start LZW compression algorithm
        for symbol in uncompressed_data:  # Symbol is still a byte here.
            string_and_symbol = string + chr(symbol)  # Here byte data turns into str.

            if string_and_symbol in self.codebook:
                string = string_and_symbol

            else:
                # output the stored sequence to the codes array
                code_array.append(self.codebook[string])

                # Add string_and_symbol to the dictionary.
                if len(self.codebook) < self.MAXIMUM_CODEBOOK_SIZE:
                    self.codebook[string_and_symbol] = self.codebook_size
                    self.codebook_size += 1

                # stores sequences for entry in the dictionary
                string = chr(symbol)

        # Output the code for string.
        if string:
            code_array.append(self.codebook[string])

        return code_array

    def calculate_max_bit_size(self, code_array):
        """Finds maximum bit size for the largest number in code array.
        """
        self.bit_size = max(code_array).bit_length()

    @staticmethod
    def compress_code(code_array, bit_size):
        """Use of bit-packing to compress the code array further.
        """
        byte_size = (bit_size + 7) // 8  # Number of bytes needed for each integer
        compressed_code = bytearray()
        for i in code_array:
            i_bytes = int(i).to_bytes(byte_size, 'little', signed=True)
            compressed_code.extend(i_bytes)
        return bytes(compressed_code)

    @staticmethod
    def decompress_code(compressed_code, bit_size):

        byte_size = (bit_size + 7) // 8  # Number of bytes used for each integer
        code_array = []
        for i in range(0, len(compressed_code), byte_size):
            i_bytes = compressed_code[i:i + byte_size]
            code_array.append(int.from_bytes(i_bytes, 'little', signed=True))
        return code_array

    def decode(self, compressed_data):
        """bytes to bytes
        int to bytes
        """

        # compressed data in form of bytes is turned into code array
        code_array = self.decompress_code(compressed_data, self.bit_size)

        self.create_reversed_codebook()
        # decompressed_data = self.recover_data(code_array)
        decompressed_data = self.recover_data(code_array)

        return decompressed_data

    def create_reversed_codebook(self):
        """Initiation of the base code.
        """
        # Starts with the amount of entries for the identical code 256
        # k:v int:str
        self.codebook_size = self.INITIAL_CODEBOOK_SIZE
        self.codebook = {i: chr(i) for i in range(self.codebook_size)}

    def recover_data(self, code_array):
        """Obtains the original data input from the integer codes.
        """

        # first int-code is stored as a str
        w = result = chr(code_array.pop(0))

        for code in code_array:

            if code in self.codebook:
                # entry becomes the stored str in this int-code
                entry = self.codebook[code]
            elif code == self.codebook_size:
                entry = w + w[0]
            else:
                raise ValueError(f'Poorly compressed code: {code}')

            result += entry

            if self.codebook_size < self.MAXIMUM_CODEBOOK_SIZE:

                # Add w+entry[0] to the codebook.
                self.codebook[self.codebook_size] = w + entry[0]
                self.codebook_size += 1

            w = entry

        # turns string into bytes before return
        decompressed_data = bytes(result, 'utf-8')

        return decompressed_data
