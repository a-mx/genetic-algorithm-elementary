from candidate import Candidate
from typing import List
from function import Function
class Population:
    def __init__(self, n: int, fitness_function: Function, x_min: int, x_max: int):
        self.n: int = n
        self.x_min: int = x_min
        self.x_max: int = x_max
        self.fitness_function = fitness_function
        self.population: List[Candidate] = self._make_population(self.n, self.x_min, self.x_max, self.fitness_function)

    @staticmethod
    def _make_population(n: int, x_min: int, x_max: int, fitness_function) -> List[Candidate]:
        population = []
        for _ in range(n):
            population.append(Candidate(fitness_func=fitness_function, x_max=x_max, x_min=x_min))
        return population

    def __repr__(self) -> str:
        return str(self.population)

    def __iter__(self):
        return self.population.__iter__()