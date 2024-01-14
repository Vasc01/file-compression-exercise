import time
from rich.console import Console


def do_something():

    # Display the spinner for this amount of time while executing do_something
    time.sleep(5.0)


console = Console()

with console.status(
        "[rgb(229,193,0)]Computing...", spinner="arrow3"
):
    do_something()

console.print(":white_heavy_check_mark:  [green]Done")
