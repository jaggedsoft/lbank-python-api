import requests
import time
import json
import hashlib

from LbankPython.error_num import error_print

class Lbank_Api():


    LBANK_API_URL = 'http://172.16.1.93:8081/'
    PAIR_QUOTATION_URL = LBANK_API_URL+'v1/ticker.do'
    ALL_PAIR_DATA=LBANK_API_URL+'v1/accuracy.do'
    AVAILABLE_PAIR_URL = LBANK_API_URL+'v1/currencyPairs.do'
    MARKET_DEPTH_URL =LBANK_API_URL+ 'v1/depth.do'
    HISTORICAL_TRANSACTION_URL =LBANK_API_URL+ 'v1/trades.do'
    KLINE_DATA_URL =LBANK_API_URL+ 'v1/kline.do'
    GET_USER_ASSETS_URL =LBANK_API_URL+ 'v1/user_info.do'
    PLACE_AN_ORDER =LBANK_API_URL+ 'v1/create_order.do'
    QUERY_ORDER = LBANK_API_URL + 'v1/orders_info.do'
    REVOCATION_OF_ORDER =LBANK_API_URL+ 'v1/cancel_order.do'
    QUERY_ORDER_HISTORY =LBANK_API_URL+ 'v1/orders_info_history.do'
    ACCESS_TO_OPEN_ORDER_FOR_USER =LBANK_API_URL+ 'v1/orders_info_no_deal.do'

    def __init__(self,api_key=None,secret_key=None):
        self._head = {'contentType': 'application/x-www-form-urlencoded'}
        self._api_key = api_key
        self._secret_key = secret_key

    def _generate_signature(self, dic):
        a = sorted(dic.items(), key=lambda x: x[0])
        str1 = ''
        for i in a:
            if i[0] != 'secret_key':
                str1 += i[0] + '=' + str(i[1]) + '&'
            else:
                abc = i[1]
        str1 = str1 + 'secret_key=' + abc
        m = hashlib.md5()
        m.update(str1.encode())
        return m.hexdigest().upper()


    def _requests_parms(self,api_key=None,secret_key=None,symbol=None,size=None,merge=None,
                       time=None,type=None,price=None,amount=None,order_id=None,current_page=None,
                        page_length=None):
        requests_data={}
        handle_data = {'api_key':api_key,'secret_key':secret_key,'symbol':symbol,'size':size,'merge':merge,
                       'time':time,'type':type,'price':price,'amount':amount,'order_id':order_id,
                       'current_page':current_page,'page_length':page_length}
        for k,v in handle_data.items():
            if v:
                requests_data[k]=v
        return requests_data


    def _init_session(self,url,re_dict):
        session = requests.session()
        session.headers.update({'contentType':'application/x-www-form-urlencoded'})
        if re_dict.get('api_key',None):
            re_dict['sign']=self._generate_signature(re_dict)
            return session.post(url=url,data=re_dict)
        else:
            return session.get(url=url,params=re_dict)


    def pair_quotation(self,symbol):
        '''Get the market'''
        url = Lbank_Api.PAIR_QUOTATION_URL
        print(self._requests_parms(symbol=symbol))
        return error_print(json.loads(self._init_session(url,self._requests_parms(symbol=symbol)).text))

    @classmethod
    def available(cls):
        '''Access to the LBank available Transaction pair to interface'''
        url = Lbank_Api.AVAILABLE_PAIR_URL
        return error_print(json.loads(requests.get(url).text))


    def market_depth(self,symbol,size,merge):
        '''Get the depth ofLBank,1 <= size <= 60, merge: 0 or 1'''
        url =Lbank_Api.MARKET_DEPTH_URL
        return error_print(json.loads(self._init_session(url, self._requests_parms(symbol=symbol,size=size,merge=merge)).text))


    def historical_transaction(self,symbol,size,start_time):
        '''Access to LBank historical transaction information, 1 <= size <= 600, start_time: %Y-%m-%d %H-%M'''
        tm = time.strptime(start_time, '%Y-%m-%d %H:%M')
        t = int(time.mktime(tm))
        url = Lbank_Api.HISTORICAL_TRANSACTION_URL
        return error_print(json.loads(self._init_session(url, self._requests_parms(symbol=symbol,size=size,time=t)).text))


    def kline_data(self,symbol,size,type,start_time):
        '''Get the K-line data,1 <= size <= 2880, start_time: %Y-%m-%d %H-%M
            tyoe:minute1：1minute
                minute5：5minute
                minute15：15minute
                minute30：30minute
                hour1：1hour
                hour4：4hour
                hour8：8hour
                hour12：12hour
                day1：1day
                week1：1week
                '''

        tm = time.strptime(start_time, '%Y-%m-%d %H:%M')
        t = int(time.mktime(tm))
        url = Lbank_Api.KLINE_DATA_URL
        return error_print(json.loads(self._init_session(url, self._requests_parms(symbol=symbol, size=size,type=type,time=t)).text))


    def essential_information(self):
        '''Get the basic information of all the money pairs'''
        url = Lbank_Api.ALL_PAIR_DATA
        return error_print(json.loads(requests.get(url).text))


    def user_transaction(self):
        '''Access to user account asset information'''
        url = Lbank_Api.GET_USER_ASSETS_URL
        data =self._requests_parms(api_key=self._api_key,secret_key=self._secret_key)
        return error_print(json.loads(self._init_session(url,data).text))


    def place_order(self,symbol,type,price,amount):
        '''Place an order,type: buy or sell ,price>=0 ,amount>=00.1'''
        url = Lbank_Api.PLACE_AN_ORDER
        data = self._requests_parms(api_key=self._api_key, secret_key=self._secret_key,symbol=symbol,type=type,price=price,amount=amount)
        return error_print(json.loads(self._init_session(url, data).text))


    def query_order(self,symbol,order_id):
        '''Query order'''
        url = Lbank_Api.QUERY_ORDER
        return error_print(json.loads(self._init_session(url, self._requests_parms(api_key=self._api_key, secret_key=self._secret_key,symbol=symbol,order_id=order_id)).text))



    def cancel_the_order(self,symbol,order_id):
        '''Cancel the order'''
        data = self._requests_parms(api_key=self._api_key, secret_key=self._secret_key,symbol=symbol,order_id=order_id)
        url = Lbank_Api.REVOCATION_OF_ORDER
        return error_print(json.loads(self._init_session(url, data).text))


    def query_h_order(self,symbol,current_page,page_length):
        '''Query order history,1<= page_length <= 200'''
        url = Lbank_Api.QUERY_ORDER_HISTORY
        data = self._requests_parms(api_key=self._api_key, secret_key=self._secret_key,symbol=symbol,current_page=current_page,page_length=page_length)
        return (json.loads(self._init_session(url, data).text))


    def open_order(self, symbol, current_page, page_length):
        '''Access to open orders for users,1<= page_length <= 200'''
        url = Lbank_Api.ACCESS_TO_OPEN_ORDER_FOR_USER
        data = self._requests_parms(api_key=self._api_key, secret_key=self._secret_key,symbol=symbol,current_page=current_page,page_length=page_length)
        return error_print(json.loads(self._init_session(url, data).text))


