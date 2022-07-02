# скрипт ждет пока минуты будут кратные пяти.Затем выходит из функции.
import time


def time_mod():
    loc_hour = time.localtime().tm_hour
    loc_min = time.localtime().tm_min

    print(f'Мы зашли в фунцию time_mod {loc_hour}:{loc_min}')
    time.sleep(100)
    while True:
        local_time = time.localtime().tm_min
        loc2 = local_time % 5
        if (loc2 == 0) or local_time == 0:
            time.sleep(25)
            return
        else:
            time.sleep(10)
