import math
from libc.math cimport sin

def integrate_cython(f, double a, double b, *, int n_iter=100000):
    """Cython версия"""
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x
    
    if f is math.sin:
        # Используем C-функцию без GIL
        with nogil:
            for i in range(n_iter):
                x = a + i * step
                acc += sin(x) * step
    else:
        # Для Python-функций GIL нужен
        for i in range(n_iter):
            x = a + i * step
            acc += f(x) * step
    
    return acc