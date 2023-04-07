import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import os

# open file from github
url = "https://raw.githubusercontent.com/mqxi/SolarExploration/main/data/Solar_Energy_Production.csv"
res = requests.get(url, allow_redirects=True)
with open("Solar_Energy_Production.csv", "wb") as file:
    file.write(res.content)
solar_energy = pd.read_csv("Solar_Energy_Production.csv")

# print informations
print("Dataframe: ",solar_energy)
print(f"Info: {solar_energy.info()}")
print(f"Buildings: {solar_energy['name'].unique()}")

# solar site by date
site = solar_energy.groupby('name')['installationDate'].unique()
site = pd.DataFrame(site).sort_values(by='installationDate')
print(site)

# solar power production per site
counts = solar_energy.groupby('name')['kWh'].sum()
site_totals = pd.DataFrame(counts).sort_values(by='kWh', ascending=False)
print(site_totals)

site_totals = site_totals.sort_values(by='kWh', ascending=True)

site_totals.plot(figsize=(15, 6), kind='barh', legend=False)
plt.title('Calgary Solar Power Generation per Site [september 2015 to march 2023]')
plt.xlabel('GigaWatt-hours')
plt.ylabel('Site')

# define the directory where you want to save the file
dir_path = os.path.join(os.getcwd(), 'plots')

# create the directory if it doesn't exist
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

plt.savefig(os.path.join(dir_path, 'CalgaryPowerGenerationPerSiteTS.png'))


# create df for time series analysis
solar_energy['date'] = pd.to_datetime(solar_energy['date']) 

df_pw = solar_energy.drop(columns= ['name', 'id', 'address', 'public_url', 'installationDate', 'uid'])
df_pw = df_pw.set_index('date')

#change to daily frequency
count_date = df_pw.groupby(df_pw.index.date)['kWh'].sum()
pw_clean = pd.DataFrame(count_date)
pw_clean['date'] = pd.to_datetime(pw_clean.index)
pw_clean = pw_clean.set_index('date')
pw_clean.head()

#plot the data
pw_clean.plot(style='-', figsize=(20, 7), lw=1,
              title='Calgary Solar Power Production in kWh')
plt.savefig(os.path.join(dir_path, 'CalgarySolarPowerProductionInkWh.png'))

pw_clean.loc[(pw_clean.index > '2022-01-01') & (pw_clean.index < '2023-01-01')] \
    .plot(style='-', figsize=(18, 6), title='1 year of data (Jan/2022 - Jan/2023)')
plt.savefig(os.path.join(dir_path, '1yearOfPowerGeneration.png'))
