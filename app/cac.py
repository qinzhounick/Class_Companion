import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


# Values
data = pd.open("data.csv", delimeter=":")

# Plot second column vs. first column
plt.plot(data.iloc[:, 0], data.iloc[:, 1], label="Second column vs First column")
plt.xlabel("First Column")
plt.ylabel("Second Column")
plt.title("Plot of Second Column vs First Column")
plt.legend()
plt.show()