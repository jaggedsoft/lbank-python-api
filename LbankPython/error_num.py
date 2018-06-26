error_n={
    '10000':'internal error',
    '10001':'The necessary parameters can not be empty',
    '10002':'Validation does not pass',
    '10003': 'invalid parameter',
    '10004': 'User requests are too frequent',
    '10005': 'Secret——key does not exist',
    '10006': '用户不存在',
    '10007': 'Invalid sign',
    '10008': 'This transaction pair is not supported',
    '10009': 'The limit order should not be short of the price and the number of the orders',
    '10010': 'A single price or a single number must be more than 0',
    '10013': 'The minimum amount of sale that is less than the position of 0.001',
    '10014': 'Insufficient amount of money in account',
    '10015': 'Order type error',
    '10016': 'Insufficient account balance',
    '10017': 'Server exception',
    '10018': 'The number of order query entries should not be larger than 50 less than 1 bars',
    '10019': 'The number of withdrawal entries should not be greater than 3 less than 1',
    '10020': 'Minimum amount of sale less than 0.001',
}

def error_print(a):
    if 'result'in a and a['result'] =='false':
        b = str(a['error_code'])
        return (b,error_n[b])
    else:
        return a

