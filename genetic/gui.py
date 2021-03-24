import tkinter as tk
from PIL import ImageTk, Image
from . import genetic_algo
from genetic.generate_from_latent import generate_image

class LatentHiker(tk.Frame):
    def __init__(self, parent,population_size, G, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure(background='black')

        photo1 = ImageTk.PhotoImage(Image.open("./genetic/gato_pizza.jpg").resize((256, 256)))
        tk.Label(self, bg='black', fg='black').grid(row=0, column=0, pady=(5,0))

        self.G = G
        self.population = genetic_algo.Population(self.G, population_size)

        self.images = []
        self.sliders = []
        self.generated_images_cache = []
        row = -1
        screen_width = self.winfo_screenwidth()
        cells_per_row = screen_width // 280
        for i, individual in enumerate(self.population.individuals):
            if i % (cells_per_row+1) == 0:
                row += 2
            col = (i % (cells_per_row+1))

            generated_image = ImageTk.PhotoImage(generate_image(G, individual.genes).resize((256, 256)))
            self.generated_images_cache.append(generated_image)

            image = tk.Label(self, image=generated_image, bg='black')
            image.grid(row=row, column=col, padx=(5, 5))
            self.images.append(image)
            slider = tk.Scale(self, from_=0, to=10, orient=tk.HORIZONTAL, bg='black', fg='white')
            slider.grid(row=row+1, column=col, pady=(5, 25))
            self.sliders.append(slider)
        row += 2            

        tk.Label(self, text='Mutation Rate:', bg='black', fg='white').grid(row=row, column=0)
        row += 1
        self.mutation_input_box = tk.Entry(self)
        self.mutation_input_box.insert(tk.END, '0.01')
        self.mutation_input_box.grid(row=row, column=0)
        tk.Button(self, text='UPDATE', width=16, bg='white', fg='black', command=self._update).grid(row=row, column=cells_per_row)
        row += 1

        tk.Label(self, bg='black', fg='black').grid(row=row, column=0, pady=(5,0))

    def _update(self):
        fitness = []
        for slider in self.sliders:
            fitness.append(slider.get())
            slider.configure(state='disabled')

        self.population.evolve(fitness, float(self.mutation_input_box.get()))

        for i in range(len(self.population.individuals)):
            generated_image = ImageTk.PhotoImage(generate_image(self.G, self.population.individuals[i].genes).resize((256, 256)))
            self.generated_images_cache[i] = generated_image

            self.images[i].configure(image=generated_image)
            self.sliders[i].configure(state='normal')
            self.sliders[i].set(0)

def start_gui(population_size, G):
    root = tk.Tk()
    root.title('Latent Hiker')
    root.configure(background='black')
    root.state('zoomed')
    # root.resizable(width=False, height=False)

    main_frame = tk.Frame(root, bg='black')
    main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set, background='black')
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * int((e.delta / 60)), "units"))
    second_frame = tk.Frame(canvas, bg='black')
    canvas.create_window((0,0), window=second_frame, anchor='nw')

    LatentHiker(second_frame, population_size, G).pack(fill=tk.BOTH, expand=True)
    root.mainloop()