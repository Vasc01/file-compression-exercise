from core.compression import CompressionABC


class LZWCompressionBytes(CompressionABC):

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

        # reserves code 256 for RESTART_CODEBOOK
        self.codebook["RESTART_CODEBOOK"] = self.RESTART_CODEBOOK
        self.codebook_size += 1

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

                else:
                    # A code is inserted to identify for the decoding algorithm that the codebook is restarted.
                    code_array.append(self.codebook["RESTART_CODEBOOK"])

                    # Once the codebook reaches the maximum size it starts rebuilding itself from the beginning.
                    self.create_codebook()

                # stores sequences for entry in the dictionary
                string = chr(symbol)

        # Output the code for string.
        if string:
            code_array.append(self.codebook[string])

        return code_array

    def compress_code(self):
        pass
        # integer array to binary
        # compressed_data = struct.pack('>' + 'i' * len(temporary_data_output), *temporary_data_output)
        # compressed_data = self.pack(temporary_data_output)

    # def pack(self, codepoints):
    #     """Variable bit lengths"""
    #     tailbits = []
    #     codesize = 4096
    #
    #     minwidth = 8
    #     while (1 << minwidth) < codesize:
    #         minwidth = minwidth + 1
    #
    #     nextwidth = minwidth
    #
    #     for pt in codepoints:
    #
    #         newbits = self.inttobits(pt, nextwidth)
    #         tailbits = tailbits + newbits
    #
    #         codesize = codesize + 1
    #
    #         if codesize >= (2 ** nextwidth):
    #             nextwidth = nextwidth + 1
    #
    #         while len(tailbits) > 8:
    #             nextbits = tailbits[:8]
    #             nextbytes = self.bitstobytes(nextbits)
    #             for bt in nextbytes:
    #                 yield struct.pack("B", bt)
    #
    #             tailbits = tailbits[8:]
    #
    #     if tailbits:
    #         tail = self.bitstobytes(tailbits)
    #         for bt in tail:
    #             yield struct.pack("B", bt)
    #
    # def inttobits(self, anint, width=None):
    #
    #     remains = anint
    #     retreverse = []
    #     while remains:
    #         retreverse.append(remains & 1)
    #         remains = remains >> 1
    #
    #     retreverse.reverse()
    #
    #     ret = retreverse
    #     if None != width:
    #         ret_head = [0] * (width - len(ret))
    #         ret = ret_head + ret
    #
    #     return ret
    #
    # def bitstobytes(self, bits):
    #
    #     ret = []
    #     nextbyte = 0
    #     nextbit = 7
    #     for bit in bits:
    #         if bit:
    #             nextbyte = nextbyte | (1 << nextbit)
    #
    #         if nextbit:
    #             nextbit = nextbit - 1
    #         else:
    #             ret.append(nextbyte)
    #             nextbit = 7
    #             nextbyte = 0
    #
    #     if nextbit < 7: ret.append(nextbyte)
    #     return ret

    def decode(self, compressed_data):
        """bytes to bytes
        int to bytes
        """

        # compressed data in form of bytes is turned into code array
        # self.decompress_code()
        code_array = compressed_data  # for now

        self.create_reversed_codebook()
        # decompressed_data = self.recover_data(code_array)
        decompressed_data = self.geather_recovered_data(code_array)

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

        # reserves code 256 for RESTART_CODEBOOK
        self.codebook[self.RESTART_CODEBOOK] = "RESTART_CODEBOOK"
        self.codebook_size += 1

    def recover_data(self, code_array):
        """Obtains the original data input from the integer codes.
        """

        # first int-code is stored as a str
        w = result = chr(code_array.pop(0))

        index = -1
        for code in code_array:
            index += 1
            if code == self.RESTART_CODEBOOK:
                self.create_reversed_codebook()
                break

            elif code in self.codebook:
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
        # decompressed_data = bytes(result, 'utf-8')
        decompressed_data = result

        return decompressed_data, index

    def geather_recovered_data(self, code_array):

        recovered_data = ""

        while code_array:
            recovered_data += self.recover_data(code_array)[0]
            index_restarting_code = self.recover_data(code_array)[1]
            code_array = code_array[index_restarting_code+1:]
            print(index_restarting_code)

        return bytes(recovered_data, 'utf-8')
