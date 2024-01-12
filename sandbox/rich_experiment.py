# Official rich documentation:
# https://rich.readthedocs.io/en/latest/index.html

from rich import print as rprint
from rich.box import SIMPLE_HEAD
from rich.table import Table
from rich.console import Console
table = Table(style="rgb(229,193,0)",
              header_style="rgb(229,193,0)",
              pad_edge=False,
              show_edge=False,
              collapse_padding=True,
              box=SIMPLE_HEAD)
console = Console()

rprint()

header = "LZW Compression"
console.rule(f"[bold rgb(229,193,0)]{header}", style="rgb(229,193,0)")

path = r"C:\Workspace\1_PyCh_projects\file-compression-exercise"

rprint(f"[rgb(229,193,0)]path to containing folder: [green]{path}")

table.add_column("", style="rgb(229,193,0)", no_wrap=True)
table.add_column("name", style="green")
table.add_column("size", justify="right", style="green")
table.add_column("compression rate", style="rgb(23,255,23)")

table.add_row("original", "test.txt", "350kB", "")
table.add_row("converted", "test-test.lzw", "50kB", "3.55")

rprint()
console.print(table)

# rprint()
console.rule(style="rgb(229,193,0)")
rprint()
