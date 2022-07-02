# Проверяем обьем. если обьем больше 40М то начинает мониторить следующую свечу. Она должна быть противоположной
# по вектору текущей свече.Как только мы убеждаемся что она противоположная, то выставляем стоп-ордер по её хаю.
# Стоп лосс ниже лоэ
import requests
import json
import time
from time_modul import time_mod
from check_active_order import check_activ_ord


def check_volume():
    # Проверяем обьем, если он больше заданного, то переходим дальше
    print('вход в чек вольюм')
    i = 1
    while True:  # потом переписать код чтобы нижние 6 строк были в отдельной функции
        url = 'https://www.bitmex.com/api/v1/trade/bucketed?binSize=5m&partial=false&symbol=XBTUSD&count=1&reverse=true'
        resp = requests.get(url).text  # Со временем запустить проверку па времени или по обьему,которая будет
        data = json.loads(resp)  # проводится после модуля времени, на случай если новая свеча еще не появилась
        data1 = data[0]  # типа -> запрос(false)->time_mod-> запрос (сравниваем с предыдущим) если обьемы
        vol = data1['volume']  # различаются то норм, если совпадают, то повторить запрос(значит это еще старая свеча)
        print(f'проход № {i}  Текущий объём: {vol}')

        i += 1
        if vol < 30000000:  # 30000000 нужный объём
            print('Маленький объём')
            time_mod()
        else:
            print('У нас нужный объём, выполняем проверку на отклонение за последние 10 свечей')
            return deviation_price()


def deviation_price():
    # проверка на отклонение за последние 10 свечей
    url2 = 'https://www.bitmex.com/api/v1/trade/bucketed?binSize=5m&partial=false&symbol=XBTUSD&count=10&reverse=true'
    resp2 = requests.get(url2).text
    resp2_json = json.loads(resp2)
    resp_close_now = resp2_json[0]['close']
    resp_close_ten = resp2_json[9]['close']
    print('Проверяем изменение цены за десять свечей')
    print(f'now: {resp_close_now} ten candels later:  {resp_close_ten}')
    if abs(resp_close_ten - resp_close_now) >= 500:  # 500 нужный параметр
        print('Переходим к проверке разворотной свечи')
        i = 1
        return reversal_candle(i)
    else:
        print('ждем 5 минут до формирования следующей свечи')
        time.sleep(300)
        return print('переходим опять в чек вольюм'), check_volume()


def reversal_candle(i):
    # Проверка на нужный вектор свечи
    time_mod()
    url3 = 'https://www.bitmex.com/api/v1/trade/bucketed?binSize=5m&partial=false&symbol=XBTUSD&count=2&reverse=true'
    resp = requests.get(url3).text
    data = json.loads(resp)
    print('После запроса и вычислений на разворотную свечу получаем: ')
    data_new_op = data[0]['open']
    data_new_cl = data[0]['close']
    data_new_high_bitcoin = data[0]['high']
    data_new_low_bitcoin = data[0]['low']
    data_old_op = data[1]['open']
    data_old_cl = data[1]['close']
    difference_old = data_old_cl - data_old_op  # Направление старой свечи
    difference_new = data_new_cl - data_new_op  # Направление новой разворотной свечи
    reversal_candle_value = difference_new
    print('difference_old', difference_old)
    print('difference_new', difference_new)

    if (difference_old > 0) and (difference_new < 0):  # разворотная свеча красная
        print('Разворотная свеча сформирована (красная)')
        print('Переходим к функции открывающей ордер1')
        data_new_bitcoin = data_new_low_bitcoin - 10
        orderQty = -1
        return fun_open_order(orderQty, data_new_bitcoin, reversal_candle_value)

    elif (data_old_cl - data_old_op < 0) and (data_new_cl - data_new_op > 0):  # разворотная свеча зелёная
        print('Разворотная свеча сформирована (зеленая)\nПереходим к функции открывающей ордер2')
        data_new_bitcoin = data_new_high_bitcoin + 10
        orderQty = 1  # Для биткоина 100 минимум и кратно 100
        return fun_open_order(orderQty, data_new_bitcoin, reversal_candle_value)

    elif i < 5:  # нужный параметр 5
        print(f'У Нас две одинаковые по цвету свечи, ждем следущую. Проход № {i}')
        i += 1
        print(f'заходим в reversal_candle({i})')
        reversal_candle(i)
    else:
        print('Из 5-ти свечей нет пеперодной\nПереходим к началу программы')
        check_volume()  # Переходим в начало программы


# -------------------------------------------------------------------------------------------------


def fun_open_order(orderQty, data_new_bitcoin, reversal_candle_value):  # Сформирована разворотная свеча
    print('Перешли в функцию - fun_open_stop_order')
    print(
        f'сторона: {orderQty},макс или мин биткоин: {data_new_bitcoin}\n'
        f',цвет разворотной свечи: {reversal_candle_value}')

    print('Переходим к слежению за ценой - check_activ_ord ')
    check_activ_ord(orderQty, data_new_bitcoin, reversal_candle_value)
    print('Переходим к слежению за открытым ордером')



if __name__ == '__main__':
    print('Запуск программы')
    check_volume()

print('the end')