"""Starts the program.

Use this file as entry point to the program.
With the following commands you have access to the core functionalities.

command   complete path or file name   algorithm   optional new name for the output file
encode    filename.extension           lzw/huf     new_filename
decode    filename.extension                       new_filename

Examples:
encode text.txt lzw encoded_text
decode encoded_text.lzw decoded_text
"""

from frontend.application import run

if __name__ == "__main__":

    # Part of the frontend that starts the input and output formatting.
    run()
