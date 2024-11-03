# Koppen–Geiger climate classification

Created by DOAN Quang Van @ Center for Computational Sciences, University of Tsukuba

Update: 03 November 2024

**KoppenClimate** is a Python library for classifying climates based on the Köppen-Geiger climate classification system. It includes tools for calculating climate classification based on temperature and precipitation data and can visualize monthly temperature and precipitation as a hythergraph.

## Features

- Classify climate types according to the Köppen-Geiger climate classification system.
- Calculate and output key climate statistics (e.g., mean temperature, annual precipitation).
- Plot hythergraphs for visualizing monthly temperature and precipitation data.

## Installation

1.  pip install git+https://github.com/doan-van/Koppen-Geiger-climate-classification.git

2. Or download the 
3. Install the package using pip:
    ```bash
    pip install .
    ```

## Usage

### Importing the Library

```python
from koppen_classification import KoppenClassification
import numpy as np
