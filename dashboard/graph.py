import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/distance_data.csv")

plt.plot(df["Time"], df["Distance"])
plt.xlabel("Time")
plt.ylabel("Distance (cm)")
plt.title("Distance Measurements")
plt.show()