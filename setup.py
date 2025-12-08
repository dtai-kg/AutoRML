from setuptools import setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='autorml',
    version='0.1.3',
    packages=["autorml", "autorml.annotation"],
    install_requires=required,
    author="Ioannis Dasoulas",
    author_email="ioannis.dasoulas@kuleuven.be",
    description="AutoRML: A framework for automatic RML mapping generation "
                "using semantic table annotations",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/dtai-kg/AutoRML",
    license="Apache-2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
    ],
    python_requires='>=3.9, <3.12'
)
