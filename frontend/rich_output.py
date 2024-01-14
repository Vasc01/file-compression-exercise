"""Formatted console output.

The rich library for python offers formatted and colored output for command line software.
It increases readability of the information.
Official rich documentation: https://rich.readthedocs.io/en/latest/index.html
"""

from rich import print as rprint
from rich.box import SIMPLE_HEAD
from rich.table import Table
from rich.console import Console


class RichOutput(object):
    """Creates structured output elements.

    The output information is colored, separated and justified for maximum readability.

    Attributes:
        output_table (Table): Table with information about encoding or decoding process.
        help_table (Table): Table with information about software features and available commands.
        console (Console): Provides control over terminal formatting.
    """

    def __init__(self):
        """Initiates an instance of the RichOutput."""

        self.output_table = Table(style="rgb(229,193,0)",
                                  header_style="rgb(229,193,0)",
                                  pad_edge=False,
                                  show_edge=False,
                                  collapse_padding=True,
                                  box=SIMPLE_HEAD)
        self.help_table = Table(style="rgb(229,193,0)",
                                header_style="rgb(229,193,0)",
                                pad_edge=False,
                                show_edge=False,
                                collapse_padding=True,
                                box=None)
        self.console = Console()

    def add_rule(self, header=None):
        """Creates horizontal line with optional text in the middle"""

        if header:
            self.console.rule(f"[bold rgb(229,193,0)]{header}", style="rgb(229,193,0)")
        else:
            self.console.rule(style="rgb(229,193,0)")

    @staticmethod
    def add_path(path):
        """Prints out the path of the current directory"""

        rprint(f"[rgb(229,193,0)]path to containing folder: [green]{path}")

    def display_output(self, original_filename, converted_filename, original_size,
                       converted_size, compression_rate, time_elapsed):
        """Creates information summary of encoding or decoding process.

        Args:
            original_filename (str): File name of the original file with extension.
            converted_filename (str): File name of the converted file with extension.
            original_size (str): Size of the original file in bytes.
            converted_size (str): Size of the converted file in bytes.
            compression_rate (float): original_size / converted_size. Displayed only if encoding.
            time_elapsed (str): Time for encoding or decoding in seconds.
        """

        # Poor compression has rate less than 1.0. It is than displayed in red, otherwise in green.
        if compression_rate < 1.0:
            style = "rgb(254,44,45)"
        else:
            style = "rgb(23,255,23)"

        # Creates columns of the table.
        self.output_table.add_column("", style="rgb(229,193,0)", no_wrap=True)
        self.output_table.add_column("name", style="green")
        self.output_table.add_column("size", justify="right", style="green")
        self.output_table.add_column("compression rate", style=style)
        self.output_table.add_column("time elapsed", style="green")

        # Creates rows of the table.
        self.output_table.add_row("original", original_filename, original_size, "", "")
        self.output_table.add_row("converted", converted_filename,
                                  converted_size,
                                  f"{compression_rate:.2f}" if compression_rate != 0 else " ",
                                  time_elapsed)

        self.console.print(self.output_table)

    def display_help(self):
        """A text block with helpful information about the operation of the program is created."""

        rprint("[rgb(229,193,0)]This application will perform encoding or decoding on any type of files using"
               "either Huffman or LZW compression algorithm.")
        rprint("[rgb(229,193,0)]It is operated as follows:")

        # Creates columns of the table.
        self.help_table.add_column("[green]command  ", justify="left", style="green")
        self.help_table.add_column("complete path or file name  ", justify="left", style="rgb(229,193,0)")
        self.help_table.add_column("[green]algorithm  ", justify="left", style="green")
        self.help_table.add_column("[dim]optional new name for the output file", justify="left",
                                   style="dim rgb(229,193,0)")

        # Creates rows of the table.
        self.help_table.add_row("encode", "filename.extension", "lzw/huf", "new_filename")
        self.help_table.add_row("decode", "filename.extension", "", "new_filename")

        self.console.print(self.help_table)

        # Example commands.
        rprint()
        rprint("[rgb(229,193,0)]Examples:")
        rprint("[green]encode",
               "[rgb(229,193,0)]text.txt",
               "[green]lzw",
               "[dim rgb(229,193,0)]encoded_text")
        rprint("[green]decode",
               "[rgb(229,193,0)]encoded_text.lzw",
               "[dim rgb(229,193,0)]decoded_text")

    @staticmethod
    def execute_with_spinner(function, *args):
        """Shows a spinner/animation while executing a longer process.

        Args:
            function: Used to execute encoding or decoding.
            args: Any arguments needed for the mentioned function.

        Returns:
            data: The result of the executed function.
        """
        console = Console()

        # Starts the spinner.
        with console.status("[rgb(229,193,0)]Computing...", spinner="aesthetic"):
            data = function(*args)

        # Stops the spinner or changes the spinner to something else.
        console.print(":white_heavy_check_mark:  [green]Done")

        return data
