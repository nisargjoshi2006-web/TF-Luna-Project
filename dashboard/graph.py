import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/distance_data.csv")

print(df.head())

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.plot(df["Distance"])
ax.set_ylim(
    df["Distance"].min() - 2,
    df["Distance"].max() + 2
)

ax.set_xlabel("Sample")
ax.set_ylabel("Distance (cm)")

st.pyplot(fig)

plt.xlabel("Sample Number")
plt.ylabel("Distance (cm)")
plt.title("TF-Luna Distance Measurements")

plt.show()