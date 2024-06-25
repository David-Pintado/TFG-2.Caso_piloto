from setuptools import find_packages, setup

setup(
    name='pythonLib',
    packages=find_packages(include=['pythonLib']),
    version='0.1.0',
    description='Libreria de Python del segundo caso piloto',
    author='David Pintado Gómez',
    install_requires=[],
    setup_requires=['pytest-runner'],
)