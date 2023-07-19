import tkinter as tk
from tkinter import filedialog, messagebox
import turtle
import random
import time
import os


class GameOfLife:
    def __init__(self, l, t, sigma):
        self.l = l
        self.t = t
        self.sigma = sigma
        self.grid = self.create_grid()

    def create_grid(self):
        grid = []
        for _ in range(self.l):
            row = []
            for _ in range(self.l):
                if random.random() < self.sigma:
                    row.append(1)
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def update_generation(self):
        new_grid = []
        for row in range(self.l):
            new_row = []
            for col in range(self.l):
                count = self.count_neighbors(row, col)
                if self.grid[row][col] == 1:
                    if count < 2 or count > 3:
                        new_row.append(0)
                    else:
                        new_row.append(1)
                else:
                    if count == 3:
                        new_row.append(1)
                    else:
                        new_row.append(0)
            new_grid.append(new_row)
        self.grid = new_grid

    def count_neighbors(self, row, col):
        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                neighbor_row = (row + i + self.l) % self.l
                neighbor_col = (col + j + self.l) % self.l
                count += self.grid[neighbor_row][neighbor_col]
        return count


class GameOfLifeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Game of   Life')

        # Frame per i pulsanti
        button_frame = tk.Frame(self.window)
        button_frame.pack()
        self.button_start = tk.Button(button_frame, text='Avvia Simulazione', command=self.start_simulation)
        self.button_start.pack(side=tk.LEFT)
        self.button_load = tk.Button(button_frame, text='Carica Simulazione', command=self.load_simulation)
        self.button_load.pack(side=tk.LEFT)
        
        # Frame per le entry e le label
        entry_frame = tk.Frame(self.window)
        entry_frame.pack()
        self.label_l = tk.Label(entry_frame, text='Lato (l):')
        self.label_l.pack(side=tk.LEFT)
        self.entry_l = tk.Entry(entry_frame)
        self.entry_l.pack(side=tk.LEFT)
        self.label_t = tk.Label(entry_frame, text='Numero di passi (t):')
        self.label_t.pack(side=tk.LEFT)
        self.entry_t = tk.Entry(entry_frame)
        self.entry_t.pack(side=tk.LEFT)
        self.label_sigma = tk.Label(entry_frame, text='Percentuale di riempimento (0<σ<1):')
        self.label_sigma.pack(side=tk.LEFT)
        self.entry_sigma = tk.Entry(entry_frame)
        self.entry_sigma.pack(side=tk.LEFT)
        self.button_save = tk.Button(self.window, text='Salva Simulazione', command=self.save_simulation)
        self.button_save.pack()
        
        self.turtle_pen = None

        self.game = None
        self.window.mainloop()

    def start_simulation(self):
        l = int(self.entry_l.get())
        t = int(self.entry_t.get())
        sigma = float(self.entry_sigma.get())
        print("l = ", l)
        print("t = ", t)
        print("s = ", sigma)
        self.game = GameOfLife(l, t, sigma)
        self.l = l  # Inizializza l'attributo 'l' nella classe

        self.turtle_screen = turtle.Screen()
        self.turtle_screen.title('Game of Life')
        self.turtle_screen.setup(width=800, height=800)

        turtle.TurtleScreen._RUNNING=True
        self.turtle_pen = turtle.Turtle()
        self.turtle_pen.speed(0)
        self.turtle_pen.hideturtle()

        cell_size = 800 / l

        for _ in range(t):
            self.draw_grid(self.turtle_pen, cell_size)
            self.game.update_generation()

        self.turtle_screen.bye()



    def load_simulation(self):
        filename = tk.filedialog.askopenfilename(
            title='Carica Simulazione', filetypes=[('Text Files', '*.txt')])
        if filename:
            print(filename)
            try:
                with open(filename, 'r') as file:
                    lines = file.readlines()
                    l = len(lines)
                    t = int(self.entry_t.get())
                    # sigma = float(self.entry_sigma.get())
                    self.game =GameOfLife(l, t, 0.1)
                    for row, line in enumerate(lines):
                        for col, value in enumerate(line.strip()):
                            self.game.grid[row][col] =int(value)
                
                    turtle.TurtleScreen._RUNNING=True
                    turtle_screen = turtle.Screen()
                    turtle_screen.title('Game of Life')
                    turtle_screen.setup(width=800, height=800)

                    turtle_pen = turtle.Turtle()
                    turtle_pen.speed(0)
                    turtle_pen.hideturtle()

                    cell_size = 800 / l

                    for _ in range(t):
                        self.draw_grid(turtle_pen, cell_size)
                        self.game.update_generation()

                    turtle_screen.bye()

            except Exception as e:
                messagebox.showerror(
                    'Errore', 'Si è verificato un errore durante il caricamento del file.')

    #def save_document(document, folder):
    #    file_path = os.path.join(folder, document)
#
    #    if os.path.exists(file_path):
    #        print("File con questo nome già esistente.")
    #        choice = input("Vuoi sovrascrivere il file? (s/n): ")
#
    #        if choice.lower() != 's':
    #            return  # Esce dalla funzione se la scelta non è di sovrascrivere
#
    #    with open(file_path, 'w') as file:
    #        # Scrivi il contenuto del documento nel file
    #        file.write(document)
#
    #    print(f"Documento salvato correttamente in {file_path}")
    
    def save_simulation(self):
        filename = tk.filedialog.asksaveasfilename(
            title='Salva Simulazione', defaultextension='.txt')
        if filename:
            try:
                with open(filename, 'w') as file:
                    for row in self.game.grid:
                        line = ''.join(map(str, row))
                        file.write(line + '\n')

                messagebox.showinfo(
                    'Salvataggio', 'Simulazione salvata correttamente.')

            except Exception as e:
                messagebox.showerror(
                    'Errore', 'Si è verificato un errore durante il salvataggio del file.')

    def draw_grid(self, pen, cell_size):
        pen.reset()
        turtle_screen = pen.getscreen()
        turtle_screen.tracer(0)

        pen.hideturtle()  # Nascondi la freccia di turtle

        # Disegna la griglia fissa
        pen.penup()
        x_start = -400
        y_start = 400

        # Disegna le linee verticali
        for col in range(self.l + 1):
            x = x_start + col * cell_size
            y1 = y_start
            y2 = y_start - self.l * cell_size
            pen.goto(x, y1)
            pen.pendown()
            pen.goto(x, y2)
            pen.penup()

        # Disegna le linee orizzontali
        for row in range(self.l + 1):
            y = y_start - row * cell_size
            x1 = x_start
            x2 = x_start + self.l * cell_size
            pen.goto(x1, y)
            pen.pendown()
            pen.goto(x2, y)
            pen.penup()

        # Disegna le celle colorate
        for row in range(len(self.game.grid)):
            for col in range(len(self.game.grid[row])):
                x = x_start + col * cell_size + 1
                y = y_start - row * cell_size - 1

                pen.penup()
                pen.goto(x, y)

                if self.game.grid[row][col] == 1:
                    pen.pendown()
                    pen.fillcolor('black')
                    pen.begin_fill()
                    for _ in range(4):
                        pen.forward(cell_size - 2)
                        pen.right(90)
                    pen.end_fill()

        turtle_screen.update()
        time.sleep(1)


gui = GameOfLifeGUI()
