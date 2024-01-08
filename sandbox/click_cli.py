import click

from core.compression import LZWCompression, HuffmanCompression
from core.performance_calculator import PerformanceCalculator


class Application(object):

    def __init__(self):
        self.lzw_algorithm = LZWCompression()
        self.huffman_algorithm = HuffmanCompression()
        self.performance_calculator = PerformanceCalculator

    @click.group()
    def cli(self):
        pass

    @cli.command()
    def compress(self):
        click.echo('compressing...')

    @cli.command()
    def decompress(self):
        click.echo('decompressing...')

    def run(self):

        value = click.prompt('Select a command to run', type=click.Choice(list(self.cli.commands.keys()) + ['exit']))
        while value != 'exit':
            self.cli.commands[value]()
