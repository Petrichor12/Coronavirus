import bs4 as bs
import requests
import urllib.request
import pandas as pd
import re
import numpy as np
from os import listdir
from os.path import isfile, join
from datetime import date

url = 'https://www.worldometers.info/coronavirus/'

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

r = requests.get(url, headers=header)

# Read text result into Pandas
dfs = pd.read_html(r.text)
# Look for the first table
df = dfs[0]
# Fill missing values with 0
df = df.fillna(0)

df.to_csv('./Data/world_info.csv')

homepage_soup = bs.BeautifulSoup(r.text, 'lxml')
# Using the table on the main page, only the countries with links (<a> tags) have detailed historical data.
country_elements = homepage_soup.select('table[id="main_table_countries_today"] > tbody > tr > td > a')
# Start with an empty list
countries_with_detailed_data = {}
# Iterate through each element, and add the contents (country name) to a list
for individual_element in country_elements:
    country_name = individual_element.contents[0]
    country_url = individual_element['href']
    countries_with_detailed_data[country_name] = country_url

print("Can get detailed data for %s" % ", ".join(list(countries_with_detailed_data.keys())))


# Looks for script elements that contain the JS stats by day, and extract x and y axis values
def extractDataFromGraph(soup, chart_id):
    scripts = soup.select('script[type="text/javascript"]')
    for individual_script in scripts:
        individual_script = individual_script.get_text(strip=True)
        if (chart_id in individual_script):
            x_text = re.search('categories: \[([^\]]+)\]', individual_script).group(1)
            y_text = re.search('data: \[([0-9, ]+)]', individual_script).group(1)
            x_values = x_text.replace('"', '').split(",")
            y_values = y_text.split(",")
    return (x_values, y_values)


# Iterate over each country and extract the same data, save to CSV
def getDetailedDataForCountry(country, url_part):
    url = 'https://www.worldometers.info/coronavirus/' + url_part
    r = requests.get(url, headers=header).text
    soup = bs.BeautifulSoup(r, 'lxml')
    dates, cases = extractDataFromGraph(soup, "coronavirus-cases-linear")
    cases = pd.to_numeric(cases)
    # a bit risky ignoring dates for the following, if for some reason they are different on different graphs
    active_cases = pd.to_numeric(extractDataFromGraph(soup, "graph-active-cases-total")[1])
    try:
        deaths = pd.to_numeric(extractDataFromGraph(soup, "coronavirus-deaths-linear")[1])
    except:
        deaths = [0] * len(cases)
    try:
        daily_deaths = pd.to_numeric(extractDataFromGraph(soup, "graph-deaths-daily")[1])
    except:
        daily_deaths = [0] * len(cases)
    # daily_cases = extractDataFromGraph(soup, "graph-cases-daily")[1]
    # doesn't work: graph-cases-daily

    # calculate daily cases
    daily_cases = cases * 0
    for i in range(0, len(cases)):
        daily_cases[i] = int(cases[i]) - int(cases[i - 1])
    daily_cases[0] = 0

    # calculate total fatality rate
    CFR = deaths / cases

    # calculate rate of growth of cases
    CGR = cases * 0.0
    for i in range(0, len(cases)):
        try:
            CGR[i] = float(cases[i]) / float(cases[i - 1])
        except:
            CGR[i] = 0.0

    # calculate rate of growth of deaths
    DGR = cases * 0.0
    for i in range(0, len(cases)):
        try:
            DGR[i] = float(deaths[i]) / float(deaths[i - 1])
        except:
            DGR[i] = 0.0

    df_country = pd.DataFrame(
        {'Dates': dates,
         'Cases': cases,
         'Deaths': deaths,
         'Active Cases': active_cases,
         'Daily Cases': daily_cases,
         'Daily Deaths': daily_deaths,
         'CFR': CFR,
         'Cases growth rate': CGR,
         'Deaths growth rate': DGR
         })

    # change daily cases from float to int (it is automatically changed to float in a np.array)
    for i in df_country['Daily Cases']:
        i = int(i)

    df_country = df_country.fillna(0)
    file_name = './Data/Countries/' + country + '.csv'
    df_country.to_csv(file_name)


