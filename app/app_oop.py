import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import os
from solar_analysis import SolarAnalysis

if "__main__" == __name__:
    url = "https://raw.githubusercontent.com/mqxi/SolarExploration/main/data/Solar_Energy_Production.csv"
    sa = SolarAnalysis(url)
    sa.print_info()
    sa.site_by_date()
    sa.power_production_per_site()
    sa.time_series_analysis()
    print("fertig")
