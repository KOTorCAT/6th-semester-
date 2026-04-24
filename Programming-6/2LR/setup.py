from setuptools import setup
from Cython.Build import cythonize

setup(
    name="integrate_cython",
    ext_modules=cythonize("integrate_cython.pyx", compiler_directives={'boundscheck': False})
)