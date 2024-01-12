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
    def __init__(self):
        self.table = Table(style="rgb(229,193,0)",
                           header_style="rgb(229,193,0)",
                           pad_edge=False,
                           show_edge=False,
                           collapse_padding=True,
                           box=SIMPLE_HEAD)
        self.console = Console()

    def add_rule(self, header=None):
        if header:
            self.console.rule(f"[bold rgb(229,193,0)]{header}", style="rgb(229,193,0)")
        else:
            self.console.rule(style="rgb(229,193,0)")

    @staticmethod
    def add_path(path):
        rprint(f"[rgb(229,193,0)]path to containing folder: [green]{path}")

    def add_table(self, original_filename, converted_filename, original_size, converted_size, compression_rate):

        if compression_rate < 1.0:
            style = "rgb(254,44,45)"
        else:
            style = "rgb(23,255,23)"

        self.table.add_column("", style="rgb(229,193,0)", no_wrap=True)
        self.table.add_column("name", style="green")
        self.table.add_column("size", justify="right", style="green")
        self.table.add_column("compression rate", style=style)

        self.table.add_row("original", original_filename, original_size, "")
        self.table.add_row("converted", converted_filename, converted_size, f"{compression_rate:.2f}")

        self.console.print(self.table)

    @staticmethod
    def display_help():
        rprint("[rgb(229,193,0)]This application will perform encoding or decoding on any type of files using"
               "either Huffman or LZW compression algorithm")
        rprint("[rgb(229,193,0)]It requires commands as follows:")
        rprint("command", "complete path or file name", "algorithm", "optional new name for the output file")
        rprint("[reverse green]encode",
               "[rgb(229,193,0)]filename.extension",
               "[reverse green]algorithm",
               "[dim rgb(229,193,0)]new_filename")

        rprint("[reverse green]decode",
               "[rgb(229,193,0)]filename.extension",
               "[reverse green]         ",
               "[dim rgb(229,193,0)]new_filename")
