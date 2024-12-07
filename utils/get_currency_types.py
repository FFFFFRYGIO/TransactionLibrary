from typing import List

import requests

url = 'https://openexchangerates.org/api/currencies.json'


def get_currency_types() -> List[str]:
    """ get all currency types from openexchangerates.org """

    response = requests.get(url)
    currencies = response.json()

    return list(currencies)
