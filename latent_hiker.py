from genetic import gui
from genetic.generate_from_latent import generate_image, load_network
from typing import List, Optional
from generate import num_range
import click

@click.command()
@click.pass_context
@click.option('-p', '--population_size', help='Number of images generated per generation', default=10, type=int)
@click.option('-n', '--network', 'network_pkl', help='Network pickle filename', required=True)
def main(ctx: click.Context, population_size: int, network_pkl: str):
    G = load_network(network_pkl)
    gui.start_gui(population_size, G)

if __name__ == "__main__":
    main() 