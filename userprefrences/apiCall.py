import requests
import json


def RealTimeCurrencyExchangeRate(from_currency, to_currency, api_key):

    base_url = r"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"

    main_url = base_url + "&from_currency=" + from_currency + \
        "&to_currency=" + to_currency + "&apikey=" + api_key

    req_ob = requests.get(main_url)
    result = req_ob.json()
    return result["Realtime Currency Exchange Rate"]['5. Exchange Rate']