# Execute the functions to collect data for all countries
for country, url in countries_with_detailed_data.items():
    getDetailedDataForCountry(country, url)


# From country dfs, create dfs for each stat and country over time
def createStatDfs(countries):
    # create empty dfs required
    df_cases = None
    df_cases_2 = pd.DataFrame()
    df_deaths = None
    df_deaths_2 = pd.DataFrame()
    df_daily_cases = None
    df_daily_cases_2 = pd.DataFrame()
    df_daily_deaths = None
    df_daily_deaths_2 = pd.DataFrame()
    df_active_cases = None
    df_active_cases_2 = pd.DataFrame()

    for country in countries:
        file_name = './Data/Countries/' + country + '.csv'
        df = pd.read_csv(file_name)

        # Cases
        if df_cases is None:
            df_cases = df
            df_cases = df_cases.drop(df_cases.columns[[0, 3, 4, 5, 6, 7, 8, 9]], axis=1)
            df_cases = df_cases.set_index('Dates')
            df_cases_2[country] = df_cases['Cases']
        else:
            df_cases = df
            df_cases = df_cases.drop(df_cases.columns[[0, 3, 4, 5, 6, 7, 8, 9]], axis=1)
            df_cases = df_cases.set_index('Dates')
            df_cases = df_cases.rename(columns={'Cases': country})
            df_cases_2 = pd.concat([df_cases_2, df_cases], axis=1, sort=False)

        # Deaths
        if df_deaths is None:
            df_deaths = df
            df_deaths = df.drop(df.columns[[0, 2, 4, 5, 6, 7, 8, 9]], axis=1)
            df_deaths = df_deaths.set_index('Dates')
            df_deaths_2[country] = df_deaths['Deaths']
        else:
            df_deaths = df
            df_deaths = df_deaths.drop(df_deaths.columns[[0, 2, 4, 5, 6, 7, 8, 9]], axis=1)
            df_deaths = df_deaths.set_index('Dates')
            df_deaths = df_deaths.rename(columns={'Deaths': country})
            df_deaths_2 = pd.concat([df_deaths_2, df_deaths], axis=1, sort=False)

        # Daily Cases
        if df_daily_cases is None:
            df_daily_cases = df
            df_daily_cases = df_daily_cases.drop(df_daily_cases.columns[[0, 3, 2, 4, 6, 7, 8, 9]], axis=1)
            df_daily_cases = df_daily_cases.set_index('Dates')
            df_daily_cases_2[country] = df_daily_cases['Daily Cases']
        else:
            df_daily_cases = df
            df_daily_cases = df_daily_cases.drop(df_daily_cases.columns[[0, 3, 2, 4, 6, 7, 8, 9]], axis=1)
            df_daily_cases = df_daily_cases.set_index('Dates')
            df_daily_cases = df_daily_cases.rename(columns={'Daily Cases': country})
            df_daily_cases_2 = pd.concat([df_daily_cases_2, df_daily_cases], axis=1, sort=False)

        # Daily Deaths
        if df_daily_deaths is None:
            df_daily_deaths = df
            df_daily_deaths = df_daily_deaths.drop(df_daily_deaths.columns[[0, 3, 4, 2, 5, 7, 8, 9]], axis=1)
            df_daily_deaths = df_daily_deaths.set_index('Dates')
            df_daily_deaths_2[country] = df_daily_deaths['Daily Deaths']
        else:
            df_daily_deaths = df
            df_daily_deaths = df_daily_deaths.drop(df_daily_deaths.columns[[0, 3, 4, 2, 5, 7, 8, 9]], axis=1)
            df_daily_deaths = df_daily_deaths.set_index('Dates')
            df_daily_deaths = df_daily_deaths.rename(columns={'Daily Deaths': country})
            df_daily_deaths_2 = pd.concat([df_daily_deaths_2, df_daily_deaths], axis=1, sort=False)

        # Active Cases
        if df_active_cases is None:
            df_active_cases = df
            df_active_cases = df_active_cases.drop(df_active_cases.columns[[0, 3, 6, 2, 5, 7, 8, 9]], axis=1)
            df_active_cases = df_active_cases.set_index('Dates')
            df_active_cases_2[country] = df_active_cases['Active Cases']
        else:
            df_active_cases = df
            df_active_cases = df_active_cases.drop(df_active_cases.columns[[0, 3, 6, 2, 5, 7, 8, 9]], axis=1)
            df_active_cases = df_active_cases.set_index('Dates')
            df_active_cases = df_active_cases.rename(columns={'Active Cases': country})
            df_active_cases_2 = pd.concat([df_active_cases_2, df_active_cases], axis=1, sort=False)

    df_cases_2.fillna(0, inplace=True)
    df_cases_2 = df_cases_2.astype(int)

    df_deaths_2.fillna(0, inplace=True)
    df_deaths_2 = df_deaths_2.astype(int)

    df_daily_cases_2.fillna(0, inplace=True)
    df_daily_cases_2 = df_daily_cases_2.astype(int)

    df_daily_deaths_2.fillna(0, inplace=True)
    df_daily_deaths_2 = df_daily_deaths_2.astype(int)

    df_active_cases_2.fillna(0, inplace=True)
    df_active_cases_2 = df_active_cases_2.astype(int)

    df_cases_2.to_csv('./Data/Stats/Cases.csv')
    df_deaths_2.to_csv('./Data/Stats/Deaths.csv')
    df_daily_cases_2.to_csv('./Data/Stats/Daily cases.csv')
    df_daily_deaths_2.to_csv('./Data/Stats/Daily deaths.csv')
    df_active_cases_2.to_csv('./Data/Stats/Active cases.csv')


