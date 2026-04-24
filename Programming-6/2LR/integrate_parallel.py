#!/usr/bin/env python3
"""
Параллельное вычисление интеграла с потоками и процессами
"""

import math
import timeit
from typing import Callable
import concurrent.futures as ftres
from functools import partial


def integrate(f: Callable[[float], float], 
              a: float, 
              b: float, 
              *, 
              n_iter: int = 100000) -> float:
    """Вычисление интеграла"""
    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate_async(f: Callable[[float], float],
                   a: float,
                   b: float,
                   *,
                   n_jobs: int = 2,
                   n_iter: int = 1000,
                   use_processes: bool = False) -> float:
    """
    Параллельное вычисление интеграла
    
    Parameters
    ----------
    use_processes : bool
        True - процессы (ProcessPoolExecutor)
        False - потоки (ThreadPoolExecutor)
    """
    executor_class = ftres.ProcessPoolExecutor if use_processes else ftres.ThreadPoolExecutor
    
    with executor_class(max_workers=n_jobs) as executor:
        step = (b - a) / n_jobs
        iter_per_job = n_iter // n_jobs
        
        futures = []
        for i in range(n_jobs):
            sub_a = a + i * step
            sub_b = a + (i + 1) * step
            futures.append(executor.submit(integrate, f, sub_a, sub_b, n_iter=iter_per_job))
        
        return sum(f.result() for f in ftres.as_completed(futures))


if __name__ == "__main__":
    n_iter = 1_000_000
    
    print("=== Итерация 2: Потоки ===")
    for n_jobs in [2, 4, 6, 8]:
        t = timeit.timeit(
            lambda: integrate_async(math.sin, 0, math.pi/2, 
                                   n_jobs=n_jobs, n_iter=n_iter, 
                                   use_processes=False),
            number=1
        )
        print(f"n_jobs={n_jobs}: {t:.4f} сек")
    
    print("\n=== Итерация 3: Процессы ===")
    for n_jobs in [2, 4, 6, 8]:
        t = timeit.timeit(
            lambda: integrate_async(math.sin, 0, math.pi/2,
                                   n_jobs=n_jobs, n_iter=n_iter,
                                   use_processes=True),
            number=1
        )
        print(f"n_jobs={n_jobs}: {t:.4f} сек")