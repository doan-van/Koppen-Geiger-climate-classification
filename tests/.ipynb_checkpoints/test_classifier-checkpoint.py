
import numpy as np
from koppen_classification import KoppenClassification

precip = np.array([30, 40, 20, 60, 80, 100, 150, 140, 90, 70, 50, 40])
temp = np.array([10, 12, 15, 18, 20, 25, 30, 28, 22, 15, 12, 8])

koppen = KoppenClassification(precip, temp, south=False)
print("Classification:", koppen.get_classification(writeout=True))

koppen_south = KoppenClassification(precip, temp, south=True)
print("Classification (Southern Hemisphere):", koppen_south.get_classification(writeout=True))

koppen.plot_hythergraph(title="Monthly Temperature and Precipitation")
plt.show()