# Create list of countries
countries = []
for country, url in countries_with_detailed_data.items():
    if country == 'China':  # brings China to front of list
        countries.insert(0, country)
    else:
        countries.append(country)

createStatDfs(countries)

#create datasets used for animations (one long dataframe with all countries)
df = pd.read_csv('./Data/world_info.csv')

path = './Data/Countries'
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

t = pd.date_range(start='1/1/2020', end=date.today().strftime("%m/%d/%Y"))
dt = pd.DataFrame(np.arange(0,len(t), 1), index=t, columns=['Day0'])

countries = []
for c in onlyfiles:
    df = pd.read_csv(path+'/'+c)
    df['Dates'] = df['Dates'].astype(str) + ' 2020'
    df['Dates'] = pd.to_datetime(df['Dates'],format='%b %d %Y')
    df.set_index(df['Dates'],inplace=True)
    df = df.merge(dt,how='right',left_index=True, right_index=True,copy=False)
    df.fillna(0,inplace=True)
    df['Country'] = str.split(c,'.')[0]
    df.reset_index(inplace=True, drop=True)
    df = df[['Day0','Country','Dates','Cases','Deaths','Active Cases','Daily Cases','Daily Deaths','CFR',
            'Cases growth rate', 'Deaths growth rate']]
    df['New Cases Last Week'] = df['Cases'].diff(periods=7)
    df['New Deaths Last Week'] = df['Deaths'].diff(periods=7)
    df['CGR Last Week'] = df['Cases growth rate'].rolling(window=7).mean()
    df['DGR Last Week'] = df['Deaths growth rate'].rolling(window=7).mean()
    df['New Cases'] = df['Cases'].diff()
    df['New Deaths'] = df['Deaths'].diff()
    df['CFR_Current']=df['New Deaths'].rolling(window=28).sum()/df['New Cases'].shift(13).rolling(window=28).sum()
    df['CFR_Total']=df['Deaths']/df['Cases']
    df.fillna(0,inplace=True)
    countries.append(df)

df = pd.concat(countries)
df = df.sort_values(by='Day0')
df.reset_index(inplace=True,drop=True)

df.to_csv('./Data/timeseries.csv')
#df