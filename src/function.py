from typing import List


class Function:
    def __init__(self, coef: List[float], x_min: int = -1, x_max: int = 28):
        if x_min > x_max:
            raise ValueError("x_min musi być mniejsze lub równe x_max")

        self.coef = coef
        self.set_domain(x_min, x_max)

    def raw(self, x: int) -> float:
        return sum(c*(x**i) for i, c in enumerate(self.coef))

    def set_domain(self, x_min: int, x_max: int):
        if x_min > x_max:
            raise ValueError("x_min musi być mniejsze lub równe x_max")

        self.x_min = x_min
        self.x_max = x_max
        minimum = min(self.raw(x) for x in range(x_min, x_max + 1))
        self.offset = max(0, -minimum)

    def __call__(self, x):
        return self.raw(x) + self.offset