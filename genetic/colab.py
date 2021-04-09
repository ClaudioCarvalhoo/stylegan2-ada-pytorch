from __future__ import print_function
from IPython.display import Image, clear_output, display
from ipywidgets import interact, interactive, fixed, interact_manual, Layout, Box, Label
import ipywidgets as widgets
from . import genetic_algo
from genetic.generate_from_latent import generate_image, load_network
import io


def _update(sliders, population, mutationInput, G, board):
    fitness = []
    for slider in sliders:
        fitness.append(slider.value)

    population.evolve(fitness, float(mutationInput.value))

    phenotypes = []
    for i in range(len(population.individuals)):
        generated_image = generate_image(G, population.individuals[i].genes)
        slider = widgets.IntSlider(
            value=0, min=0, max=10, readout=False, layout=Layout(width="90%")
        )
        image = widgets.Image(
            value=image_to_byte_array(generated_image),
            format="jpg",
            width="90%",
        )
        phenotype = widgets.VBox([image, slider])
        phenotypes.append(phenotype)
    board.children = phenotypes


def image_to_byte_array(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format="JPEG")
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def run_colab(population_size, network_pkl):
    G = load_network(network_pkl)
    population = genetic_algo.Population(G, population_size)
    phenotypes = []
    sliders = []
    for individual in population.individuals:
        generated_image = generate_image(G, individual.genes)
        slider = widgets.IntSlider(
            value=0, min=0, max=10, readout=False, layout=Layout(width="90%")
        )
        image = widgets.Image(
            value=image_to_byte_array(generated_image),
            format="jpg",
            width="90%",
        )
        phenotype = widgets.VBox([image, slider])
        phenotypes.append(phenotype)
        sliders.append(slider)
    board = Box(
        children=phenotypes, layout=Layout(display="flex", flex_flow="row wrap")
    )

    mutationInput = widgets.BoundedFloatText(
        value=0.01,
        min=0.0,
        max=1.0,
        step=0.01,
    )
    button = widgets.Button(description="Update")
    button.on_click(lambda _: _update(sliders, population, mutationInput, G, board))
    mutationInputBox = widgets.VBox([Label("Taxa de mutação:"), mutationInput])
    bottomBox = Box(
        children=[mutationInputBox, button],
        layout=Layout(
            display="flex",
            width="100%",
            justify_content="space-between",
            align_items="flex-end",
            padding="0 15% 0 0",
        ),
    )

    app = widgets.VBox([board, bottomBox])
    display(app)
