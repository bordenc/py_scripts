#! /usr/bin/env python3
"""
Use the Bank of Canada's valet service to look up exchange rates.
Documentation at https://www.bankofcanada.ca/valet/docs
"""

import datetime
import decimal
import json
import urllib.request


def get_fx(from_currency='CAD', to_currency='CAD',
           start_date=None, end_date=None):
    """
    Return the exchange to another currency expressed from a base currency
    on a date or range of dates.

    :param from_currency: The base currency using 3-digit ISO 4217 currency
        code.
    :param to_currency: The destination currency using the 3-digit ISO 4217
        currency code. This will be the cost of the currency expressed in
        units of the from_currency
    :param start_date: The starting date for which to return an exchange rate.
    :param end_date: On optional ending date on which to return a dictionary
        of exchange rates.

    :return: A dict of exchange rates with key=date (str) and
        value=exchange rate (decimal.Decimal).

    TODO: add unit tests to see if I did this correctly
    """

    # Match BOC precision
    decimal.getcontext().prec = 5

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    
    if from_currency == to_currency:
        return decimal.Decimal(1)

    if not end_date:
        start_date = end_date
    if not start_date:
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
            json_data = json.load(file)

            fx_rates = {item['d']: decimal.Decimal(item[series_name]['v'])
                        for item in json_data['observations']}
    else:
        from_currency = get_fx(from_currency, 'CAD', start_date, end_date)
        to_currency = get_fx('CAD', to_currency, start_date, end_date)

        if start_date == end_date:
            return from_currency * to_currency

        fx_rates = {date: value * to_currency[date]
                    for (date, value) in from_currency.items()}

    if len(fx_rates) > 1:
        return fx_rates
    if len(fx_rates) == 1:
        # TODO: Make this return one value without breaking other things
        return fx_rates
    else:
        # Bank holidays almost never last more than a week,
        # so back up seven days and pop the most recent observation
        delta = datetime.timedelta(days=7)
        start_date -= delta
        fx_rates = get_fx(from_currency, to_currency,
                          str(start_date), str(end_date))
        key = sorted(fx_rates.keys(), reverse=True)[0]
        return {key: fx_rates[key]}


if __name__ == '__main__':
    from argparse import ArgumentParser
    arg_parser = ArgumentParser(description=__doc__)
    arg_parser.add_argument(
        '--from_currency', default='CAD')
    arg_parser.add_argument(
        '--to_currency', default='CAD')
    arg_parser.add_argument(
        '--from_date', default=None)
    arg_parser.add_argument(
        '--to_date', default=None)
    args = arg_parser.parse_args()
    results = get_fx(args.from_currency, args.to_currency,
                     args.from_date, args.to_date)

    if not hasattr(results, 'keys'):
        key = str(args.from_date)
        results = {key: results}

    print('FX 1.00', args.from_currency, '=')
    for fx_date in results.keys():
        print(fx_date, ':', results[fx_date], args.to_currency)
