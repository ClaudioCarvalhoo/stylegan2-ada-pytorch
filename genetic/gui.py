from tkinter import *
from PIL import ImageTk, Image
from . import genetic_algo
from genetic.generate_from_latent import generate_image


def start_gui(population_size, G):
    window = Tk()
    window.resizable(width=False, height=False)
    window.title('Latent Hiker')
    window.configure(background='black')

    photo1 = ImageTk.PhotoImage(Image.open("./genetic/gato_pizza.jpg").resize((256, 256)))
    Label(window, bg='black', fg='black').grid(row=0, column=0, pady=(5,0))

    population = genetic_algo.generate_initial_population(population_size, G)

    images = []
    sliders = []
    generated_images_cache = []
    row = -1
    for i in range(population_size):
        if i % 5 == 0:
            row += 2
        col = (i % 5)

        generated_image = ImageTk.PhotoImage(generate_image(G, population[i].genes).resize((256, 256)))
        generated_images_cache.append(generated_image)

        image = Label(window, image=generated_image, bg='black')
        image.grid(row=row, column=col, padx=(5, 5))
        images.append(image)
        slider = Scale(window, from_=0, to=10, orient=HORIZONTAL, bg='black', fg='white')
        slider.grid(row=row+1, column=col, pady=(5, 25))
        sliders.append(slider)
    row += 2

    def update():
        nonlocal images
        nonlocal sliders
        fitness = []
        for slider in sliders:
            fitness.append(slider.get())
            slider.configure(state='disabled')

        nonlocal population
        nonlocal mutation_input_box
        population = genetic_algo.evolve(population, fitness, float(mutation_input_box.get()))

        for i in range(population_size):
            generated_image = ImageTk.PhotoImage(generate_image(G, population[i].genes).resize((256, 256)))
            generated_images_cache[i] = generated_image

            images[i].configure(image=generated_image)
            sliders[i].configure(state='normal')
            sliders[i].set(0)
            
        
    Label(window, text='Mutation Rate:', bg='black', fg='white').grid(row=row, column=0)
    row += 1
    mutation_input_box = Entry()
    mutation_input_box.insert(END, '0.01')
    mutation_input_box.grid(row=row, column=0)
    Button(window, text='UPDATE', width=16, bg='white', fg='black', command=update).grid(row=row, column=4)
    row += 1

    Label(window, bg='black', fg='black').grid(row=row, column=0, pady=(5,0))

    window.mainloop()