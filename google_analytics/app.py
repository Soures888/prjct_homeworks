import os
import requests

# Loading environment variables
measurement_id = os.getenv('MEASUREMENT_ID')
api_secret = os.getenv('API_SECRET')
request_params = {
    'api_secret': api_secret,
    'measurement_id': measurement_id
}


def get_bitcoin_price():
    data = requests.get('https://blockchain.info/ticker').json()
    return data['USD']['last']


def push_data(bitcoin_price: float):
    # Event payload
    payload = {
        'client_id': 'bitcoinprice',
        'non_personalized_ads': False,
        'events': [
            {
                'name': 'bitcoin_price',
                'params': {
                    'currency': 'USD',
                    'value': bitcoin_price
                }
            }
        ]
    }

    # Sending request
    response = requests.post(
        'https://www.google-analytics.com/mp/collect',
        params=request_params,
        json=payload
    )
    print('Sending request...')
    print(response.status_code, response.text)


if __name__ == '__main__':
    push_data(bitcoin_price=get_bitcoin_price())
