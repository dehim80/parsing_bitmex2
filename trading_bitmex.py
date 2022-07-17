# This file will contain commands for opening, closing and changed orders
import bitmex
import requests, time
import json


def new_market_order(orderQty):
    print(f'Мы вошли в функцию new_market_order сторона: {orderQty}')
    client = bitmex.bitmex(test=False, api_key='',
                           api_secret='')
    order_new_market = client.Order.Order_new(symbol='XRPUSD', orderQty=orderQty).result()
    ord_new_m_price = order_new_market[0]['price']
    orderID = order_new_market[0]['orderID']
    print (f'orderID: {orderID}')
    if orderQty > 0:
        ord_lim_price = ord_new_m_price + 0.01
        orderQty = -1
        stopPX = ord_new_m_price - 0.003 # нужный параметр  - 0.003
        #new_stop_order(orderQty, stopPX)
        new_limit_order(orderQty, ord_lim_price)
        check_open_ord(orderQty, stopPX, ord_lim_price, orderID)
    else:
        ord_lim_price = ord_new_m_price - 0.01
        orderQty = +1
        stopPX = ord_new_m_price + 0.003 # нужный параметр  + 0.003
        #new_stop_order(orderQty, stopPX)
        new_limit_order(orderQty, ord_lim_price)
        check_open_ord(orderQty, stopPX, ord_lim_price, orderID)

def close_market_order(orderQty):
    print(f'Мы вошли в функцию close_market_order сторона: {orderQty}')
    client = bitmex.bitmex(test=False, api_key='',
                           api_secret='')
    order_new_market = client.Order.Order_new(symbol='XRPUSD', orderQty=orderQty).result()
    ord_new_m_price = order_new_market[0]['price']
    orderID = order_new_market[0]['orderID']
    print(f'{orderID} price: {ord_new_m_price}')
    return


def new_limit_order(orderQty, price):
    # открывает позицию (orderQty=+1)-на покупку. (orderQty=-1)-на продажу.записывает orderId в файл order_id
    print(f'Мы вошли в функцию new_limit_order сторона: {orderQty} цена: {price} ')
    client = bitmex.bitmex(test=False, api_key='',
                           api_secret='')
    order_new = client.Order.Order_new(symbol='XRPUSD', orderQty=orderQty, ordType='Limit', price=price).result()
    print('лимитник выставлен  orderID: ',order_new[0]['orderID'])
    return


def new_stop_order(orderQty, stopPX):
    # открывает позицию (orderQty=+1)-на покупку. (orderQty=-1)-на продажу.записывает orderId в файл order_id
    print(f'Мы вошли в функцию new_stop_order сторона: {orderQty} цена: {stopPX}')
    client = bitmex.bitmex(test=False, api_key='',
                           api_secret='')
    order_new = client.Order.Order_new(symbol='XRPUSD', orderQty=orderQty, ordType='Stop', stopPx=stopPX).result()
    print('orderID: ', order_new[0]['orderID'])
    order_tpl = order_new[0]
    order_id_stop_order = order_tpl['orderID']

    with open("order_id.txt", "w") as somefile:
        somefile.write(order_id_stop_order)
    return


def close_position(orderID):
    # Закрывает позицию. Читает ID ордера из файла orderId
    client = bitmex.bitmex(test=False, api_key='',
                           api_secret='')

    client.Order.Order_cancel(orderID=orderID).result()
    print(f'Ордер закрыт  {orderID}')


def close_all_position():
    # Закрывает все позиции.
    print('Мы в функции close_all_position')
    client = bitmex.bitmex(test=False, api_key='',
                           api_secret='')

    client.Order.Order_cancelAll().result()
    print('Все ордера закрыты')




def check_open_ord(orderQty, stopPX, ord_lim_price, orderID):
    # функция слежения за открытым ордером, закрывать по стопу будем от сюда
    print('Мы вошли в функцию check_open_order')
    print(f'сторона: {orderQty} стоп-цена: {stopPX}\n'
          f'orderID {orderID} лимит-цена: {ord_lim_price}')
    while True:
        url = 'https://www.bitmex.com/api/v1/trade?symbol=XRPUSD&count=1&reverse=true'

        resp = requests.get(url).text
        data = json.loads(resp)
        data1 = (data[0]['price'])
        # print(data1) # использовать только при отладке
        time.sleep(2)
        if orderQty > 0:  # Если продажа то
            if data1 >= stopPX or data1 <= ord_lim_price:
                print('Вариант 1')
                close_all_position()
                close_market_order(1)
                return

        else:  # Если покупка то
            if data1 <= stopPX or data1 >= ord_lim_price:
                print('Вариант 2')
                close_all_position()
                close_market_order(-1)
                return


#if __name__=='__main__':
#    new_market_order(-1)
