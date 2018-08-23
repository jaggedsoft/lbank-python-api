API_KEY = 'YOUR API KEY'


PRIVATE_KEY = '''YOUR PRIVATE KEY'''


from LBank import LBankAPI


api = LBankAPI(API_KEY, PRIVATE_KEY)
assets = api.user_assets()
print (assets)
