from core.compression import CompressionABC


class LZWCompressionBytesNoRestart(CompressionABC):

    INITIAL_CODEBOOK_SIZE = 256
    MAXIMUM_CODEBOOK_SIZE = 4096
    RESTART_CODEBOOK = 256

    def __init__(self):

        # tracks the current size of the codebook
        self.codebook_size = None
        # Contains the current codebook as it changes through the file encoding.
        self.codebook = None

    def encode(self, uncompressed_data: bytes):
        """Compress bytes data to bytes output"""

        # Build the initial codebook.
        self.create_codebook()
        code_array = self.create_code(uncompressed_data)
        # compressed_code = self.compress_code(code_array)
        # return compressed_code
        return code_array

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

    def decode(self, compressed_data):
        """bytes to bytes
        int to bytes
        """

        # compressed data in form of bytes is turned into code array
        # self.decompress_code()
        code_array = compressed_data  # for now

        self.create_reversed_codebook()
        # decompressed_data = self.recover_data(code_array)
        decompressed_data = self.recover_data(code_array)

        return decompressed_data

    def decompress_code(self, compressed_data):
        pass

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

            # Add w+entry[0] to the codebook.
            self.codebook[self.codebook_size] = w + entry[0]
            self.codebook_size += 1

            w = entry

        # turns string into bytes before return
        decompressed_data = bytes(result, 'utf-8')

        return decompressed_data
