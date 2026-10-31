import random
from candidate import Candidate

class Generations:
    def __init__(self,
                 population,
                 p_crossover: float = 0.75,
                 p_mutation: float = 0.001,
                 generation_count: int = 1000):
        
        if not 0 <= p_crossover <= 1:
            raise ValueError("Prawdopodobieństwo krzyżowania musi być w zakresie 0..1")

        if not 0 <= p_mutation <= 1:
            raise ValueError("Prawdopodobieństwo mutacji musi być w zakresie 0..1")

        if generation_count < 0:
            raise ValueError("Liczba pokoleń nie może być ujemna")
        
        self.population = population
        self.fitness_function = self.population.fitness_function
        self.p_crossover = p_crossover
        self.p_mutation = p_mutation
        self.generation_count = generation_count
        self.history = {"min": [], "avg": [], "max": []}
        self.best = None

    def _copy_candidate(self, candidate):
        return Candidate(
            representation=list(candidate.representation),
            fitness_func=self.fitness_function,
            x_min=self.population.x_min,
            x_max=self.population.x_max,
        )

    def _update_best(self):
        candidate = max(self.population, key=lambda item: item.get_fitness())
        if self.best is None or candidate.get_fitness() > self.best.get_fitness():
            self.best = self._copy_candidate(candidate)

    def selection(self):
        sorted_pop = sorted(self.population, key=lambda x: x.get_fitness(), reverse=True)
        n = len(sorted_pop)
        weights = list(range(n, 0, -1))
        chosen = random.choices(sorted_pop, weights=weights, k=n)
        self.population.population = chosen

    def crossover(self):
        new_pop = []
        population = self.population.population
        n = len(population)

        for i in range(0, n - 1, 2):
            parent1 = population[i]
            parent2 = population[i + 1]

            representation1 = list(parent1.representation)
            representation2 = list(parent2.representation)

            if (
                random.random() < self.p_crossover
                and len(representation1) > 1
            ):
                point = random.randint(1, len(representation1) - 1)

                representation1, representation2 = (
                    representation1[:point] + representation2[point:],
                    representation2[:point] + representation1[point:],
                )

            child1 = Candidate(
                representation1,
                self.fitness_function,
                x_min=self.population.x_min,
                x_max=self.population.x_max,
            )

            child2 = Candidate(
                representation2,
                self.fitness_function,
                x_min=self.population.x_min,
                x_max=self.population.x_max,
            )

            if not child1.is_valid():
                child1 = Candidate(
                    fitness_func=self.fitness_function,
                    x_min=self.population.x_min,
                    x_max=self.population.x_max,
                )

            if not child2.is_valid():
                child2 = Candidate(
                    fitness_func=self.fitness_function,
                    x_min=self.population.x_min,
                    x_max=self.population.x_max,
                )

            new_pop.extend([child1, child2])

        if n % 2 == 1:
            last = population[-1]

            new_pop.append(
                Candidate(
                    list(last.representation),
                    self.fitness_function,
                    x_min=self.population.x_min,
                    x_max=self.population.x_max,
                )
            )

        self.population.population = new_pop

    def mutation(self):
        for candidate in self.population:
            old_representation = candidate.representation.copy()

            for index in range(len(candidate.representation)):
                if random.random() < self.p_mutation:
                    candidate.representation[index] = (
                        1 - candidate.representation[index]
                    )

            if not candidate.is_valid():
                candidate.representation = old_representation

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
        self._update_best()
        for _ in range(self.generation_count):
            self.run_generation()
            self.collect_stats()
            self._update_best()
        return self.history