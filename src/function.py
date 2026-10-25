from typing import List
class Function:
    def __init__(self, coef: List[float]):
        self.coef = coef
            
    def __call__(self, x):
        return sum(c*(x**i) for i, c in enumerate(self.coef))