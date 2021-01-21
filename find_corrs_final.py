
import yfinance
import pandas as pd
from os import path


if path.exists('sp500_2020_changes.csv'):
    print('Found the data.')
else:
    print('Fetching data, please wait...\n')
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    
    d={}
    for symbol in sp500['Symbol']:
        try:
            d[symbol] = yfinance.Ticker(symbol).history(period='1y')['Close'].pct_change()[1:]
        except:
            pass
    df = pd.DataFrame(d)
    # for key, val in d.items():
    #    df[key] = val
    df.to_csv('sp500_2020_changes.csv', index=True)
    print('Done\n')
    
sp_full = pd.read_csv('sp500_2020_changes.csv')

if path.exists('sp500_comp_data.csv'):    
    pass
else:
    sp500.to_csv('sp500_comp_data.csv', index=False)
    
sp_metadata = pd.read_csv('sp500_comp_data.csv')
    
d_comp_names = dict(zip(sp_metadata['Symbol'], sp_metadata['Security']))

target = input('Please type in a ticker\n').upper()

if target in sp_full.columns:
    pass
else:
    target_ticker = yfinance.Ticker(target)
    d_comp_names[target] = target_ticker.info['longName']
    sp_full[target] = target_ticker.history(period='1y')['Close'].pct_change()[1:].values
   
sp_full_corr = sp_full.corr()

s = sp_full_corr[target].sort_values().dropna()
s_abs = sp_full_corr[target].apply(abs).sort_values().dropna()

full_tuples = list(zip(s.index, s))
abs_tuples = list(zip(s_abs.index, s_abs))

tupmin = full_tuples[0]
tupmax = full_tuples[-2]
tupmin_abs = abs_tuples[0]

print(f'Selected stock: {d_comp_names[target]} ({target})')
print(f'Stock with largest positive correlation: {d_comp_names[tupmax[0]]} ({tupmax[0]}) with {round(tupmax[1],3)}')
print(f'Stock with largest negative correlation: {d_comp_names[tupmin[0]]} ({tupmin[0]}) with {round(tupmin[1],3)}')
print(f'Stock with smallest correlation: {d_comp_names[tupmin_abs[0]]} ({tupmin_abs[0]}) with {round(tupmin_abs[1],3)}')

input('press Enter to exit')
