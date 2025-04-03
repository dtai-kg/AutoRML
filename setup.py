from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='autorml',
    version='0.1.0',
    packages=find_packages(),
    install_requires=required,
    #conda_deps=[],  # Path to your exported YAML file
)