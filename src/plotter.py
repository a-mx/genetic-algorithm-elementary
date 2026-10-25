import matplotlib.pyplot as plt
class Plotter:
    def __init__(self, history):
        self.history = history

    def make_plots(self):
        plt.figure(dpi=100, figsize=(13,5))

        plt.subplot(1,3,1)
        plt.plot(self.history['min'])
        plt.title("Minimalne przystosowanie")
        plt.ylabel("Wartość funkcji")
        plt.xlabel("Pokolenie")

        plt.subplot(1,3,2)
        plt.plot(self.history['avg'])
        plt.title("Średnie przystosowanie")
        plt.ylabel("Wartość funkcji")
        plt.xlabel("Pokolenie")

        plt.subplot(1,3,3)
        plt.plot(self.history['max'])
        plt.title("Maksymalne przystosowanie")
        plt.ylabel("Wartość funkcji")
        plt.xlabel("Pokolenie")
        plt.show()
