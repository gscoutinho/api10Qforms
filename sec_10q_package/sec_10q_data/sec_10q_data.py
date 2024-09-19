import requests as req
import pandas as pd
from datetime import datetime, timedelta

def get_data_sec(ticker, email):

    #request header as established in API
    headers = {"user-Agent": email}

    #fetch for company tickers
    res = req.get("https://www.sec.gov/files/company_tickers.json", headers=headers)

    res.raise_for_status()
    df_tickers = pd.DataFrame.from_dict(res.json(), orient='index')


    #add leading zeros to match standard
    df_tickers['cik_str'] = df_tickers['cik_str'].astype(str).str.zfill(10)

    cik_tryout = df_tickers[df_tickers['ticker'] == ticker]

    if cik_tryout.empty:
        raise ValueError(f"Ticker '{ticker}' not found.")
    
    cik = cik_tryout.iloc[0]['cik_str']

    #fetch company facts
    url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
    res = req.get(url, headers=headers)
    res.raise_for_status()
    return res.json()['facts']['us-gaap']


def get_10q_data(ticker, email):
    fillings_us_gaap = get_data_sec(ticker, email)

    print(fillings_us_gaap)

    ten_q_data = {}

    for key, value in fillings_us_gaap.items():
        for unit_key, unit_values in value.get('units', {}).items():
            ten_q_entries = [entry for entry in unit_values if entry.get('form') == '10-Q']
            if ten_q_entries:
                if key not in ten_q_data:
                    ten_q_data[key] = {
                        'label': value.get('label'),
                        'description': value.get('description'),
                        'units': {}
                    }
                ten_q_data[key]['units'][unit_key] = ten_q_entries

    return ten_q_data