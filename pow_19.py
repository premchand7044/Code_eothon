class Pow:
    def pow(self, x: float, n: int) -> float:
        if x == 0:
            return 0
        if n == 0:
            return 1
        if n < 0:
            return 1 / self.pow(x, -n)

        result = self.pow(x, n // 2)
        if n % 2 == 0:
            return result * result
        else:
            return result * result * x