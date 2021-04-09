from __future__ import print_function
from IPython.display import Image, clear_output, display
from ipywidgets import interact, interactive, fixed, interact_manual, Layout, Box, Label
import ipywidgets as widgets
from . import genetic_algo
from genetic.generate_from_latent import generate_image
import io

def _update(board, population):
    # fitness = []
    # for slider in sliders:
    #     fitness.append(slider.get())

    # population.evolve(fitness, float(GET-FROM-MUTATION))

    # for i in range(len(population.individuals)):
    #     generated_image = generate_image(G, population.individuals[i].genes)
    pass

def image_to_byte_array(image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format='JPEG')
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr
        

def run_colab(population_size, network_pkl):
    G = load_network(network_pkl)
    population = genetic_algo.Population(G, population_size)
    phenotypes = []
    for individual in population.individuals:
        generated_image = generate_image(G, individual.genes)
        slider = widgets.IntSlider(
            value=0, 
            min=0, 
            max=10,
            readout=False,
            layout=Layout(width='90%')
        )
        image = widgets.Image(
            value=image_to_byte_array(generated_image),
            format='jpg',
            width="90%",
        )
        phenotype = widgets.VBox([image, slider])
        phenotypes.append(phenotype)
    board = Box(
        children=phenotypes, 
        layout=Layout(
            display='flex',
            flex_flow='row wrap'
        )
    )
    display(board)