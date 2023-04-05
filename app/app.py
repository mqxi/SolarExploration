import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests

url = "https://raw.githubusercontent.com/mqxi/SolarExploration/9f696e8c658ee121075933904ee874e7093b35ba/data/Solar_Energy_Production.csv"
res = requests.get(url, allow_redirects=True)
with open("Solar_Energy_Production.csv", "wb") as file:
    file.write(res.content)
solar_energy = pd.read_csv("Solar_Energy_Production.csv")
print(solar_energy)