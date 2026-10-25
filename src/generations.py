import random
from candidate import Candidate
from population import Population
class Generations:
    def __init__(self,
                 population,
                 p_crossover: float = 0.75,
                 p_mutation: float = 0.001,
                 generation_count: int = 1000):
        self.population = population
        self.fitness_function = self.population.fitness_function
        self.p_crossover = p_crossover
        self.p_mutation = p_mutation
        self.generation_count = generation_count
        self.history = {"min": [], "avg": [], "max": []}

    def selection(self):
        sorted_pop = sorted(self.population, key=lambda x: x.get_fitness(), reverse=True)
        n = len(sorted_pop)
        weights = list(range(n, 0, -1))
        chosen = random.choices(sorted_pop, weights=weights, k=n)
        self.population.population = chosen

    def crossover(self):
        new_pop = []
        n = len(self.population.population)

        for i in range(0, n - 1, 2):
            c1 = self.population.population[i]
            c2 = self.population.population[i + 1]
            r1 = list(c1.representation)
            r2 = list(c2.representation)

            if random.random() < self.p_crossover:
                k = random.randint(1, len(r1) - 1)
                r1, r2 = r1[:k] + r2[k:], r2[:k] + r1[k:]

            new_pop.append(Candidate(r1, self.fitness_function, x_min=self.population.x_min, x_max=self.population.x_max))
            new_pop.append(Candidate(r2, self.fitness_function, x_min=self.population.x_min, x_max=self.population.x_max))

        if n % 2 == 1:
            last = list(self.population[-1].representation)
            new_pop.append(Candidate(last, self.fitness_function, x_min=self.population.x_min, x_max=self.population.x_max))

        self.population.population = new_pop

    def mutation(self):
        for c in self.population:
            for idx in range(len(c.representation)):
                if random.random() < self.p_mutation:
                    c.representation[idx] = 1 - c.representation[idx]

    def collect_stats(self):
        fits = [c.get_fitness() for c in self.population]
        self.history["min"].append(min(fits))
        self.history["avg"].append(sum(fits) / len(fits))
        self.history["max"].append(max(fits))

    def run_generation(self):
        self.selection()
        self.crossover()
        self.mutation()

    def run(self):
        self.collect_stats()
        for _ in range(self.generation_count):
            self.run_generation()
            self.collect_stats()
        return self.history