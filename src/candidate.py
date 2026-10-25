import random
from typing import List
from function import Function
import math
class Candidate:
    def __init__(self, representation: List[int] =None, fitness_func=None, x_min = -1, x_max =28):
        self.x_min = x_min
        self.x_max = x_max
        self.bit_length = math.ceil(math.log2(x_max - x_min + 1))
        self.representation = representation if representation is not None else self._random_representation()
        self.fitness_func = fitness_func if fitness_func is not None else Function([6, 5.5, -0.2])

    def _random_representation(self):
        while True:
            bits = [random.randint(0, 1) for _ in range(self.bit_length)]
            if self.x_min <= self._decode(bits) <= self.x_max:
                return bits

    def _decode(self, bits):
        code = 0
        for bit in bits:
            code = code * 2 + bit
        n = self.x_max - self.x_min + 1
        return self.x_min + (code % n)

    def get_value(self) -> int:
        return self._decode(self.representation)

    

    def get_fitness(self) -> float:
        x = self.get_value()
        return self.fitness_func(x)
    
    
    def __repr__(self) -> str:
        return str(self.representation) \
        + f" Value: {self.get_value():.2f}" \
        + f" Fitness: {self.get_fitness():.2f}\n"