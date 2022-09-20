"""Use the Bank of Canada's valet service to look up exchange rates."""
# Documentation at https://www.bankofcanada.ca/valet/docs

import datetime
import decimal
import json
import urllib.request


def get_fx(from_currency='CAD', to_currency='CAD',
           start_date=None, end_date=None):
    """
    Return the exchange to another currency expressed from a base currency
    on a date or range of dates.

    Parameters
    ----------
    **from_currency**
        The base currency using 3-digit ISO 4217 currency code.
    **to_currency**
        The destination currency using the 3-digit ISO 4217 currency code.
        This will be the cost of the currency expressed in units of the
        ``from_currency``
    **start_date**
        The starting date for which to return an exchange rate.
    **end_date**
        On optional ending date on which to return a dictionary of exchange
        rates.

    Return
    ------
    A dict of exchange rates with key=date and value=exchange rate. If only
    one date is provided, return only the exchange rate value.
    """

    # Match BOC precision
    decimal.getcontext().prec = 5

    from_currency = from_currency[:3].upper()
    to_currency = to_currency[:3].upper()
    
    if from_currency == to_currency:
        return decimal.Decimal(1)

    if not start_date:
        start_date = end_date
    elif not end_date:
        end_date = start_date    

    if from_currency == 'CAD' or to_currency == 'CAD':

        series_name = 'FX' + from_currency + to_currency
        url = ('https://www.bankofcanada.ca/valet/observations/'
               + series_name + '/json')

        if start_date:        
            start_date = datetime.date.fromisoformat(start_date)
            end_date = datetime.date.fromisoformat(end_date)
                
            query = ('?start_date=' + str(start_date)
                     + '&end_date=' + str(end_date))
        else:
            query = '?recent=1'

        with urllib.request.urlopen(url + query) as file:
            json_data = file.read.decode()
            json_data = json.loads(json_data)

            fx_rates = {item['d']: decimal.Decimal(item[series_name]['v'])
                        for item in json_data['observations']}
    else:
        from_currency = get_fx(from_currency, 'CAD', start_date, end_date)
        to_currency = get_fx('CAD', to_currency, start_date, end_date)

        if start_date == end_date:
            return from_currency * to_currency

        fx_rates = {date: decimal.Decimal(value) * to_currency[date]
                    for (date, value) in from_currency}

    if len(fx_rates) == 1:
        return fx_rates.popitem()[1]
    else:
        return fx_rates

# TODO: need to return previous date if start_date is a holiday
