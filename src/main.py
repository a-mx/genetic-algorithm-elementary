
from population import Population
from generations import Generations
from plotter import Plotter
from function import Function
import tkinter as tk
from tkinter import ttk, messagebox
import random

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


FITNESS_FUNCTIONS = {
    "kwadratowa (testowa)": Function([6, 5.5, -0.2]),
    "liniowa":           Function([1, -2]),
    "stała":             Function([10]),
}

class GAApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("AE")

        params = ttk.LabelFrame(root, text="Parametry")
        params.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.pop_size = tk.IntVar(value=20)
        self.p_cross = tk.DoubleVar(value=0.5)
        self.p_mut = tk.DoubleVar(value=0.01)
        self.gen_count = tk.IntVar(value=100)
        self.func_name = tk.StringVar(value=list(FITNESS_FUNCTIONS)[0])

        self.x_min = tk.IntVar(value=-1)
        self.x_max = tk.IntVar(value=28)
        
        self.seed = tk.StringVar(value="")

        self.pop_size_entry   = ttk.Entry(params, textvariable=self.pop_size)
        self.p_cross_entry    = ttk.Entry(params, textvariable=self.p_cross)
        self.p_mut_entry      = ttk.Entry(params, textvariable=self.p_mut)
        self.gen_count_entry  = ttk.Entry(params, textvariable=self.gen_count)
        self.x_min_entry = ttk.Entry(params, textvariable=self.x_min)
        self.x_max_entry = ttk.Entry(params, textvariable=self.x_max)
        

        self.func_combo = ttk.Combobox(
            params, textvariable=self.func_name,
            values=list(FITNESS_FUNCTIONS), state="readonly")

        self.seed_entry = ttk.Entry(params, textvariable=self.seed)

        rows = [
            ("Liczebność populacji:", self.pop_size_entry),
            ("P. krzyżowania:",       self.p_cross_entry),
            ("P. mutacji:",           self.p_mut_entry),
            ("Liczba pokoleń:",       self.gen_count_entry),
            ("Funkcja przystosowania:",  self.func_combo),
            ("x min:", self.x_min_entry),
            ("x max:", self.x_max_entry),
            ("Ziarno:",               self.seed_entry),
        ]

        for r, (label, widget) in enumerate(rows):
            ttk.Label(params, text=label).grid(row=r, column=0, sticky="w", pady=2)
            widget.grid(row=r, column=1, sticky="ew", pady=2)

        self.func_combo.bind("<<ComboboxSelected>>", self.on_function_selected)

        ttk.Button(params, text="Uruchom", command=self.run_ga)\
            .grid(row=len(rows), column=0, columnspan=2, pady=10, sticky="ew")

        self.result = tk.Text(params, height=9, width=32, state="disabled")
        self.result.grid(row=len(rows) + 1, column=0, columnspan=2)

        plots = ttk.Frame(root)
        plots.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        self.fig_func = Figure(figsize=(6, 3.2))
        self.ax_func = self.fig_func.add_subplot(111)
        self.canvas_func = FigureCanvasTkAgg(self.fig_func, plots)
        self.canvas_func.get_tk_widget().pack(fill="both", expand=True)

        self.fig_hist = Figure(figsize=(6, 3.2))
        self.ax_hist = self.fig_hist.add_subplot(111)
        self.canvas_hist = FigureCanvasTkAgg(self.fig_hist, plots)
        self.canvas_hist.get_tk_widget().pack(fill="both", expand=True)

        self.draw_function(FITNESS_FUNCTIONS[self.func_name.get()])

    def on_function_selected(self, event=None):
        self.draw_function(FITNESS_FUNCTIONS[self.func_name.get()])
        self.result.configure(state="normal")
        self.result.delete("1.0", tk.END)
        self.result.configure(state="disabled")

    def run_ga(self):
        try:
            if self.seed.get().strip():
                random.seed(int(self.seed.get()))

            fitness = FITNESS_FUNCTIONS[self.func_name.get()]
            n = self.pop_size.get()

            x_min = self.x_min.get()
            x_max = self.x_max.get()
            population = Population(n, fitness, x_min=x_min, x_max=x_max)

            gen = Generations(
                population=population,
                p_crossover=self.p_cross.get(),
                p_mutation=self.p_mut.get(),
                generation_count=self.gen_count.get(),
            )
            history = gen.run()

            best = max(gen.population, key=lambda c: c.get_fitness())
            self.show_result(best, fitness)
            self.draw_function(fitness)
            print(history)
            self.draw_history(history)

        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def show_result(self, best, fitness):
        self.result.configure(state="normal")
        self.result.delete("1.0", tk.END)
        self.result.insert(tk.END, f"Najlepszy x: {best.get_value()}\n")
        self.result.insert(tk.END, f"Najlepsze przystosowanie: {best.get_fitness():.2f}\n")
        self.result.configure(state="disabled")

    def draw_function(self, fitness):
        self.ax_func.clear()
        xs = list(range(self.x_min.get(), self.x_max.get() + 1))
        ys = [fitness(x) for x in xs]
        self.ax_func.plot(xs, ys, "o-", markersize=3, color="blue")
        self.ax_func.set_title("Funkcja przystosowania")
        self.ax_func.set_xlabel("x")
        self.ax_func.set_ylabel("f(x)")
        self.ax_func.grid(True, alpha=0.3)
        self.fig_func.tight_layout()
        self.canvas_func.draw()

    def draw_history(self, history):
        self.ax_hist.clear()
        gens = list(range(len(history["max"])))
        self.ax_hist.plot(gens, history["max"], label="max", color="green")
        self.ax_hist.plot(gens, history["avg"], label="średnia", color="blue")
        self.ax_hist.plot(gens, history["min"], label="min", color="red")
        self.ax_hist.set_title("Przystosowanie w pokoleniach")
        self.ax_hist.set_xlabel("Pokolenie")
        self.ax_hist.set_ylabel("Przystosowanie")
        self.ax_hist.legend()
        self.ax_hist.grid(True, alpha=0.3)
        self.fig_hist.tight_layout()
        self.canvas_hist.draw()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x720")
    app = GAApp(root)
    root.mainloop()