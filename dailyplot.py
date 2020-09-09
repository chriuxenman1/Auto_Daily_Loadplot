import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
%matplotlib notebook # Code written with Jupyter notebook

# Import data with date in first column and load data from 2018 to 2020 for different households in other columns
df = pd.read_csv('load_data.csv', index_col=0, sep=';', parse_dates=True, infer_datetime_format=True, dayfirst=True)
df.index.freq = '15T' # set frequency

# Set UTC timestamp
df.index = df.index.tz_localize('UTC') # df.index with utc timestamp
df.index = df.index.tz_convert('Europe/Berlin') # df.index conversion to european timestamp

# Create a list with years and months combined as: "2018-01", "2018-02", ..., "2020-12"
years = ["2018", "2019", "2020"]
months = ["01","02","03","04","05","06","07","08","09","10","11","12"] 
year_month = []
for y in years:
    for m in months:
        yemo = "{}-{}".format(y, m)
        year_month.append(yemo)

# Control of how many days a month has and saving it in a list as: [31, 28, 31, 30, ...] 
days_per_month = []
for yemo in year_month:
    lix = str(df[yemo].index[-1]) # save as string
    nod = lix[8:10]
    days_per_month.append(nod)

# Create a list of lists with the following purpose:
# - For every element in days_per_month a list is created with the number of days per month as: [[1,2,3,...,31],[1,2,...,28],[...],...]
# - Example for days_per_month[0]: The number 31 is going to be [1,2,3,...31]
li_days_per_month = []
for d in days_per_month:
    li_days_per_month.append(list(range(1,int(d)+1)))
    
# Convert every int element in str_days_per_month to str
str_days_per_month = []
for n in li_days_per_month:
    n = [str(n) for n in n]
    str_days_per_month.append(n)

# append the tick "-" to year_month
year_month_added = []
for e in year_month:
    year_month_added.append(e + '-')
    
# Combine every month with the number of days: [2018-01-1, 2018-01-2, ..., 2020-12-30, 2020-12-31]
datum = [f"{i}{k}" for i, j in zip(year_month_added, str_days_per_month) for k in j]

# Plot the daily load data and save it in the directory in a dedicate folder, e.g. every daily load plot for house1 is stored in the folder "house1" in the dict
for house in list(df.columns):
    # Create a folder in path, if it does not exist
    from pathlib import Path
    Path(house).mkdir(parents=True, exist_ok=True)
    for day in datum:
        # Clear RAM
        plt.close('all')
        # Save weekday as a string and convert it to the corresponding label of the day (MO, TU, WE, ...)
        datum_dayofweek = pd.to_datetime(day).dayofweek
        if datum_dayofweek==0:
            datum_dayofweek = "MO"
        elif datum_dayofweek==1:
            datum_dayofweek = "TU"        
        elif datum_dayofweek==2:
            datum_dayofweek = "WE"      
        elif datum_dayofweek==3:
            datum_dayofweek = "TH"      
        elif datum_dayofweek==4:
            datum_dayofweek = "FR"      
        elif datum_dayofweek==5:
            datum_dayofweek = "SA"  
        elif datum_dayofweek==6:
            datum_dayofweek = "SU"          
        # Generate title
        png_title = day + "_" + datum_dayofweek + "_" + house 
        # Create plot
        content = df.filter(like=house)[day]
        plt.figure(figsize=(9,6))
        plt.title(f"{png_title}")
        plt.plot(content)
        plt.ylim(0, 1000)
        # Save png
        plt.savefig(f'{house}/{png_title}.png', bbox_inches='tight')
