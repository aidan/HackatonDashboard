from __future__ import division
import requests
import json
import sysboard.settings as cfg


def push_data(tile, key, data):
    requests.post('http://' + cfg.sysboard_address + '/api/v0.1/' + cfg.sysboard_apikey + '/push',
                  data={'tile': tile, 'key': key, 'data': json.dumps(data)})


def push_settings(tile, data):
    requests.post('http://' + cfg.sysboard_address + '/api/v0.1/' + cfg.sysboard_apikey + '/tileconfig/' +
                  tile, data={'value': json.dumps(data)})


def clean_get(key):
    rnum = cfg.redis.get(key)
    if not rnum:
        return 0
    else:
        return int(rnum)


def clean_time(raw):
    m, s = divmod(raw/100, 60)
    h, m = divmod(m, 60)
    return '%d:%02d:%02d' % (h, m, s)


def clean_transfer(raw, redis=True):
    if redis:
        return int((raw*8)/1000/cfg.refresh_time)
    else:
        return '{0:.2f}'.format((raw*8)/1000/1000/cfg.refresh_time) + ' Mb/s'