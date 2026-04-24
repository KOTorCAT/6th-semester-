#!/usr/bin/env python3
"""
Полное сравнение всех итераций
"""

import math
import timeit

# Итерация 1
from integrate import integrate

# Итерации 2-3
from integrate_parallel import integrate_async

# Итерация 4
try:
    from integrate_cython import integrate_cython
    CYTHON_AVAILABLE = True
except:
    CYTHON_AVAILABLE = False
    print("Cython не скомпилирован. Выполните: python3 setup.py build_ext --inplace")

print("="*60)
print("СРАВНЕНИЕ ВРЕМЕНИ ВЫПОЛНЕНИЯ")
print("="*60)

n_iter = 1_000_000

# Итерация 1
print("\n1. Чистый Python:")
t1 = timeit.timeit(lambda: integrate(math.sin, 0, math.pi/2, n_iter=n_iter), number=1)
print(f"   {t1:.4f} сек")

# Итерация 2 (потоки)
print("\n2. Потоки (n_jobs=4):")
t2 = timeit.timeit(lambda: integrate_async(math.sin, 0, math.pi/2, n_jobs=4, n_iter=n_iter, use_processes=False), number=1)
print(f"   {t2:.4f} сек (ускорение: {t1/t2:.2f}x)")

# Итерация 3 (процессы)
print("\n3. Процессы (n_jobs=4):")
t3 = timeit.timeit(lambda: integrate_async(math.sin, 0, math.pi/2, n_jobs=4, n_iter=n_iter, use_processes=True), number=1)
print(f"   {t3:.4f} сек (ускорение: {t1/t3:.2f}x)")

# Итерация 4 (Cython)
if CYTHON_AVAILABLE:
    print("\n4. Cython (sin из C):")
    t4 = timeit.timeit(lambda: integrate_cython(math.sin, 0, math.pi/2, n_iter=n_iter), number=1)
    print(f"   {t4:.4f} сек (ускорение: {t1/t4:.2f}x)")

print("\n" + "="*60)
print("ВЫВОД:")
print("1. Потоки не дают ускорения из-за GIL")
print("2. Процессы дают ускорение ~3-4x")
print("3. Cython с C-функцией дает максимальное ускорение")
print("="*60)