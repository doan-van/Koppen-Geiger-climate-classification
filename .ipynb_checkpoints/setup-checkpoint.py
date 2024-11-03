
from setuptools import setup, find_packages

setup(
    name="KoppenClimate",
    version="0.1",
    description="Koppen Climate Classification Tool",
    packages=find_packages(),
    install_requires=["numpy", "matplotlib"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
