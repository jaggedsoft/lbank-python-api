API_KEY = 'YOUR API KEY'
PRIVATE_KEY = '''YOUR PRIVATE KEY'''


from time import sleep
from LBank import LBankAPI


api = LBankAPI(API_KEY, PRIVATE_KEY)
assets = api.user_assets()
for k, v in assets.items():
    for kk, vv in v.items():
        print (k, kk, vv)

symbol = 'eth_usdt'

order = api.place_order(symbol, 'buy', 1, 1)
order_id = order['order_id']

for _ in range(10):
    status = api.query_order(symbol, order_id)
    status = status['orders'][0]
    filled = status['deal_amount']
    if status['status'] == 2:
        break
    sleep(1)

if status['status'] != 2:
    api.cancel_the_order(symbol, order_id)

print ('Filled Volume:', filled)

