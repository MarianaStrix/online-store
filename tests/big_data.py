import random


def set_relatives(i):
    if i <= 2000:
        return [i-1] if i % 2 == 0 else [i+1]
    return []


def one_citizen(i):
    long_str = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean '
    'commodo ligula eget dolor. Aenean massa. Cum sociis natoque '
    'penatibus et magnis dis parturient montes, nascetur ridiculus '
    'mus. Donec quam feli'

    citizen = {
        'citizen_id': i,
        'town': long_str,
        'street': long_str,
        'building': long_str,
        'apartment': 7,
        'name': long_str,
        'birth_date': str(random.randint(1, 28)) + '.' +
                      str(random.randint(1, 12)) + '.' +
                      str(random.randint(1954, 2000)),
        'gender': 'male',
        'relatives': set_relatives(i)
    }
    return citizen


list_citizens = [one_citizen(i) for i in range(1, 10001)]


def big_data():
    return list_citizens
