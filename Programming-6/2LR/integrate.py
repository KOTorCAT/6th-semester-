#!/usr/bin/env python3
"""
Модуль для численного интегрирования методом прямоугольников
"""

import math
import timeit
from typing import Callable
import unittest


def integrate(f: Callable[[float], float], 
              a: float, 
              b: float, 
              *, 
              n_iter: int = 100000) -> float:
    """
    Вычисление определенного интеграла методом левых прямоугольников.
    
    Parameters
    ----------
    f : Callable[[float], float]
        Подынтегральная функция
    a : float
        Нижний предел интегрирования
    b : float
        Верхний предел интегрирования
    n_iter : int, optional
        Количество итераций (по умолчанию 100000)
        
    Returns
    -------
    float
        Приближенное значение интеграла
        
    Examples
    --------
    >>> integrate(math.sin, 0, math.pi/2, n_iter=1000)
    0.9992143962198362
    >>> integrate(lambda x: x**2, 0, 1, n_iter=1000)
    0.3328335000000001
    """
    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


class TestIntegrate(unittest.TestCase):
    def test_sin(self):
        """Проверка интеграла sin(x) от 0 до π/2"""
        result = integrate(math.sin, 0, math.pi/2, n_iter=100000)
        self.assertAlmostEqual(result, 1.0, places=4)
    
    def test_polynomial(self):
        """Проверка интеграла x² от 0 до 1"""
        result = integrate(lambda x: x**2, 0, 1, n_iter=100000)
        self.assertAlmostEqual(result, 1/3, places=4)
    
    def test_convergence(self):
        """Проверка устойчивости к изменению числа итераций"""
        result1 = integrate(math.sin, 0, math.pi/2, n_iter=1000)
        result2 = integrate(math.sin, 0, math.pi/2, n_iter=100000)
        self.assertLess(abs(result2 - 1), abs(result1 - 1))


if __name__ == "__main__":
    # Doctest
    print("=== Doctest ===")
    import doctest
    doctest.testmod(verbose=True)
    
    # Unittest
    print("\n=== Unittest ===")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Замер времени
    print("\n=== Замер времени ===")
    for n_iter in [10000, 100000, 1000000]:
        t = timeit.timeit(
            lambda: integrate(math.sin, 0, math.pi/2, n_iter=n_iter),
            number=1
        )
        print(f"n_iter={n_iter}: {t:.4f} сек")