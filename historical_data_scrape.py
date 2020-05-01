import os
from datetime import datetime
import time

import pandas as pd 
import requests 

start_time_date = datetime.now()
#start_time = time.time()
start_time_str = start_time_date.strftime('%Y-%m-%d %H:%M:%S')
print(f'Started at {start_time_str}')

sp500_element_data = pd.read_csv('../data/SP500_Data.csv', index_col=0)

tickers = sp500_element_data['Symbol'].to_list()

url = 'https://query1.finance.yahoo.com/v7/finance/download/'

list_of_dfs = []

start_time = 345427200 #Max date, use this for testing 1586044800 
end_time = 1586649600
interval = '1d'

for ticker in tickers:
    try:
        print(f'---------------------- {ticker} ----------------------')
        parameters = f'{ticker}?period1={start_time}&period2={end_time}&interval={interval}&events=history&frequency=1d'

        request_url = url + parameters
        r = requests.get(request_url)

        print(request_url)
        lines = r.text.split('\n')

        header = lines[0].split(',')
        rows = []
        index = []
        for line in lines[1:]:
            try:
                #print('----------------------------------------------------')
                #print(line)

                commas = line.split(',')
                #for comma in commas:
                #    print(comma)

                #each_index = commas[0]
                #index.append(each_index)

                rows.append(commas)

                df = pd.DataFrame(
                    data=rows, 
                    columns= header
                )

                #print(df.head())
            except:
                pass
        df = df.set_index(header[0])
        # print(df.head())
        list_of_dfs.append(df)

        #print(list_of_dfs)

        df.to_csv(f'../data/{ticker}.csv', index='Date')
    
    except:
        pass


end_time = datetime.now()
end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
print(f'Finished at {end_time_str}')

#total_time = (time.time() - start_time)

#print(f'Total time {total_time}')