from __future__ import division
import requests
import json
import threading
import sysboard.settings as cfg
from time import sleep


class widget(threading.Thread):
    def __init__(self):
        super(widget, self).__init__()
        self.alive = True
        self.timer = 0
        self.refresh = cfg.refresh_time

    def shutdown(self):
        self.alive = False

    def run(self):
        while self.alive:
            if self.timer >= self.refresh:
                self.timer = 0
                self.payload()
                print('TICK: ' + self.__class__.__name__)
            else:
                self.timer += 1
                sleep(1)
        print('SHUTDOWN: ' + self.__class__.__name__)

    def payload(self):
        pass


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
    if raw < 0:
        raw = 0
    if redis:
        return int((raw*8)/1000/cfg.refresh_time)
    else:
        return '{0:.2f}'.format((raw*8)/1000/1000/cfg.refresh_time) + ' Mb/s'