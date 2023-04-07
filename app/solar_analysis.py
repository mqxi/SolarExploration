import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import os


class SolarAnalysis:
    def __init__(self, url):
        self.url = url
        self.solar_energy = self.load_data()
        self.dir_path = os.path.join(os.getcwd(), 'plots')
        self.check_dir()

    def load_data(self):
        res = requests.get(self.url, allow_redirects=True)
        with open("Solar_Energy_Production.csv", "wb") as file:
            file.write(res.content)
        solar_energy = pd.read_csv("Solar_Energy_Production.csv")
        return solar_energy

    def check_dir(self):
        # create the directory if it doesn't exist
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

    def print_info(self):
        print(f"Dataframe: {self.solar_energy}")
        print(f"Info: {self.solar_energy.info()}")
        print(f"Describe: {self.solar_energy.describe()}")
        print(f"Buildings: {self.solar_energy['name'].unique()}")

    def site_by_date(self):
        site = self.solar_energy.groupby('name')['installationDate'].unique()
        site = pd.DataFrame(site).sort_values(by='installationDate')
        print(site)
        return site

    def power_production_per_site(self):
        counts = self.solar_energy.groupby('name')['kWh'].sum()
        site_totals = pd.DataFrame(counts).sort_values(by='kWh', ascending=False)
        print(site_totals)

        site_totals = site_totals.sort_values(by='kWh', ascending=True)
        site_totals.plot(figsize=(15, 6), kind='barh', legend=False)
        plt.title('Calgary Solar Power Generation per Site [september 2015 to march 2023]')
        plt.xlabel('GigaWatt-hours')
        plt.ylabel('Site')

        plt.savefig(os.path.join(self.dir_path, 'CalgaryPowerGenerationPerSiteTS.png'))
        return site_totals

    def time_series_analysis(self):
        self.solar_energy['date'] = pd.to_datetime(self.solar_energy['date'])

        df_pw = self.solar_energy.drop(columns=['name', 'id', 'address', 'public_url', 'installationDate', 'uid'])
        df_pw = df_pw.set_index('date')

        # change to daily frequency
        count_date = df_pw.groupby(df_pw.index.date)['kWh'].sum()
        pw_clean = pd.DataFrame(count_date)
        pw_clean['date'] = pd.to_datetime(pw_clean.index)
        pw_clean = pw_clean.set_index('date')
        pw_clean.head()

        # plot the data
        pw_clean.plot(style='-', figsize=(20, 7), lw=1,
                      title='Calgary Solar Power Production in kWh')
        plt.savefig(os.path.join(self.dir_path, 'CalgarySolarPowerProductionInkWh.png'))

        pw_clean.loc[(pw_clean.index > '2022-01-01') & (pw_clean.index < '2023-01-01')] \
            .plot(style='-', figsize=(18, 6), title='1 year of data (Jan/2022 - Jan/2023)')
        plt.savefig(os.path.join(self.dir_path, '1yearOfPowerGeneration.png'))

        return pw_clean

    def analysis(self):
        self.print_info()
        self.site_by_date()
        self.power_production_per_site()
        self.time_series_analysis()
