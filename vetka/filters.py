import random
from vetka import app

g_month = ['ёбанутобря', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
           'октября', 'ноября', 'декабря']


@app.template_filter('shuffle')
def filter_shuffle(seq):
    try:
        result = list(seq)
        random.shuffle(result)
        return result
    except Exception as e:
        print('Filter_shuffle failed: % s' % e)
        return seq


@app.template_filter('datetime_human')
def filter_datetime_human(dt):
    try:
        return '%s %s %s в %02d:%02d' % (dt.day, g_month[dt.month], dt.year, dt.hour, dt.minute)
    except Exception as e:
        print('Filter_datetime_human failed: % s' % e)
        return dt
