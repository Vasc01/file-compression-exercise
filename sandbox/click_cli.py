import click

from core.algorihm import LZWAlgorithm, HuffmanAlgorithm
from core.stream_encoder import StreamEncoder
from core.performance_calculator import PerformanceCalculator


class Application(object):

    def __init__(self):
        self.lzw_algorithm = LZWAlgorithm()
        self.huffman_algorithm = HuffmanAlgorithm()
        self.stream_encoder = StreamEncoder()
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
