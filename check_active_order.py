import time
import json
import requests
#from time_modul import time_mod
#from trading_bitmex import new_market_order


def check_activ_ord(orderQty, data_new_bitcoin, reversal_candle_value):
    # Следим за ценой и открываем ордер
    k = 1
    while True:
        url = 'https://www.bitmex.com/api/v1/trade?symbol=XBTUSD&count=1&reverse=true'

        resp = requests.get(url).text
        data = json.loads(resp)
        data1 = (data[0]['price'])
        print(k,data1)
        time.sleep(2)
        k+=1
        if orderQty < 0:
            if data1 <= data_new_bitcoin:
                print('Открываем маркет на продажу')
                return new_market_order(orderQty)
            elif k > 140:  # 140
                print('Прошло 5 минут а ордер не открыт ждем\n'
                      ' формирования следующей разворотной свечи')
                print('Переходим в reversal_candle_comparison')
                return reversal_candle_comparison(reversal_candle_value, i=1)
        elif orderQty > 0:
            if data1 >= data_new_bitcoin:
                print('Открываем маркет на покупку')
                return new_market_order(orderQty)
            elif k > 140:  # 140
                print('Прошло 5 минут а ордер не открыт ждем\n'
                      ' формирования следующей разворотной свечи')
                print('Переходим в def reversal_candle_comparison')
                return reversal_candle_comparison(reversal_candle_value, i=1)



def reversal_candle_comparison(reversal_candle_value,i):
    # Сверяем значение разворотной свечи со следующей

    print(f'Мы вошли в reversal_candle_comparison проход № {i}')
    url3 = 'https://www.bitmex.com/api/v1/trade/bucketed?binSize=5m&partial=false&symbol=XBTUSD&count=2&reverse=true'# Поменять на XBT
    resp = requests.get(url3).text
    data = json.loads(resp)
    print('r_c_c После запроса и вычислений на разворотную свечу получаем: ')
    data_new_op_bit = data[0]['open']
    data_new_cl_bit = data[0]['close']
    data_new_high = round((data[0]['high']),4)
    data_new_low = round((data[0]['low']),4)
    difference_new = data_new_cl_bit - data_new_op_bit
    print('reversal_candle_value', reversal_candle_value)
    print('difference_new', difference_new)

    if ((reversal_candle_value > 0) and (difference_new < 0)) or ( # Если свеча противоположная разворотной, то ждем 5 мин
            (reversal_candle_value < 0) and (difference_new > 0)):
        time_mod()
        i += 1
        if i < 5:
            reversal_candle_comparison(reversal_candle_value, i) # Переходим в начало функции с i+1
        else:
            print('За пять свечей так и не сформировалась разворотная\nПереходим в начало программы')
            # Поставить переход в начало программы check_order()

    else: # Если свеча совпадает с разворотной, то переходим в check_activ_ord(reversal_candle_value)
        # передать параметры новой свечи хай или лоу в зависимости от цвета.Зеленая - хай и по ней выставим стоп-ордер на покупку
        if data_new_cl_bit - data_new_op_bit < 0: # Красная свеча
            price = data_new_low - 10
            check_activ_ord(-1, price, reversal_candle_value)
        else:                                     # Зеленая свеча
            price = data_new_high + 10
            check_activ_ord(1, price, reversal_candle_value)



#reversal_candle_comparison(reversal_candle_value=-5,i=1)