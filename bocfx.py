# Documentation at https://www.bankofcanada.ca/valet/docs

import urllib.request
import datetime
import json

def get_fx(from_currency='CAD', to_currency='CAD',
           start_date=None, end_date=None):

    from_currency = from_currency[:3].upper()
    to_currency = to_currency[:3].upper()
    
    if from_currency == to_currency:
        return '1.0000'

    if not start_date:
        start_date = end_date
    elif not end_date:
        end_date = start_date    

    if from_currency == 'CAD' or to_currency == 'CAD':

        series_name = 'FX' + from_currency + to_currency
        url = ('https://www.bankofcanada.ca/valet/observations/'
               + series_name + '/json' )

        if start_date:        
            start_date = datetime.date.fromisoformat(start_date)
            end_date = datetime.date.fromisoformat(end_date)
                
            query = ('?start_date=' + str(start_date)
                     + '&end_date=' + str(end_date))
        else:
            query = '?recent=1'
            

        with urllib.request.urlopen(url + query) as file:
            json_data = json.loads(file.read().decode())

            fx_rates = {item['d']:item[series_name]['v']
                        for item in json_data['observations']}
    else:
        from_currency = get_fx(from_currency,'CAD',start_date,end_date)
        to_currency = get_fx('CAD',to_currency,start_date,end_date)

        if start_date == end_date:
            return str(float(from_currency) * float(to_currency))

        fx_rates = {date: str(float(value) * float(to_currency[date]))
                    for (date, value) in from_currency}

    if len(fx_rates) == 1:
        return fx_rates.popitem()[1]
    else:
        return fx_rates

#TODO: need to return previous date if start_date is a holiday
