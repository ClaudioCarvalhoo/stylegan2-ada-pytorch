from __future__ import print_function
from IPython.display import Image, clear_output, display
from ipywidgets import interact, interactive, fixed, interact_manual, Layout, Box, Label
import ipywidgets as widgets
from . import genetic_algo
from genetic.generate_from_latent import generate_image, load_network
import io


def _update(population, mutationInput, G, board, loading, button):
    button.disabled = True
    mutationInput.disabled = True
    fitness = [phenotype.children[1].value for phenotype in board.children]
    population.evolve(fitness, float(mutationInput.value))
    loading.value = 0
    board.children = _generate_phenotypes(population, G, loading)
    button.disabled = False
    mutationInput.disabled = False

def _generate_phenotypes(population, G, loading=None):
    phenotypes = []
    for individual in population.individuals:
            generated_image = generate_image(G, individual.genes)
            slider = widgets.IntSlider(value=0, min=0, max=10, readout=False, layout=Layout(width="95%"))
            image = widgets.Image(
                value=_image_to_byte_array(generated_image),
                format="jpg",
                width=256,
            )
            phenotype = widgets.VBox([image, slider])
            phenotypes.append(phenotype)
            if loading is not None:
                loading.value += 100/len(population.individuals)
    return phenotypes

def _image_to_byte_array(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format="JPEG")
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def run_colab(population_size, network_pkl):
    G = load_network(network_pkl)
    population = genetic_algo.Population(G, population_size)
    
    phenotypes = _generate_phenotypes(population, G)
    board = Box(children=phenotypes, layout=Layout(display="flex", flex_flow="row wrap"))

    mutationInput = widgets.BoundedFloatText(value=0.01,min=0.0,max=1.0,step=0.01, layout=Layout(width="100px"))
    button = widgets.Button(description="Update")
    button.on_click(lambda _: _update(population, mutationInput, G, board, loading, button))
    mutationInputBox = widgets.VBox([Label("Taxa de mutação:"), mutationInput])
    loading = widgets.FloatProgress(
      value=100,
      min=0,
      max=100,
      bar_style='info',
      style={'bar_color': '#008080'},
      orientation='horizontal'
    ) 
    bottomBox = Box(
        children=[mutationInputBox, loading, button],
        layout=Layout(
            display="flex",
            width="100%",
            justify_content="space-between",
            align_items="flex-end",
            padding="0 15% 20px 0",
        ),
    )

    app = widgets.VBox([board, bottomBox])
    display(app)
